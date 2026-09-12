#!/usr/bin/env python3
"""supergit — proactive git and worktree steward for AI-agent-driven projects.

One library (the shared main checkout, read-only), many rooms (worktrees, one
per task, started from origin/main, deleted when done). Work leaves a room only
through `ship` (branch + PR). Only the owner merges.

Every verb ends with the same three blocks so a non-technical owner never has
to read git:  Done / Waiting / You decide.

Usage: supergit <verb> [args]   (run `supergit help` for the verb table)
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

VERSION = "1.0.0"
SKILL_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = SKILL_DIR / "config.json"
# Projects come from config.json → "projects" (a list of {"id", "path", "origin"?}).
# SUPERGIT_PROJECTS=/path/a:/path/b adds more without editing the file.
TEMPLATE_DIR = SKILL_DIR / "templates"
ROOMS_DIR = ".claude/worktrees"          # same place Claude Code and the push gate use
AGENT_PREFIXES = ("claude", "codex", "hermes", "supergit")
DEFAULT_TTL_HOURS = 12
GATE_BASENAME = "push-verify"


# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------

class SupergitError(RuntimeError):
    pass


def sh(args: list[str], cwd: Path | None = None, check: bool = True, timeout: int = 600,
       env: dict | None = None, capture: bool = True) -> subprocess.CompletedProcess:
    merged = {**os.environ, **(env or {})}
    proc = subprocess.run(
        args, cwd=str(cwd) if cwd else None, text=True,
        capture_output=capture, timeout=timeout, env=merged,
    )
    if check and proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise SupergitError(f"`{' '.join(args)}` failed ({proc.returncode}): {detail[-800:]}")
    return proc


def git(args: list[str], cwd: Path, check: bool = True, timeout: int = 120) -> str:
    return sh(["git", *args], cwd=cwd, check=check, timeout=timeout).stdout.strip()


def has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def now() -> dt.datetime:
    return dt.datetime.now().astimezone()


def iso(t: dt.datetime) -> str:
    return t.replace(microsecond=0).isoformat()


def parse_iso(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s)


def hours_ago(s: str) -> float:
    return (now() - parse_iso(s)).total_seconds() / 3600


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:40] or "task"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}


def expand(p: str) -> Path:
    return Path(os.path.expanduser(p)).resolve()


def detect_agent() -> str:
    forced = os.environ.get("SUPERGIT_AGENT")
    if forced:
        return forced
    if os.environ.get("CLAUDECODE") or os.environ.get("CLAUDE_CODE"):
        return "claude-code"
    if any(k.startswith("CODEX") for k in os.environ):
        return "codex"
    if any(k.startswith("HERMES") for k in os.environ):
        return "hermes"
    return "unknown"


def branch_prefix() -> str:
    agent = detect_agent()
    return {"claude-code": "claude", "codex": "codex", "hermes": "hermes"}.get(agent, "supergit")


# ----------------------------------------------------------------------------
# report — the contract every verb honours
# ----------------------------------------------------------------------------

@dataclass
class Report:
    done: list[str] = field(default_factory=list)
    waiting: list[str] = field(default_factory=list)
    decide: list[str] = field(default_factory=list)
    detail: list[str] = field(default_factory=list)
    data: dict = field(default_factory=dict)

    def render(self, as_json: bool = False) -> str:
        if as_json:
            return json.dumps(
                {"done": self.done, "waiting": self.waiting, "decide": self.decide,
                 "detail": self.detail, "data": self.data},
                ensure_ascii=False, indent=2, default=str,
            )
        out: list[str] = []
        if self.detail:
            out.extend(self.detail)
            out.append("")
        out.append("✅ Done")
        out.extend(f"   {line}" for line in (self.done or ["nothing changed"]))
        out.append("⏳ Waiting")
        out.extend(f"   {line}" for line in (self.waiting or ["nothing running"]))
        out.append("❓ You decide")
        out.extend(f"   {line}" for line in (self.decide[:3] or ["nothing"]))
        if len(self.decide) > 3:
            out.append(f"   (+{len(self.decide) - 3} more — ask for `status`)")
        return "\n".join(out)


# ----------------------------------------------------------------------------
# repo model
# ----------------------------------------------------------------------------

@dataclass
class Repo:
    library: Path          # the main checkout
    git_dir: Path          # <library>/.git
    cwd_top: Path          # top-level of wherever we were invoked

    @property
    def sidecar_dir(self) -> Path:
        d = self.git_dir / "supergit"
        d.mkdir(exist_ok=True)
        return d

    @property
    def rooms_root(self) -> Path:
        return self.library / ROOMS_DIR

    @property
    def in_library(self) -> bool:
        return self.cwd_top == self.library

    @property
    def name(self) -> str:
        return self.library.name


def find_repo(start: Path | None = None) -> Repo:
    start = (start or Path.cwd()).resolve()
    try:
        common = git(["rev-parse", "--git-common-dir"], cwd=start)
        top = git(["rev-parse", "--show-toplevel"], cwd=start)
    except SupergitError as e:
        raise SupergitError(f"not inside a git repository: {start}") from e
    git_dir = (start / common).resolve() if not Path(common).is_absolute() else Path(common)
    library = git_dir.parent if git_dir.name == ".git" else Path(top).resolve()
    return Repo(library=library, git_dir=git_dir, cwd_top=Path(top).resolve())


def resolve_project(name_or_path: str | None) -> Repo:
    """A registry id, a path, or nothing (= cwd)."""
    if not name_or_path:
        return find_repo()
    p = Path(os.path.expanduser(name_or_path))
    if p.exists():
        return find_repo(p)
    for proj in registry_projects():
        if proj["id"] == name_or_path or proj["name"] == name_or_path:
            return find_repo(proj["path"])
    raise SupergitError(f"unknown project: {name_or_path}")


def registry_projects() -> list[dict]:
    """Every project supergit knows about: config.json "projects" + SUPERGIT_PROJECTS."""
    entries: list[dict] = list(load_config().get("projects", []))
    for extra in filter(None, os.environ.get("SUPERGIT_PROJECTS", "").split(":")):
        entries.append({"path": extra})
    out, seen = [], set()
    for proj in entries:
        path = proj.get("path") if isinstance(proj, dict) else proj
        if not path:
            continue
        full = expand(path)
        if full in seen or not (full / ".git").exists():
            continue
        seen.add(full)
        pid = proj.get("id") if isinstance(proj, dict) else None
        out.append({"id": pid or slugify(full.name), "name": proj.get("name", full.name) if isinstance(proj, dict) else full.name,
                    "origin": proj.get("origin") if isinstance(proj, dict) else None, "path": full})
    return out


# ----------------------------------------------------------------------------
# sidecars (one JSON per room, inside .git/supergit/)
# ----------------------------------------------------------------------------

def sidecar_path(repo: Repo, slug: str) -> Path:
    return repo.sidecar_dir / f"{slug}.json"


def load_sidecars(repo: Repo) -> dict[str, dict]:
    out = {}
    for f in repo.sidecar_dir.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            out[data["path"]] = data
        except (json.JSONDecodeError, KeyError):
            continue
    return out


def save_sidecar(repo: Repo, data: dict) -> None:
    sidecar_path(repo, data["slug"]).write_text(json.dumps(data, ensure_ascii=False, indent=2))


def current_sidecar(repo: Repo) -> dict | None:
    return load_sidecars(repo).get(str(repo.cwd_top))


# ----------------------------------------------------------------------------
# worktree inventory
# ----------------------------------------------------------------------------

@dataclass
class Room:
    path: Path
    head: str
    branch: str | None
    kind: str                      # library | supergit | claude-native | gate | foreign
    sidecar: dict | None = None
    dirty_tracked: int = 0
    untracked: int = 0
    unpushed: int = 0
    processes: int = 0
    age_h: float | None = None
    exists: bool = True
    nested: bool = False

    @property
    def clean(self) -> bool:
        return self.dirty_tracked == 0 and self.untracked == 0

    @property
    def ttl_h(self) -> float:
        return float((self.sidecar or {}).get("ttl_hours", DEFAULT_TTL_HOURS))

    @property
    def expired(self) -> bool:
        return self.age_h is not None and self.age_h > self.ttl_h

    @property
    def label(self) -> str:
        return (self.sidecar or {}).get("slug") or self.path.name


def list_rooms(repo: Repo, probe: bool = True) -> list[Room]:
    raw = git(["worktree", "list", "--porcelain"], cwd=repo.library)
    sidecars = load_sidecars(repo)
    rooms: list[Room] = []
    block: dict = {}

    def flush():
        if not block:
            return
        path = Path(block["worktree"]).resolve()
        branch = block.get("branch", "").replace("refs/heads/", "") or None
        kind = classify(repo, path, sidecars)
        room = Room(path=path, head=block.get("HEAD", "")[:8], branch=branch, kind=kind,
                    sidecar=sidecars.get(str(path)), exists=path.exists())
        if room.sidecar:
            room.age_h = hours_ago(room.sidecar["created"])
        elif room.exists:
            room.age_h = (time.time() - (path / ".git").stat().st_mtime) / 3600 if (path / ".git").exists() else None
        rooms.append(room)

    for line in raw.splitlines():
        if not line.strip():
            flush()
            block = {}
            continue
        key, _, value = line.partition(" ")
        block[key] = value
    flush()
    # nested = lives inside another worktree (a gate tree spawned from a push-worktree, etc.)
    paths = [x.path for x in rooms if x.kind != "library"]
    for x in rooms:
        if x.kind == "library":
            continue
        x.nested = any(other != x.path and str(x.path).startswith(str(other) + "/") for other in paths)
    if probe:
        procs = process_table()
        targets = [x for x in rooms if x.exists and x.kind != "library"]
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda x: probe_room(repo, x, procs), targets))
    return rooms


def process_table() -> str:
    proc = sh(["ps", "-eo", "args"], check=False)
    return proc.stdout or ""


def classify(repo: Repo, path: Path, sidecars: dict) -> str:
    if path == repo.library:
        return "library"
    if str(path) in sidecars:
        return "supergit"
    if path.name == GATE_BASENAME:
        return "gate"
    try:
        path.relative_to(repo.rooms_root)
        return "claude-native"
    except ValueError:
        return "foreign"


def probe_room(repo: Repo, room: Room, procs: str | None = None) -> None:
    status = git(["status", "--porcelain"], cwd=room.path, check=False)
    lines = [l for l in status.splitlines() if l.strip()]
    room.untracked = sum(1 for l in lines if l.startswith("??"))
    room.dirty_tracked = len(lines) - room.untracked
    room.unpushed = count_unpushed(room.path, room.branch)
    needle = f"{room.path}/"
    room.processes = procs.count(needle) if procs is not None else count_processes(room.path)


def count_unpushed(path: Path, branch: str | None) -> int:
    if branch:
        up = git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], cwd=path, check=False)
        if up and "fatal" not in up:
            out = git(["rev-list", "--count", f"{up}..HEAD"], cwd=path, check=False)
            return int(out) if out.isdigit() else 0
    out = git(["rev-list", "--count", "origin/main..HEAD"], cwd=path, check=False)
    return int(out) if out.isdigit() else 0


def count_processes(path: Path) -> int:
    proc = sh(["pgrep", "-f", f"{path}/"], check=False)
    return len([l for l in proc.stdout.splitlines() if l.strip()])


def changed_files(path: Path) -> set[str]:
    """Files this room's HEAD touches relative to origin/main — its own work,
    not origin/main's drift since the room forked (three-dot, not two-dot)."""
    out = git(["diff", "--name-only", "origin/main...HEAD"], cwd=path, check=False)
    return {l.strip() for l in out.splitlines() if l.strip()}


def find_overlaps(rooms: list[Room]) -> list[tuple[Room, Room, set[str]]]:
    """Pairwise file overlap across rooms that still have live, unshipped work.
    A room that is clean and fully pushed already left through `ship` — its
    files stop mattering here the moment a PR exists to review instead."""
    active = [x for x in rooms if x.kind in ("supergit", "claude-native", "foreign") and x.exists and (not x.clean or x.unpushed)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        file_sets = list(pool.map(lambda x: changed_files(x.path), active))
    found = []
    for i, a in enumerate(active):
        for j in range(i + 1, len(active)):
            shared = file_sets[i] & file_sets[j]
            if shared:
                found.append((a, active[j], shared))
    return found


# ----------------------------------------------------------------------------
# deploy awareness — read through GitHub, which the host (Vercel, Netlify…)
# writes to: one Deployment per build, one status per outcome. `gh` alone then
# answers the three questions that matter to a non-technical owner: is
# production running what's on main, are two production builds racing, and
# are previews failing.
# ----------------------------------------------------------------------------

def github_slug(repo: Repo) -> str | None:
    url = git(["remote", "get-url", "origin"], cwd=repo.library, check=False)
    m = re.search(r"github\.com[:/]([^/\s]+)/([^/\s]+?)(?:\.git)?/?$", url)
    return f"{m.group(1)}/{m.group(2)}" if m else None


def gh_json(args: list[str], cwd: Path, timeout: int = 30):
    proc = sh(["gh", *args], cwd=cwd, check=False, timeout=timeout)
    if proc.returncode != 0 or not (proc.stdout or "").strip():
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def deploy_capable(repo: Repo) -> bool:
    lib = repo.library
    return any((lib / p).exists() for p in ("vercel.json", ".vercel", "netlify.toml", "railway.json", "fly.toml"))


def deploy_state(repo: Repo, limit: int = 12) -> dict | None:
    """Returns None when the repo has no host, no GitHub origin, or no `gh`."""
    slug = github_slug(repo)
    if not slug or not has("gh") or not deploy_capable(repo):
        return None
    deps = gh_json(["api", f"repos/{slug}/deployments?per_page={limit}"], repo.library)
    if not isinstance(deps, list):
        return None

    def with_status(d: dict) -> dict:
        st = gh_json(["api", f"repos/{slug}/deployments/{d['id']}/statuses?per_page=1"], repo.library, timeout=20)
        s = st[0] if isinstance(st, list) and st else {}
        return {"env": (d.get("environment") or "").lower(), "sha": d.get("sha") or "", "created": d.get("created_at"),
                "state": s.get("state") or "pending", "url": s.get("environment_url") or s.get("target_url")}

    with ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(with_status, deps))
    prod = [x for x in rows if x["env"] == "production"]
    prev = [x for x in rows if x["env"] == "preview"]
    live = next((x for x in prod if x["state"] == "success"), None)
    head = git(["rev-parse", "origin/main"], cwd=repo.library, check=False)
    head_age_min = None
    ts = git(["log", "-1", "--format=%ct", "origin/main"], cwd=repo.library, check=False)
    if ts.isdigit():
        head_age_min = (time.time() - int(ts)) / 60
    # Vercel writes the GitHub record when a build FINISHES, so an in-flight
    # production build is invisible here. A main that moved in the last 25 min
    # is therefore "probably building", not "nothing is building".
    head_probably_building = head_age_min is not None and head_age_min < 25 and not (live and live["sha"] == head)
    # Racing = two production builds that finished within 30 min of each other:
    # two pushes hit main in quick succession, and the later finish wins.
    times = sorted((parse_iso(x["created"].replace("Z", "+00:00")) for x in prod if x.get("created")), reverse=True)
    burst = sum(1 for t in times if (times[0] - t).total_seconds() < 1800) if times else 0
    return {
        "slug": slug, "head": head, "rows": rows, "head_age_min": head_age_min,
        "production": prod[0] if prod else None,          # newest finished production build, whatever its outcome
        "live": live,                                      # newest production build that succeeded
        "burst": burst,                                    # production builds inside the last 30-min window
        "head_deployed": bool(live and live["sha"] == head),
        "head_building": head_probably_building,
        "preview_failed": sum(1 for x in prev[:10] if x["state"] in ("failure", "error")),
        "preview_seen": min(len(prev), 10),
    }


def deploy_summary(ds: dict | None) -> str:
    """One short phrase for a brief line; '' when there is nothing to say."""
    if not ds or not ds["rows"]:
        return ""
    p = ds["production"]
    if ds["burst"] > 1:
        s = f"prod ⚠️ {ds['burst']} builds in 30 min"
    elif p and p["state"] in ("failure", "error"):
        s = f"prod ❌ last build failed ({p['sha'][:7]})"
    elif ds["head_deployed"]:
        s = "prod ✅"
    elif ds["head_building"]:
        s = f"prod ⏳ main moved {ds['head_age_min']:.0f}m ago, build likely in flight"
    elif ds["live"]:
        s = f"prod ⚠️ on {ds['live']['sha'][:7]}, main is {ds['head'][:7]}"
    else:
        s = "prod ? no successful build recorded"
    if ds["preview_failed"] >= 3:
        s += f" · previews ❌ {ds['preview_failed']}/{ds['preview_seen']}"
    return s


def direct_pushes(repo: Repo, n: int = 15) -> list[tuple[str, str]]:
    """Commits on origin/main that never went through a pull request.
    Squash merges leave the PR's merge commit on main; a merge-commit strategy
    leaves the PR's own commits — GitHub's commits/{sha}/pulls covers both."""
    slug = github_slug(repo)
    if not slug or not has("gh"):
        return []
    merged = gh_json(["pr", "list", "--state", "merged", "--limit", "100", "--json", "mergeCommit"], repo.library) or []
    via_pr = {(m.get("mergeCommit") or {}).get("oid") for m in merged}
    log = git(["log", "--no-merges", "--format=%H %s", "-n", str(n), "--since=24.hours", "origin/main"], cwd=repo.library, check=False)
    candidates = []
    for line in log.splitlines():
        sha, _, subject = line.partition(" ")
        if sha and sha not in via_pr and not re.search(r"\(#\d+\)\s*$", subject):
            candidates.append((sha, subject))
    if not candidates:
        return []

    def has_pr(item):
        prs = gh_json(["api", f"repos/{slug}/commits/{item[0]}/pulls"], repo.library, timeout=20)
        return bool(prs)

    with ThreadPoolExecutor(max_workers=8) as pool:
        flags = list(pool.map(has_pr, candidates))
    return [(sha[:8], subj) for (sha, subj), ok in zip(candidates, flags) if not ok]


def preview_for(ds: dict | None, sha: str) -> dict | None:
    if not ds or not sha:
        return None
    return next((x for x in ds["rows"] if x["env"] == "preview" and x["sha"] == sha), None)


def library_state(repo: Repo, fetch: bool = True) -> dict:
    lib = repo.library
    if fetch:
        sh(["git", "fetch", "--quiet", "origin", "main"], cwd=lib, check=False, timeout=30)
    counts = git(["rev-list", "--left-right", "--count", "origin/main...HEAD"], cwd=lib, check=False).split()
    behind, ahead = (int(counts[0]), int(counts[1])) if len(counts) == 2 else (0, 0)
    status = [l for l in git(["status", "--porcelain"], cwd=lib, check=False).splitlines() if l.strip()]
    untracked = sum(1 for l in status if l.startswith("??"))
    unique_ahead = ahead
    if ahead:
        cherry = git(["cherry", "origin/main", "HEAD"], cwd=lib, check=False)
        unique_ahead = sum(1 for l in cherry.splitlines() if l.startswith("+"))
    return {"behind": behind, "ahead": ahead, "unique_ahead": unique_ahead,
            "dirty_tracked": len(status) - untracked, "untracked": untracked,
            "branch": git(["branch", "--show-current"], cwd=lib, check=False)}


# ----------------------------------------------------------------------------
# project rules: `## Ship gate` in AGENTS.md / CLAUDE.md
# ----------------------------------------------------------------------------

def read_ship_gate(library: Path) -> dict:
    """Returns {"commands": [...], "hook": bool, "merge_deploys": str|None}."""
    gate = {"commands": [], "hook": False, "merge_deploys": None}
    for name in ("AGENTS.md", "CLAUDE.md"):
        f = library / name
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^## Ship gate\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
        if not m:
            continue
        section = m.group(1)
        fence = re.search(r"```(?:bash|sh)?\s*\n(.*?)```", section, re.S)
        if fence:
            gate["commands"] = [l.strip() for l in fence.group(1).splitlines() if l.strip() and not l.strip().startswith("#")]
        if re.search(r"^\s*-?\s*hook:\s*pre-push", section, re.M):
            gate["hook"] = True
        md = re.search(r"^\s*-?\s*merge-deploys:\s*(\S+)", section, re.M)
        if md:
            gate["merge_deploys"] = md.group(1)
        return gate
    # defaults when no section exists
    pkg = library / "package.json"
    if pkg.exists():
        scripts = json.loads(pkg.read_text()).get("scripts", {})
        if "verify:push" in scripts:
            gate["hook"] = True
        elif "build" in scripts:
            gate["commands"] = ["npm run build"]
    return gate


# ----------------------------------------------------------------------------
# verbs
# ----------------------------------------------------------------------------

def verb_status(args) -> Report:
    repo = resolve_project(args.project)
    r = Report()
    lib = library_state(repo, fetch=not args.no_fetch)
    rooms = list_rooms(repo)
    r.data = {"library": str(repo.library), "library_state": lib, "rooms": [room_dict(x) for x in rooms]}

    r.detail.append(f"📚 {repo.name} — library {repo.library}")
    lib_line = f"   branch {lib['branch'] or '?'} · {lib['behind']} behind origin/main · {lib['ahead']} ahead"
    if lib["dirty_tracked"] or lib["untracked"]:
        lib_line += f" · ⚠️ dirty ({lib['dirty_tracked']} modified, {lib['untracked']} untracked) — the library should be read-only"
    r.detail.append(lib_line)
    r.detail.append("")
    others = [x for x in rooms if x.kind != "library"]
    r.detail.append(f"🚪 rooms: {len(others)}")
    for x in sorted(others, key=lambda k: (k.kind, k.path)):
        r.detail.append("   " + room_line(x))
    sweepable = [x for x in others if x.kind == "supergit" and x.expired and x.clean and x.unpushed == 0 and x.processes == 0]
    if sweepable:
        r.detail.append(f"   → `cleanup` would remove {len(sweepable)} expired clean room(s)")

    overlaps = find_overlaps(others)
    if overlaps:
        r.detail.append("")
        r.detail.append(f"⚠️  {len(overlaps)} pair(s) of rooms touch the same file(s):")
        for a, b, shared in overlaps:
            sample = ", ".join(sorted(shared)[:4]) + ("…" if len(shared) > 4 else "")
            r.detail.append(f"   `{a.label}` × `{b.label}` — {sample}")
        for a, b, shared in overlaps[:2]:
            r.decide.append(f"`{a.label}` and `{b.label}` both touch {len(shared)} file(s) — same task, or will one conflict the other on ship?")

    if lib["ahead"] and lib["unique_ahead"] == 0:
        r.detail.append(f"   ℹ️ the {lib['ahead']} local commit(s) already exist on origin in equivalent form — `sync --reset-equivalent` is lossless")
    if lib["behind"] and not lib["dirty_tracked"] and not lib["ahead"]:
        r.decide.append(f"library is {lib['behind']} behind — run `sync`? (yes/no)")
    if lib["dirty_tracked"]:
        r.decide.append(f"library has {lib['dirty_tracked']} modified file(s) — someone edited the library; keep, or move to a room? (keep/move)")
    for x in others:
        if x.kind in ("supergit", "claude-native") and x.expired and not x.clean:
            r.decide.append(f"room `{x.label}` is past TTL with unsaved changes — ship, park, or abandon?")
        elif x.kind in ("supergit", "claude-native") and x.expired and x.unpushed:
            r.decide.append(f"room `{x.label}` has {x.unpushed} unpushed commit(s) — ship or park?")
    nested = [x for x in others if x.kind == "gate" and x.nested]
    if nested:
        r.decide.append(f"{len(nested)} nested gate tree(s) found — remove with `cleanup --go`? (yes/no)")
    r.done.append(f"inspected {len(others)} room(s)")
    return r


def room_dict(x: Room) -> dict:
    return {"path": str(x.path), "kind": x.kind, "branch": x.branch, "head": x.head, "dirty": x.dirty_tracked,
            "untracked": x.untracked, "unpushed": x.unpushed, "processes": x.processes, "age_h": x.age_h,
            "expired": x.expired, "exists": x.exists, "nested": x.nested,
            "task": (x.sidecar or {}).get("task"), "agent": (x.sidecar or {}).get("agent")}


def room_line(x: Room) -> str:
    flags = []
    if not x.exists:
        flags.append("missing on disk")
    if x.dirty_tracked or x.untracked:
        flags.append(f"dirty {x.dirty_tracked}+{x.untracked}u")
    if x.unpushed:
        flags.append(f"{x.unpushed} unpushed" if x.branch else f"{x.unpushed} commit(s) not on main")
    if x.processes:
        flags.append(f"{x.processes} proc")
    if x.nested:
        flags.append("NESTED")
    if x.expired:
        flags.append("expired")
    age = f"{x.age_h:.0f}h" if x.age_h is not None else "?"
    who = (x.sidecar or {}).get("agent", "")
    task = (x.sidecar or {}).get("task", "")
    core = f"[{x.kind}] {x.label} · {x.branch or 'detached'} · {age}"
    if who:
        core += f" · {who}"
    if task:
        core += f" · “{task[:50]}”"
    return core + (f"  ⚠️ {', '.join(flags)}" if flags else "  ✓ clean")


def verb_start(args) -> Report:
    repo = resolve_project(args.project)
    r = Report()
    slug = slugify(args.slug)
    ts = now().strftime("%Y%m%d-%H%M")
    room_name = f"{slug}-{ts}"
    branch = f"{branch_prefix()}/{room_name}"
    room_path = repo.rooms_root / room_name

    # overlap check
    existing = [x for x in list_rooms(repo, probe=False) if x.kind in ("supergit", "claude-native")]
    words = set(slug.split("-"))
    overlaps = [x for x in existing if words & set(slugify(x.label).split("-")) - {"fix", "update", "new", "the", "push", "gate", "release", "refactor", "cleanup", "tidy", "and", "for", "to"}]
    if overlaps and not args.force:
        for x in overlaps:
            r.detail.append(f"   existing room looks related: {room_line(x)}")
        r.decide.append("a related room already exists — continue there, or start a new one? (`start --force` to create anyway)")
        r.done.append("nothing created")
        return r

    sh(["git", "fetch", "--quiet", "origin"], cwd=repo.library, timeout=60)
    repo.rooms_root.mkdir(parents=True, exist_ok=True)
    ensure_excluded(repo, ROOMS_DIR + "/")
    git(["worktree", "add", "-b", branch, str(room_path), "origin/main"], cwd=repo.library)
    base = git(["rev-parse", "origin/main"], cwd=repo.library)

    linked = link_dependencies(repo.library, room_path) if not args.no_deps else "skipped"
    env_local = repo.library / ".env.local"
    if env_local.exists():
        shutil.copyfile(env_local, room_path / ".env.local")

    sidecar = {
        "slug": room_name, "agent": detect_agent(), "task": args.task or args.slug,
        "path": str(room_path), "branch": branch, "base": base, "created": iso(now()),
        "ttl_hours": args.ttl, "granted": ["ship"] if args.grant_ship else [],
        "notes": [], "shipped": None,
    }
    save_sidecar(repo, sidecar)
    r.data = sidecar
    r.done.append(f"room `{room_name}` opened from origin/main ({base[:8]})")
    r.done.append(f"branch {branch}")
    r.done.append(f"dependencies: {linked}")
    if args.grant_ship:
        r.done.append("ship granted for this task — no need to ask again")
    r.detail.append(f"cd {room_path}")
    r.detail.append("when done: `supergit finish`  ·  to save progress: `supergit park`  ·  idea? `supergit note \"…\"`")
    return r


def ensure_excluded(repo: Repo, pattern: str) -> None:
    probe = pattern.rstrip("/") + "/x"
    if sh(["git", "check-ignore", "-q", probe], cwd=repo.library, check=False).returncode == 0:
        return
    exclude = repo.git_dir / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude.read_text() if exclude.exists() else ""
    if pattern not in existing.splitlines():
        exclude.write_text(existing.rstrip("\n") + f"\n{pattern}\n")


def link_dependencies(library: Path, room: Path) -> str:
    """Same method as scripts/verify-pushed-tree.mjs: hardlink farm, lockfile stamp."""
    src = library / "node_modules"
    if not src.exists():
        return "none (library has no node_modules)"
    lock = library / "package-lock.json"
    stamp = hashlib.sha256(lock.read_bytes()).hexdigest() if lock.exists() else "no-lockfile"
    dest = room / "node_modules"
    if dest.exists():
        shutil.rmtree(dest)
    proc = sh(["cp", "-RlP", str(src), str(dest)], check=False, timeout=900)
    if proc.returncode != 0:
        return f"link failed — run `npm install` in the room ({(proc.stderr or '').strip()[-200:]})"
    (room / ".node-modules-stamp").write_text(stamp)
    return "node_modules hardlinked from the library"


def require_room(repo: Repo) -> dict:
    if repo.in_library:
        raise SupergitError("you are in the library (the shared main checkout). Rooms only: `supergit start <slug>`")
    sc = current_sidecar(repo)
    if not sc:
        # adopt a claude-native or foreign room on first use
        branch = git(["branch", "--show-current"], cwd=repo.cwd_top, check=False) or None
        sc = {
            "slug": repo.cwd_top.name, "agent": detect_agent(), "task": repo.cwd_top.name,
            "path": str(repo.cwd_top), "branch": branch,
            "base": git(["merge-base", "HEAD", "origin/main"], cwd=repo.cwd_top, check=False),
            "created": iso(now()), "ttl_hours": DEFAULT_TTL_HOURS, "granted": [], "notes": [],
            "shipped": None, "adopted": True,
        }
        save_sidecar(repo, sc)
    return sc


def verb_label(args) -> Report:
    """Give the current room a task name. Claude Code makes its own worktree per
    session and never calls `start`, so without this the room shows up in
    `status` as a bare folder name and nobody can tell what it was for."""
    repo = find_repo()
    sc = require_room(repo)
    old = sc.get("task")
    sc["task"] = args.text.strip()
    save_sidecar(repo, sc)
    r = Report()
    r.done.append(f"room `{sc['slug']}` is now labelled “{sc['task'][:60]}”" + (f" (was “{old[:40]}”)" if old and old != sc["task"] else ""))
    r.done.append("name the session the same way, so the sidebar and `status` agree")
    return r


def verb_note(args) -> Report:
    repo = find_repo()
    sc = require_room(repo)
    sc.setdefault("notes", []).append({"at": iso(now()), "text": args.text})
    save_sidecar(repo, sc)
    r = Report()
    r.done.append(f"noted on room `{sc['slug']}` ({len(sc['notes'])} note(s)) — surfaces at ship and finish, not in memory")
    return r


def commit_room(repo: Repo, sc: dict, message: str, trailer: str | None) -> str | None:
    room = repo.cwd_top
    git(["add", "-A"], cwd=room)
    staged = git(["diff", "--cached", "--name-only"], cwd=room)
    if not staged:
        return None
    full = message.strip().rstrip(".")
    if trailer:
        full += f"\n\n{trailer}"
    git(["commit", "-q", "-m", full], cwd=room)
    return git(["rev-parse", "--short", "HEAD"], cwd=room)


def push_branch(room: Path, branch: str, gate_cb, env: dict | None = None) -> tuple[bool, str]:
    """Push with one rebase retry. Returns (ok, note)."""
    for attempt in (1, 2):
        proc = sh(["git", "push", "-u", "origin", f"HEAD:refs/heads/{branch}"], cwd=room, check=False, timeout=1800, env=env)
        if proc.returncode == 0:
            return True, "pushed" if attempt == 1 else "pushed after one rebase"
        err = (proc.stderr or "") + (proc.stdout or "")
        if attempt == 1 and ("non-fast-forward" in err or "rejected" in err or "fetch first" in err):
            sh(["git", "fetch", "--quiet", "origin"], cwd=room, check=False, timeout=60)
            rb = sh(["git", "rebase", "origin/main"], cwd=room, check=False, timeout=300)
            if rb.returncode != 0:
                sh(["git", "rebase", "--abort"], cwd=room, check=False)
                return False, "rebase onto origin/main hit a conflict — stopped, nothing lost"
            ok, note = gate_cb()
            if not ok:
                return False, f"gate failed after rebase: {note}"
            continue
        return False, err.strip()[-600:]
    return False, "push rejected twice"


def run_gate(room: Path, gate: dict, skip: bool) -> tuple[bool, str]:
    if skip:
        return True, "gate skipped (--skip-gate)"
    if gate["hook"] and not gate["commands"]:
        return True, "gate runs inside the pre-push hook"
    for cmd in gate["commands"]:
        proc = subprocess.run(cmd, shell=True, cwd=str(room), text=True, capture_output=True, timeout=3600)
        if proc.returncode != 0:
            tail = (proc.stdout + proc.stderr).strip().splitlines()[-15:]
            return False, f"`{cmd}` failed:\n" + "\n".join(tail)
    return True, f"{len(gate['commands'])} gate command(s) passed" if gate["commands"] else "no gate configured"


def verb_park(args) -> Report:
    repo = find_repo()
    sc = require_room(repo)
    r = Report()
    sha = commit_room(repo, sc, args.message or f"wip: {sc['task']}", args.trailer or os.environ.get("SUPERGIT_TRAILER"))
    if sha:
        r.done.append(f"saved as {sha}")
    branch = sc.get("branch") or git(["branch", "--show-current"], cwd=repo.cwd_top)
    ok, note = push_branch(repo.cwd_top, branch, lambda: (True, "no gate on park"), env={"SUPERGIT_SKIP_GATE": "1"})
    r.done.append(f"branch {branch}: {note}" if ok else f"could not push: {note}")
    r.done.append("room stays — come back any time")
    return r


def verb_ship(args) -> Report:
    repo = find_repo()
    sc = require_room(repo)
    r = Report()
    room = repo.cwd_top
    branch = sc.get("branch") or git(["branch", "--show-current"], cwd=room)
    if not branch or branch in ("main", "master"):
        raise SupergitError("this room is not on a feature branch — ship refuses to push main")

    gate = read_ship_gate(repo.library)
    message = args.message or sc["task"]
    trailer = f"Supergit-Room: {sc['slug']}"
    extra = args.trailer or os.environ.get("SUPERGIT_TRAILER")
    if extra:
        trailer = f"{extra}\n{trailer}"
    sha = commit_room(repo, sc, message, trailer)
    r.done.append(f"committed {sha}" if sha else "nothing new to commit")

    ok, note = run_gate(room, gate, args.skip_gate)
    if not ok:
        r.done.append("gate failed — nothing pushed")
        r.detail.append(note)
        r.decide.append("fix the failing check and `ship` again, or `park` to save progress? (fix/park)")
        return r
    r.done.append(note)

    ok, note = push_branch(room, branch, lambda: run_gate(room, gate, args.skip_gate))
    if not ok:
        r.done.append("push failed")
        r.detail.append(note)
        r.decide.append("push was rejected — retry, or ask for help? (retry/help)")
        return r
    r.done.append(f"branch {branch}: {note}")

    pr_url = None
    if not args.no_pr:
        pr_url = open_pr(repo, sc, branch, gate, args)
        r.done.append(f"PR: {pr_url}")
    sc["shipped"] = {"sha": git(["rev-parse", "HEAD"], cwd=room), "pr": pr_url, "at": iso(now())}
    save_sidecar(repo, sc)
    r.data = {"branch": branch, "pr": pr_url}
    if pr_url:
        n = pr_url.rsplit("/", 1)[-1]
        if deploy_capable(repo):
            r.waiting.append(f"preview build for {branch} — the host starts it on its own; `review {n}` shows the link when it's ready")
            r.decide.append(f"look at the preview, then merge? → `supergit review {n}`")
        else:
            r.decide.append(f"review and merge? → `supergit review {n}`")
    return r


def open_pr(repo: Repo, sc: dict, branch: str, gate: dict, args) -> str:
    if not has("gh"):
        raise SupergitError("GitHub CLI `gh` is not installed — branch is pushed, open the PR by hand")
    room = repo.cwd_top
    existing = sh(["gh", "pr", "list", "--head", branch, "--json", "url", "--limit", "1"], cwd=room, check=False)
    if existing.returncode == 0:
        found = json.loads(existing.stdout or "[]")
        if found:
            return found[0]["url"]
    title = (args.title or sc["task"]).strip()[:70]
    body = args.body_file and Path(args.body_file).read_text() or pr_body(repo, sc, gate, args)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(body)
        body_path = f.name
    proc = sh(["gh", "pr", "create", "--base", "main", "--head", branch, "--title", title, "--body-file", body_path],
              cwd=room, check=False, timeout=120)
    os.unlink(body_path)
    if proc.returncode != 0:
        raise SupergitError(f"gh pr create failed: {(proc.stderr or proc.stdout).strip()[-400:]}")
    return proc.stdout.strip().splitlines()[-1]


def pr_body(repo: Repo, sc: dict, gate: dict, args) -> str:
    room = repo.cwd_top
    commits = git(["log", "--oneline", "origin/main..HEAD"], cwd=room, check=False)
    files = git(["diff", "--stat", "origin/main...HEAD"], cwd=room, check=False)
    notes = "\n".join(f"- {n['text']}" for n in sc.get("notes", [])) or "none"
    deploy = gate.get("merge_deploys")
    deploy_line = (f"⚠️ **Merging deploys to {deploy}.**" if deploy
                   else "Check whether merging deploys this project before you merge.")
    return f"""## What changed
{args.summary or "_(agent: replace with 3–6 plain sentences — what a user of the product would notice)_"}

## What I verified
{args.verified or "- build/gate: see Details"}

## Risk
{args.risk or "_(agent: Low / Medium / High, and the one thing most likely to go wrong)_"}

## Merging this
{deploy_line}
Undo: `supergit undo <this PR number>`

## Follow-ups (not in this PR)
{notes}

## Details for reviewers
Task: {sc['task']}  ·  Room: `{sc['slug']}`  ·  Agent: {sc.get('agent')}

```
{commits or '(no commits ahead of origin/main)'}
```

```
{files}
```
"""


def verb_finish(args) -> Report:
    repo = find_repo()
    r = Report()
    if repo.in_library:
        raise SupergitError("you are in the library — nothing to finish here. `status` shows the rooms.")
    sc = require_room(repo)
    room = repo.cwd_top
    rooms = {x.path: x for x in list_rooms(repo)}
    me = rooms.get(room)
    if me is None:
        raise SupergitError("this directory is not a registered worktree")

    blockers = []
    if not me.clean:
        blockers.append(f"{me.dirty_tracked} modified + {me.untracked} untracked file(s) unsaved")
    if me.unpushed and not args.keep_branch:
        blockers.append(f"{me.unpushed} commit(s) not pushed")
    notes = sc.get("notes", [])
    if notes:
        r.detail.append("📝 notes from this room:")
        r.detail.extend(f"   - {n['text']}" for n in notes)
    if blockers:
        r.done.append("room kept — " + "; ".join(blockers))
        r.decide.append("unsaved work here — `ship`, `park`, or `abandon`? (ship/park/abandon)")
        return r
    if args.dry_run:
        r.done.append("dry run — room is clean and pushed; `finish` would remove it")
        if notes:
            r.decide.append("keep these notes somewhere (drafts/ or vault), or drop them? (keep/drop)")
        return r

    if me.processes:
        sh(["pkill", "-f", f"{room}/"], check=False)
        time.sleep(1)
        sh(["pkill", "-9", "-f", f"{room}/"], check=False)
    os.chdir(repo.library)
    git(["worktree", "remove", "--force", str(room)], cwd=repo.library)
    git(["worktree", "prune"], cwd=repo.library)
    sidecar_path(repo, sc["slug"]).unlink(missing_ok=True)
    r.done.append(f"room `{sc['slug']}` closed")
    if sc.get("branch") and not sc.get("shipped"):
        r.done.append(f"branch {sc['branch']} kept on origin (not merged)")
    if notes:
        r.decide.append("keep the notes above somewhere (drafts/ or vault), or drop them? (keep/drop)")
    return r


def verb_sync(args) -> Report:
    repo = resolve_project(args.project)
    r = Report()
    lib = repo.library
    sh(["git", "fetch", "--quiet", "origin", "main"], cwd=lib, timeout=60)
    state = library_state(repo, fetch=False)
    if state["dirty_tracked"]:
        files = git(["diff", "--name-only"], cwd=lib, check=False).splitlines()[:8]
        r.done.append("refused — the library has uncommitted edits (it should be read-only)")
        r.detail.extend(f"   {f}" for f in files)
        r.decide.append("someone edited the library — move those edits to a room, or discard them? (move/discard)")
        return r
    if state["ahead"] and state["unique_ahead"] == 0 and getattr(args, "reset_equivalent", False):
        git(["reset", "--hard", "origin/main"], cwd=lib)
        r.done.append(f"library moved to origin/main — its {state['ahead']} local commit(s) already existed there in equivalent form, nothing lost")
        return r
    if state["ahead"]:
        r.done.append(f"refused — the library has {state['ahead']} local commit(s) not on origin; a plain fast-forward is impossible")
        if state["unique_ahead"] == 0:
            r.detail.append(f"   all {state['ahead']} local commit(s) already exist on origin in equivalent form (same change, different SHA)")
            r.decide.append("safe to move the library onto origin/main — `sync --reset-equivalent`? (yes/no)")
        else:
            r.decide.append(f"{state['unique_ahead']} local commit(s) are genuinely unique — push them from a room, or discard? (push/discard — discard needs a named authorization)")
        return r
    if not state["behind"]:
        r.done.append("library already current with origin/main")
        return r
    git(["merge", "--ff-only", "origin/main"], cwd=lib)
    r.done.append(f"library fast-forwarded by {state['behind']} commit(s) to {git(['rev-parse', '--short', 'HEAD'], cwd=lib)}")
    return r


def verb_cleanup(args) -> Report:
    repo = resolve_project(args.project)
    r = Report()
    go = args.go
    rooms = [x for x in list_rooms(repo) if x.kind != "library"]
    plan: list[tuple[str, Room]] = []
    human: list[str] = []

    for x in rooms:
        reason = None
        if not x.exists:
            plan.append(("prune (missing on disk)", x))
            continue
        if x.kind == "gate" and x.nested and x.processes == 0:
            plan.append(("remove nested gate tree", x))
            continue
        if x.kind == "gate":
            continue
        eligible_kind = x.kind == "supergit" or (x.kind == "claude-native" and args.include_native) or (x.kind == "foreign" and args.include_foreign)
        if not eligible_kind:
            if x.expired:
                human.append(f"{x.label} [{x.kind}] — not supergit-owned; pass --include-{'native' if x.kind == 'claude-native' else 'foreign'} to include")
            continue
        if not x.expired and not args.all:
            continue
        if not x.clean:
            reason = "unsaved changes"
        elif x.unpushed:
            reason = f"{x.unpushed} unpushed commit(s)"
        elif x.processes:
            reason = f"{x.processes} live process(es)"
        if reason:
            human.append(f"{x.label} [{x.kind}] — {reason}")
        else:
            plan.append(("remove expired clean room", x))

    # merged branches — ancestry OR squash-merged (we squash, so ancestry alone never matches)
    checked_out = {x.branch for x in rooms if x.branch}
    local_branches = [b.strip().lstrip("* ") for b in git(["branch", "--list"], cwd=repo.library, check=False).splitlines()]
    merged_local = [b for b in local_branches
                    if b and b not in ("main", "master") and not b.startswith("(") and b not in checked_out
                    and is_merged(repo.library, b)]
    merged_remote = []
    if args.remote_branches:
        for line in git(["branch", "-r", "--list", "origin/*"], cwd=repo.library, check=False).splitlines():
            b = line.strip()
            if b == "origin/main" or "->" in b:
                continue
            short = b.split("/", 1)[1]
            if short.split("/")[0] in AGENT_PREFIXES and is_merged(repo.library, b):
                merged_remote.append(short)

    junk = [l[3:] for l in git(["status", "--porcelain", "--untracked-files=normal"], cwd=repo.library, check=False).splitlines()
            if l.startswith("??") and "/" not in l[3:].rstrip("/")]

    r.detail.append(f"🧹 cleanup plan for {repo.name} ({'EXECUTING' if go else 'dry run — add --go to execute'})")
    for action, x in plan:
        r.detail.append(f"   {action}: {x.label} ({x.path})")
    for b in merged_local:
        r.detail.append(f"   delete merged local branch: {b}")
    for b in merged_remote:
        r.detail.append(f"   delete merged remote branch: origin/{b}")
    if not plan and not merged_local and not merged_remote:
        r.detail.append("   nothing to remove")
    if human:
        r.detail.append("   needs a human:")
        r.detail.extend(f"      - {h}" for h in human)
    if junk:
        r.detail.append(f"   untracked files at library root (reported, never deleted): {', '.join(junk[:8])}")

    if go:
        removed = 0
        for action, x in plan:
            if x.exists:
                if x.processes:
                    sh(["pkill", "-f", f"{x.path}/"], check=False)
                git(["worktree", "remove", "--force", str(x.path)], cwd=repo.library, check=False)
            removed += 1
            sc = x.sidecar
            if sc:
                sidecar_path(repo, sc["slug"]).unlink(missing_ok=True)
        git(["worktree", "prune"], cwd=repo.library, check=False)
        for b in merged_local:
            git(["branch", "-d", b], cwd=repo.library, check=False)
        for b in merged_remote:
            sh(["git", "push", "--quiet", "origin", "--delete", b], cwd=repo.library, check=False, timeout=60)
        r.done.append(f"removed {removed} worktree(s), {len(merged_local)} local branch(es), {len(merged_remote)} remote branch(es)")
    else:
        git(["worktree", "prune"], cwd=repo.library, check=False)
        r.done.append("dry run only — registry pruned, nothing removed")
    for h in human[:3]:
        r.decide.append(f"{h} — ship, park, or abandon?")
    return r


def is_merged(library: Path, ref: str, into: str = "origin/main") -> bool:
    """True if `ref` is an ancestor of `into` OR its squashed diff is already in `into`."""
    if sh(["git", "merge-base", "--is-ancestor", ref, into], cwd=library, check=False).returncode == 0:
        return True
    base = git(["merge-base", into, ref], cwd=library, check=False)
    if not base:
        return False
    tree = git(["rev-parse", f"{ref}^{{tree}}"], cwd=library, check=False)
    if not tree:
        return False
    synthetic = git(["commit-tree", tree, "-p", base, "-m", "supergit squash check"], cwd=library, check=False)
    if not synthetic:
        return False
    cherry = git(["cherry", into, synthetic], cwd=library, check=False)
    return cherry.startswith("-")


def verb_where(args) -> Report:
    repo = resolve_project(args.project)
    kw = args.keyword.lower()
    r = Report()
    hits: list[str] = []
    for x in list_rooms(repo, probe=False):
        blob = " ".join([x.label, x.branch or "", json.dumps(x.sidecar or {}, ensure_ascii=False)]).lower()
        if kw in blob:
            hits.append(f"room: {room_line(x)}")
    for b in git(["branch", "-a", "--list", f"*{args.keyword}*"], cwd=repo.library, check=False).splitlines():
        hits.append(f"branch: {b.strip()}")
    if has("gh"):
        proc = sh(["gh", "pr", "list", "--state", "all", "--search", args.keyword, "--json", "number,title,state,url,mergedAt",
                   "--limit", "8"], cwd=repo.library, check=False, timeout=30)
        if proc.returncode == 0:
            for pr in json.loads(proc.stdout or "[]"):
                when = f" merged {pr['mergedAt'][:10]}" if pr.get("mergedAt") else ""
                hits.append(f"PR #{pr['number']} [{pr['state']}{when}] {pr['title']} — {pr['url']}")
    live = git(["log", "origin/main", "-i", f"--grep={args.keyword}", "--oneline", "-8"], cwd=repo.library, check=False)
    for line in live.splitlines():
        hits.append(f"on main (live): {line}")
    r.detail.append(f"🔎 “{args.keyword}” in {repo.name}")
    r.detail.extend(f"   {h}" for h in hits) if hits else r.detail.append("   nothing matches")
    r.done.append(f"{len(hits)} match(es)")
    return r


def verb_brief(args) -> Report:
    r = Report()
    projects = registry_projects()
    if args.project:
        projects = [p for p in projects if p["id"] == args.project or str(p["path"]) == str(expand(args.project))]
    r.detail.append(f"☀️ brief — {now().strftime('%Y-%m-%d %H:%M')} — {len(projects)} project(s)")
    for p in projects:
        try:
            repo = find_repo(p["path"])
        except SupergitError:
            continue
        lib = library_state(repo, fetch=not args.no_fetch)
        rooms = [x for x in list_rooms(repo) if x.kind != "library"]
        stuck = [x for x in rooms if x.kind in ("supergit", "claude-native") and x.expired and (not x.clean or x.unpushed)]
        sweepable = [x for x in rooms if x.kind == "supergit" and x.expired and x.clean and x.unpushed == 0 and x.processes == 0]
        overlaps = find_overlaps(rooms)
        line = f"   {p['id']:<14} lib {lib['behind']}↓/{lib['ahead']}↑"
        if lib["dirty_tracked"]:
            line += f" ⚠️dirty({lib['dirty_tracked']})"
        line += f" · rooms {len(rooms)}"
        if stuck:
            line += f" ({len(stuck)} stuck)"
        if sweepable:
            line += f" · {len(sweepable)} sweepable"
        if overlaps:
            line += f" · ⚠️{len(overlaps)} overlapping"
        ds = deploy_state(repo)
        pushes = direct_pushes(repo) if ds else []
        if ds:
            line += " · " + deploy_summary(ds)
        if pushes:
            line += f" · ⚠️ {len(pushes)} direct push(es) to main"
        prs = []
        if has("gh") and not args.no_fetch:
            proc = sh(["gh", "pr", "list", "--json", "number,title,createdAt,url,statusCheckRollup,isDraft", "--limit", "20"],
                      cwd=repo.library, check=False, timeout=30)
            if proc.returncode == 0:
                prs = json.loads(proc.stdout or "[]")
        if prs:
            line += f" · PRs open {len(prs)}"
        r.detail.append(line)
        for pr in prs:
            age = (now() - parse_iso(pr["createdAt"].replace("Z", "+00:00"))).total_seconds() / 3600
            checks = pr.get("statusCheckRollup") or []
            green = all(c.get("conclusion") in ("SUCCESS", "NEUTRAL", "SKIPPED", None) for c in checks)
            mark = "✅" if green else "❌"
            r.detail.append(f"      PR #{pr['number']} {mark} {age:.0f}h · {pr['title'][:60]}")
            if age > 48 and green and not pr.get("isDraft"):
                r.decide.append(f"{p['id']} PR #{pr['number']} open {age/24:.0f}d, checks green — merge? (`review {pr['number']}`)")
        for x in stuck[:2]:
            r.decide.append(f"{p['id']} room `{x.label}` stuck — ship, park, or abandon?")
        if ds:
            prod = ds["production"]
            if prod and prod["state"] in ("failure", "error"):
                r.decide.append(f"{p['id']}: production build FAILED for {prod['sha'][:7]} — read the log (`audit`), then fix-forward or `undo`?")
            elif ds["burst"] > 1:
                r.decide.append(f"{p['id']}: {ds['burst']} production builds inside 30 min — separate pushes hit main back-to-back; is production on the one you meant? (`audit`)")
            elif ds["live"] and not ds["head_deployed"] and not ds["head_building"]:
                r.decide.append(f"{p['id']}: main is ahead of production and nothing is building — did a build fail silently? (`audit`)")
            if ds["preview_failed"] >= 5:
                r.decide.append(f"{p['id']}: previews failing {ds['preview_failed']} of last {ds['preview_seen']} — read one build log before shipping more")
        for sha, subject in pushes[:2]:
            r.decide.append(f"{p['id']}: `{sha}` landed on main WITHOUT a PR — “{subject[:50]}”. Who pushed it, and should it have been a ship?")
        if sweepable and not stuck:
            r.decide.append(f"{p['id']}: {len(sweepable)} room(s) expired & clean — `clean up`?")
        for a, b, shared in overlaps[:1]:
            r.decide.append(f"{p['id']}: `{a.label}` and `{b.label}` touch {len(shared)} shared file(s) — worth a look before either ships")
        if lib["behind"] and not lib["dirty_tracked"] and not lib["ahead"]:
            r.decide.append(f"{p['id']} library {lib['behind']} behind — `sync`? (yes/no)")
        if lib["dirty_tracked"]:
            r.decide.append(f"{p['id']} library has uncommitted edits — someone worked in the library; move to a room?")
    r.done.append(f"briefed {len(projects)} project(s)")
    return r


def verb_review(args) -> Report:
    repo = resolve_project(args.project)
    if not has("gh"):
        raise SupergitError("GitHub CLI `gh` is required for review")
    r = Report()
    proc = sh(["gh", "pr", "view", str(args.pr), "--json",
               "number,title,url,author,baseRefName,headRefName,headRefOid,mergeable,mergeStateStatus,isDraft,additions,deletions,changedFiles,files,body,statusCheckRollup,createdAt"],
              cwd=repo.library, timeout=60)
    pr = json.loads(proc.stdout)
    gate = read_ship_gate(repo.library)
    checks = pr.get("statusCheckRollup") or []
    failing = [c for c in checks if c.get("conclusion") not in ("SUCCESS", "NEUTRAL", "SKIPPED", None)]
    behind = pr.get("mergeStateStatus") == "BEHIND"
    ds = deploy_state(repo)
    preview = preview_for(ds, pr.get("headRefOid", ""))
    r.data = {"pr": pr, "gate": gate, "behind": behind, "failing_checks": failing, "preview": preview}
    r.detail.append(f"🔍 PR #{pr['number']} — {pr['title']}")
    r.detail.append(f"   {pr['url']}")
    r.detail.append(f"   by {pr['author'].get('login')} · {pr['headRefName']} → {pr['baseRefName']} · +{pr['additions']} −{pr['deletions']} in {pr['changedFiles']} file(s)")
    r.detail.append(f"   mergeable: {pr.get('mergeable')} · state: {pr.get('mergeStateStatus')} · draft: {pr.get('isDraft')}")
    r.detail.append(f"   checks: {len(checks)} ({len(failing)} failing)" + (" · CI may be billing-blocked — the local ship gate is the real check" if not checks else ""))
    if ds:
        if preview and preview["state"] == "success":
            r.detail.append(f"   preview: ✅ {preview.get('url')}  ← look here before merging")
        elif preview and preview["state"] in ("failure", "error"):
            r.detail.append(f"   preview: ❌ build failed — {preview.get('url')} (a preview-only failure is not proof the code is broken; read the log)")
        elif preview:
            r.detail.append("   preview: ⏳ still building — check again in a few minutes")
        else:
            r.detail.append("   preview: none recorded for this commit yet")
    if gate.get("merge_deploys"):
        r.detail.append(f"   ⚠️ merging deploys to {gate['merge_deploys']}")
    r.detail.append("   files:")
    for f in pr.get("files", [])[:25]:
        r.detail.append(f"      {f['path']} (+{f['additions']} −{f['deletions']})")
    r.detail.append("")
    r.detail.append("   PR body:")
    r.detail.extend(f"      {l}" for l in (pr.get("body") or "(empty)").splitlines()[:60])
    r.detail.append("")
    r.detail.append("   → agent: write the plain-language walkthrough now: what changed · what was verified · risk · “safe to merge: yes/no, because…”")
    r.done.append("facts gathered — the walkthrough above is the agent's job, not the script's")
    if failing:
        r.decide.append("checks are failing — do not merge yet")
    elif behind:
        r.decide.append("branch is behind main — `merge` will rebase it first; proceed? (yes/no)")
    else:
        r.decide.append(f"merge PR #{pr['number']}? (yes/no)")
    return r


def verb_merge(args) -> Report:
    repo = resolve_project(args.project)
    if not has("gh"):
        raise SupergitError("GitHub CLI `gh` is required for merge")
    r = Report()
    gate = read_ship_gate(repo.library)
    pr = json.loads(sh(["gh", "pr", "view", str(args.pr), "--json",
                        "number,title,url,headRefName,mergeable,mergeStateStatus,isDraft,statusCheckRollup,mergedAt"],
                       cwd=repo.library, timeout=60).stdout)
    if pr.get("mergedAt"):
        r.done.append(f"PR #{pr['number']} is already merged")
        return r
    checks = pr.get("statusCheckRollup") or []
    failing = [c for c in checks if c.get("conclusion") not in ("SUCCESS", "NEUTRAL", "SKIPPED", None)]
    if failing:
        raise SupergitError(f"PR #{pr['number']} has failing checks — not merging")
    if pr.get("isDraft"):
        raise SupergitError(f"PR #{pr['number']} is a draft — not merging")
    deploy = gate.get("merge_deploys")
    if not args.yes:
        r.detail.append(f"🔒 merge PR #{pr['number']} — {pr['title']}")
        r.detail.append(f"   {pr['url']}")
        r.detail.append(f"   ⚠️ merging deploys to {deploy}." if deploy else "   Check whether merging deploys this project.")
        r.detail.append(f"   undo later: `supergit undo {pr['number']}`")
        r.decide.append(f"confirm merge of PR #{pr['number']}? (yes/no) → rerun with --yes")
        r.done.append("nothing merged")
        return r

    if pr.get("mergeStateStatus") == "BEHIND":
        room = next((x for x in list_rooms(repo, probe=False) if x.branch == pr["headRefName"]), None)
        work = room.path if room else None
        temp = None
        if not work:
            temp = Path(tempfile.mkdtemp(prefix="supergit-merge-"))
            git(["worktree", "add", "--force", str(temp), pr["headRefName"]], cwd=repo.library)
            work = temp
        sh(["git", "fetch", "--quiet", "origin"], cwd=work, timeout=60)
        rb = sh(["git", "rebase", "origin/main"], cwd=work, check=False, timeout=300)
        if rb.returncode != 0:
            sh(["git", "rebase", "--abort"], cwd=work, check=False)
            if temp:
                git(["worktree", "remove", "--force", str(temp)], cwd=repo.library, check=False)
            raise SupergitError("branch is behind main and the rebase hit a conflict — nothing merged, nothing lost")
        ok, note = run_gate(work, gate, False)
        if not ok:
            if temp:
                git(["worktree", "remove", "--force", str(temp)], cwd=repo.library, check=False)
            raise SupergitError(f"gate failed after rebase: {note}")
        sh(["git", "push", "--force-with-lease", "origin", f"HEAD:refs/heads/{pr['headRefName']}"], cwd=work, timeout=1800)
        if temp:
            git(["worktree", "remove", "--force", str(temp)], cwd=repo.library, check=False)
        r.done.append("branch rebased onto main, gate green, pushed")

    sh(["gh", "pr", "merge", str(pr["number"]), "--squash", "--delete-branch"], cwd=repo.library, timeout=300)
    r.done.append(f"PR #{pr['number']} merged (squash), branch deleted")
    if deploy:
        r.done.append(f"→ this deploys to {deploy}")
        r.waiting.append(f"{deploy} build for the merge commit — `brief` shows `prod ✅` once it is live; `undo {pr['number']}` if it goes wrong")

    # library sync
    try:
        sync_r = verb_sync(argparse.Namespace(project=str(repo.library)))
        r.done.extend(sync_r.done)
        r.decide.extend(sync_r.decide)
    except SupergitError as e:
        r.decide.append(f"library sync failed: {e}")

    # close the room that shipped it
    for x in list_rooms(repo):
        if x.kind == "supergit" and x.sidecar and (x.sidecar.get("shipped") or {}).get("pr", "").endswith(f"/{pr['number']}"):
            if x.clean and x.exists:
                git(["worktree", "remove", "--force", str(x.path)], cwd=repo.library, check=False)
                sidecar_path(repo, x.sidecar["slug"]).unlink(missing_ok=True)
                r.done.append(f"room `{x.label}` closed")
            else:
                r.decide.append(f"room `{x.label}` still has unsaved changes — abandon it? (yes/no)")
    git(["worktree", "prune"], cwd=repo.library, check=False)
    return r


def verb_undo(args) -> Report:
    repo = resolve_project(args.project)
    if not has("gh"):
        raise SupergitError("GitHub CLI `gh` is required for undo")
    r = Report()
    pr = json.loads(sh(["gh", "pr", "view", str(args.pr), "--json", "number,title,mergeCommit,mergedAt,url"],
                       cwd=repo.library, timeout=60).stdout)
    if not pr.get("mergedAt"):
        raise SupergitError(f"PR #{pr['number']} is not merged — nothing to undo (close it instead)")
    sha = (pr.get("mergeCommit") or {}).get("oid")
    if not sha:
        raise SupergitError("could not find the merge commit for this PR")
    if not args.yes:
        r.detail.append(f"↩️ undo PR #{pr['number']} — {pr['title']} (merge {sha[:8]})")
        r.detail.append("   this opens a *revert PR*; production changes only when that revert PR is merged")
        r.decide.append(f"open the revert PR for #{pr['number']}? (yes/no) → rerun with --yes")
        r.done.append("nothing changed")
        return r
    start = verb_start(argparse.Namespace(project=str(repo.library), slug=f"undo-pr{pr['number']}",
                                          task=f"revert PR #{pr['number']}: {pr['title']}", ttl=DEFAULT_TTL_HOURS,
                                          grant_ship=True, no_deps=True, force=True))
    room = Path(start.data["path"])
    parents = git(["rev-list", "--parents", "-n", "1", sha], cwd=room).split()
    rev = ["revert", "--no-edit"] + (["-m", "1", sha] if len(parents) > 2 else [sha])
    proc = sh(["git", *rev], cwd=room, check=False)
    if proc.returncode != 0:
        sh(["git", "revert", "--abort"], cwd=room, check=False)
        raise SupergitError(f"revert hit a conflict in room `{start.data['slug']}` — left for a human")
    os.chdir(room)
    ship = verb_ship(argparse.Namespace(message=f"revert: {pr['title']}", trailer=None, skip_gate=False, no_pr=False,
                                        title=f"revert: {pr['title']}"[:70], body_file=None,
                                        summary=f"Reverts PR #{pr['number']} ({pr['title']}). Merging this puts things back the way they were before that PR.",
                                        verified=None, risk="Low — a straight revert of one merged PR"))
    r.done.extend(start.done[:1] + ship.done)
    r.decide.append(f"merge the revert PR to complete the undo → `supergit merge <number> --yes`")
    return r


def verb_abandon(args) -> Report:
    repo = find_repo()
    r = Report()
    target = Path(args.path).resolve() if args.path else repo.cwd_top
    if target == repo.library:
        raise SupergitError("that is the library — abandon only works on rooms")
    rooms = {x.path: x for x in list_rooms(repo)}
    x = rooms.get(target)
    if not x:
        raise SupergitError(f"not a registered room: {target}")
    stat = git(["diff", "--stat"], cwd=target, check=False)
    untracked = git(["ls-files", "--others", "--exclude-standard"], cwd=target, check=False).splitlines()
    notes = (x.sidecar or {}).get("notes", [])
    r.detail.append(f"🗑️ abandon room `{x.label}` ({target})")
    if stat:
        r.detail.append("   unsaved changes:")
        r.detail.extend(f"      {l}" for l in stat.splitlines()[-12:])
    if untracked:
        r.detail.append(f"   untracked files: {len(untracked)}")
    if x.unpushed:
        r.detail.append(f"   ⚠️ {x.unpushed} commit(s) never pushed — they will be lost")
    if notes:
        r.detail.append("   notes (printed once, then gone):")
        r.detail.extend(f"      - {n['text']}" for n in notes)
    if not args.yes:
        r.decide.append("throw all of this away? (yes/no) → rerun with --yes")
        r.done.append("nothing removed")
        return r
    if x.processes:
        sh(["pkill", "-f", f"{target}/"], check=False)
    os.chdir(repo.library)
    git(["worktree", "remove", "--force", str(target)], cwd=repo.library)
    if x.branch:
        on_remote = git(["ls-remote", "--heads", "origin", x.branch], cwd=repo.library, check=False)
        if not on_remote:
            git(["branch", "-D", x.branch], cwd=repo.library, check=False)
            r.done.append(f"branch {x.branch} deleted (was never pushed)")
        else:
            r.done.append(f"branch {x.branch} kept on origin")
    git(["worktree", "prune"], cwd=repo.library, check=False)
    if x.sidecar:
        sidecar_path(repo, x.sidecar["slug"]).unlink(missing_ok=True)
    r.done.append(f"room `{x.label}` abandoned")
    return r


def verb_audit(args) -> Report:
    repo = resolve_project(args.project)
    r = Report()
    lib = repo.library
    findings: list[tuple[str, str]] = []

    def check(ok: bool, good: str, bad: str, level: str = "WARN"):
        findings.append(("PASS", good) if ok else (level, bad))

    agents = lib / "AGENTS.md"
    claude = lib / "CLAUDE.md"
    check(agents.exists() or claude.exists(), "AGENTS.md/CLAUDE.md present", "no AGENTS.md or CLAUDE.md — run `supergit init`", "FAIL")
    rules_text = "".join(f.read_text(errors="replace") for f in (agents, claude) if f.exists())
    check("## Ship gate" in rules_text, "`## Ship gate` section present", "no `## Ship gate` section — ship will fall back to package.json defaults")
    check(re.search(r"push to main|no branches", rules_text, re.I) is None, "no 'push to main' rule in project rules", "project rules still say 'push to main' — replace with the ship model")

    ignored = sh(["git", "check-ignore", "-q", f"{ROOMS_DIR}/x"], cwd=lib, check=False).returncode == 0
    check(ignored, f"{ROOMS_DIR} is ignored", f"{ROOMS_DIR} is not gitignored (rooms would show as untracked) — `start` adds it to .git/info/exclude")
    tracked_env = git(["ls-files", ".env", ".env.local", ".env.production"], cwd=lib, check=False)
    check(not tracked_env, "no .env files tracked", f"env files are TRACKED: {tracked_env.replace(chr(10), ', ')}", "FAIL")
    big = []
    for line in git(["ls-tree", "-r", "-l", "HEAD"], cwd=lib, check=False).splitlines():
        parts = line.split(None, 4)
        if len(parts) == 5 and parts[3].isdigit() and int(parts[3]) > 5_000_000:
            big.append(f"{parts[4]} ({int(parts[3]) // 1_000_000}MB)")
    check(not big, "no tracked files over 5MB", f"large tracked files: {', '.join(big[:5])}")
    for folder in ("drafts", "posted"):
        d = lib / folder
        if d.exists():
            bad = [p.name for p in d.iterdir() if not p.name.startswith(".") and not re.match(r"^\d{4}-\d{2}-\d{2}_", p.name)]
            check(not bad, f"{folder}/ names use YYYY-MM-DD_", f"{folder}/ entries without date prefix: {', '.join(bad[:5])}")
    hooks_path = git(["config", "core.hooksPath"], cwd=lib, check=False)
    has_prepush = (repo.git_dir / "hooks" / "pre-push").exists() or (hooks_path and (lib / hooks_path / "pre-push").exists())
    pkg = lib / "package.json"
    if pkg.exists() and "hooks:install" in pkg.read_text():
        check(bool(has_prepush), "pre-push hook installed", "pre-push hook missing — run `npm run hooks:install`")
    reg = next((p for p in registry_projects() if p["path"] == lib), None)
    check(reg is not None, "listed in config.json", "not in supergit config.json → projects — `supergit init --register`")
    if reg and reg.get("origin"):
        origin = git(["remote", "get-url", "origin"], cwd=lib, check=False)
        check(origin.rstrip("/").removesuffix(".git") == reg["origin"].rstrip("/").removesuffix(".git"),
              "origin matches config", f"origin mismatch: repo={origin} config={reg['origin']}")
    state = library_state(repo, fetch=not args.no_fetch)
    check(state["dirty_tracked"] == 0, "library is clean", f"library has {state['dirty_tracked']} modified file(s) — it should be read-only")
    check(state["behind"] == 0, "library current with origin/main", f"library {state['behind']} behind origin/main — `sync`")
    check(not (state["ahead"] and state["behind"]), "library not diverged", f"library DIVERGED: {state['behind']} remote-only, {state['ahead']} local-only", "FAIL")
    rooms = [x for x in list_rooms(repo) if x.kind != "library"]
    nested = [x for x in rooms if x.nested]
    check(not nested, "no nested gate trees", f"{len(nested)} nested worktree(s) — `cleanup --go`")
    check(len(rooms) <= 8, f"{len(rooms)} room(s)", f"{len(rooms)} rooms — `cleanup`")

    # deploy — what the host actually did with main, and what reached main without review
    ds = deploy_state(repo)
    pushes: list[tuple[str, str]] = []
    if ds:
        prod = ds["production"]
        check(not (prod and prod["state"] in ("failure", "error")), "last production build succeeded",
              f"last production build FAILED ({prod['sha'][:7] if prod else '?'}) — {prod.get('url') if prod else ''}", "FAIL")
        check(ds["burst"] <= 1, "one production build per half hour",
              f"{ds['burst']} production builds inside 30 min — pushes to main are landing back-to-back; the last to finish wins")
        check(ds["head_deployed"] or ds["head_building"], "production is on origin/main",
              f"production is on {ds['live']['sha'][:7] if ds['live'] else '?'} but main has been at {ds['head'][:7]} for {ds['head_age_min'] or 0:.0f} min — the build for it failed or never started")
        check(ds["preview_failed"] < 3, f"previews healthy ({ds['preview_failed']}/{ds['preview_seen']} failed)",
              f"previews failing: {ds['preview_failed']} of the last {ds['preview_seen']} — read one build log; a preview-only failure is usually an env var missing from the Preview environment")
        pushes = direct_pushes(repo)
        check(not pushes, "every commit on main in the last 24h came through a PR",
              f"{len(pushes)} commit(s) reached main WITHOUT a PR in the last 24h: " + "; ".join(f"{s} “{t[:40]}”" for s, t in pushes[:4]))
    elif deploy_capable(repo):
        check(False, "", "host deployments unreadable — `gh` missing, origin not GitHub, or the integration records nothing")

    r.detail.append(f"🩺 audit — {repo.name}")
    for level, msg in findings:
        if level != "PASS":
            r.detail.append(f"   {level}  {msg}")
    if ds:
        r.detail.append("")
        live = ds["live"]
        r.detail.append(f"🚀 deploy — production {('on ' + live['sha'][:7] + ' · ' + (live.get('url') or '')) if live else 'no successful build recorded'} · main {ds['head'][:7]}")
        for x in ds["rows"][:6]:
            mark = {"success": "✅", "failure": "❌", "error": "❌"}.get(x["state"], "⏳")
            r.detail.append(f"   {mark} {x['env']:<10} {x['sha'][:7]}  {x['state']:<11} {x.get('url') or ''}")
    passed = sum(1 for l, _ in findings if l == "PASS")
    r.done.append(f"{passed} passed, {sum(1 for l, _ in findings if l == 'FAIL')} failed, {sum(1 for l, _ in findings if l == 'WARN')} warnings")
    fails = [m for l, m in findings if l == "FAIL"]
    for m in fails[:3]:
        r.decide.append(m)
    r.data = {"findings": findings}
    return r


def verb_init(args) -> Report:
    r = Report()
    target = expand(args.path)
    if not (target / ".git").exists():
        raise SupergitError(f"{target} is not a git repository — `git init` first")
    template = TEMPLATE_DIR / "AGENTS.md"
    agents = target / "AGENTS.md"
    if not agents.exists():
        body = template.read_text() if template.exists() else ""
        body = body.replace("<project>", target.name)
        body += "\n## Ship gate\n\n```bash\n# commands supergit runs before pushing; leave empty to rely on package.json defaults\n```\n\n- hook: pre-push   # uncomment if the pre-push hook already runs build+tests\n- merge-deploys: production   # uncomment if merging to main deploys\n"
        agents.write_text(body)
        r.done.append("AGENTS.md created from template (with a Ship gate section to fill in)")
    elif "## Ship gate" not in agents.read_text():
        with agents.open("a") as f:
            f.write("\n## Ship gate\n\n```bash\n```\n")
        r.done.append("added a `## Ship gate` section to AGENTS.md")
    claude = target / "CLAUDE.md"
    if not claude.exists():
        claude.symlink_to("AGENTS.md")
        r.done.append("CLAUDE.md → AGENTS.md symlink created")
    gi = target / ".gitignore"
    gi_text = gi.read_text() if gi.exists() else ""
    if ROOMS_DIR not in gi_text:
        gi.write_text(gi_text.rstrip("\n") + f"\n{ROOMS_DIR}/\n")
        r.done.append(f"{ROOMS_DIR}/ added to .gitignore")
    pkg = target / "package.json"
    if pkg.exists() and "hooks:install" in pkg.read_text():
        proc = sh(["npm", "run", "hooks:install"], cwd=target, check=False, timeout=120)
        r.done.append("git hooks installed" if proc.returncode == 0 else "hooks:install failed — run it by hand")
    origin = git(["remote", "get-url", "origin"], cwd=target, check=False)
    entry = {"id": slugify(target.name), "name": target.name,
             "path": str(target).replace(str(Path.home()), "~"), "origin": origin or None}
    if args.register:
        data = load_config()
        projects = data.setdefault("projects", [])
        if any(p.get("id") == entry["id"] or expand(p.get("path", "")) == target for p in projects):
            r.done.append("already listed")
        else:
            projects.append(entry)
            CONFIG_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
            r.done.append("added to supergit config.json → projects")
    else:
        r.detail.append("config.json entry (add with --register):")
        r.detail.append(json.dumps(entry, ensure_ascii=False, indent=2))
    if not origin:
        r.decide.append("no GitHub remote — create one? (that's a separate, named authorization)")
    return r


def verb_help(args) -> Report:
    r = Report()
    r.detail.append(HELP.strip())
    r.done.append("that's the verb table; definitions live in README.md")
    return r


HELP = """
supergit — one library (read-only main), many rooms (one per task), ship = branch + PR, only the owner merges.

Daily        brief [project]           morning page across all registered projects
             status [project]          every room of one project
             where <keyword>           did X ship? which branch/PR/room has it?

Task         start <slug> [--task ..] [--grant-ship] [--ttl 12]     new room from origin/main
             note "<text>"             keep a thought on this room (surfaces at ship/finish)
             label "<text>"            name the room you are in (a harness-made worktree is adopted on first use)
             park                      WIP commit + push branch; room stays
             ship [-m ..] [--summary ..] [--verified ..] [--risk ..] [--no-pr]    commit → gate → push → PR
             finish [--keep-branch] [--dry-run]                     close a clean, shipped room

Decide       review <pr>               facts for a plain-language walkthrough
             merge <pr> [--yes]        gate → rebase if behind → squash-merge → sync → close room
             undo <pr> [--yes]         open a revert PR
             abandon [path] [--yes]    throw a room away on purpose

Keep clean   sync [project]            fast-forward the library (refuses if dirty)
             cleanup [project] [--go] [--all] [--include-native] [--include-foreign] [--remote-branches]
             audit [project]           structure + git health, report only
             init <path> [--register]              scaffold AGENTS.md, Ship gate, ignore, hooks, config entry

Every verb accepts --json. Tier 2 verbs need --yes after the owner's explicit word.
"""


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="supergit", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--version", action="version", version=f"supergit {VERSION}")
    sub = p.add_subparsers(dest="verb", required=True)

    def add(name, fn, **kw):
        sp = sub.add_parser(name, **kw)
        sp.set_defaults(fn=fn)
        return sp

    s = add("brief", verb_brief); s.add_argument("project", nargs="?"); s.add_argument("--no-fetch", action="store_true")
    s = add("status", verb_status); s.add_argument("project", nargs="?"); s.add_argument("--no-fetch", action="store_true")
    s = add("where", verb_where); s.add_argument("keyword"); s.add_argument("--project")
    s = add("start", verb_start); s.add_argument("slug"); s.add_argument("--task"); s.add_argument("--project")
    s.add_argument("--grant-ship", dest="grant_ship", action="store_true"); s.add_argument("--ttl", type=int, default=DEFAULT_TTL_HOURS)
    s.add_argument("--no-deps", action="store_true"); s.add_argument("--force", action="store_true")
    s = add("note", verb_note); s.add_argument("text")
    s = add("label", verb_label); s.add_argument("text")
    s = add("park", verb_park); s.add_argument("-m", "--message"); s.add_argument("--trailer")
    s = add("ship", verb_ship); s.add_argument("-m", "--message"); s.add_argument("--title"); s.add_argument("--trailer")
    s.add_argument("--summary"); s.add_argument("--verified"); s.add_argument("--risk"); s.add_argument("--body-file")
    s.add_argument("--no-pr", action="store_true"); s.add_argument("--skip-gate", action="store_true")
    s = add("finish", verb_finish); s.add_argument("--keep-branch", action="store_true"); s.add_argument("--dry-run", action="store_true")
    s = add("review", verb_review); s.add_argument("pr"); s.add_argument("--project")
    s = add("merge", verb_merge); s.add_argument("pr"); s.add_argument("--yes", action="store_true"); s.add_argument("--project")
    s = add("undo", verb_undo); s.add_argument("pr"); s.add_argument("--yes", action="store_true"); s.add_argument("--project")
    s = add("abandon", verb_abandon); s.add_argument("path", nargs="?"); s.add_argument("--yes", action="store_true")
    s = add("sync", verb_sync); s.add_argument("project", nargs="?")
    s.add_argument("--reset-equivalent", action="store_true", help="move a clean library onto origin/main when every local-only commit already exists there in equivalent form")
    s = add("cleanup", verb_cleanup); s.add_argument("project", nargs="?"); s.add_argument("--go", action="store_true")
    s.add_argument("--all", action="store_true", help="include rooms not yet past TTL"); s.add_argument("--include-native", action="store_true")
    s.add_argument("--include-foreign", action="store_true"); s.add_argument("--remote-branches", action="store_true")
    s = add("audit", verb_audit); s.add_argument("project", nargs="?"); s.add_argument("--no-fetch", action="store_true")
    s = add("init", verb_init); s.add_argument("path"); s.add_argument("--register", action="store_true")
    add("help", verb_help)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = args.fn(args)
    except SupergitError as e:
        report = Report(done=["stopped — nothing changed" if "nothing" in str(e).lower() else "stopped"],
                        decide=[f"{e}"], detail=[f"⛔ {e}"])
        print(report.render(args.json))
        return 1
    print(report.render(args.json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
