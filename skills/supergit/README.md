# supergit

**A proactive git steward for people who build with AI coding agents but are not engineers.**

You say *start on X · ship it · is PR 42 safe? · merge it · done · clean up*. The agent keeps your code, your database and your deployments clean — and you never type a git command.

It works with Claude Code, Codex, Cursor, or any agent that can run a script and read a `SKILL.md`. One Python file, no dependencies.

**[Read the interactive guide →](https://claude.ai/code/artifact/5e0b8be4-14d7-438f-b7a1-92b8656bdce7)** — when to use it, what to say, and the full term sheet below, in English and Traditional Chinese.

## Install

**With GitHub CLI 2.90+** (`gh --version` to check; `brew upgrade gh` or your package manager if older): `gh skill install` implements the open [Agent Skills spec](https://agentskills.io) this repo already follows, and pins the install to a git SHA — an upgrade is something you ask for, not something that happens under you.

```bash
gh skill install ekcheungAI/ekSkills supergit --agent claude-code   # or: codex, cursor
```

**Otherwise**, install it by hand — same result, no `gh` version requirement:

```bash
# 1. put the skill where your agent reads skills (Claude Code shown; Codex: ~/.codex/skills)
git clone https://github.com/ekcheungAI/ekSkills.git
ln -s "$(pwd)/ekSkills/skills/supergit" ~/.claude/skills/supergit

# 2. tell it about a project (repeat per project)
~/.claude/skills/supergit/scripts/supergit init ~/code/my-app --register

# 3. optional, Claude Code only: hard guards (brief on session start, refuse edits in the library)
#    merge hooks/claude-settings.snippet.json into ~/.claude/settings.json
```

Either way, `init` writes an `AGENTS.md` with the eight agent rules (see §8 below) and a `## Ship gate` section, adds `.claude/worktrees/` to `.gitignore`, and lists the project in `config.json`. Then say **"start on …"** to your agent.

> **The one rule:** the library is not a desk. Every problem this skill prevents — lost work, "which version is live?", agents overwriting each other, 100 stale copies, a database nobody can describe — comes from people and agents working directly in the main folder.

## Verbs at a glance

```
supergit brief                       morning page across all projects
supergit status | where <kw>         every room of a project · find a feature
supergit start <slug> --task "…" [--grant-ship]
supergit note "…" | park | ship [--summary … --verified … --risk …] | finish
supergit review N | merge N --yes | undo N --yes | abandon --yes
supergit sync | cleanup [--go] | audit | init <path> [--register]
node scripts/migrate.mjs <YYYYMMDDHHMMSS_name.sql> [--check|--dry-run]
```

Every verb accepts `--json`. Every reply ends **Done / Waiting / You decide**.

---
## 0. The whole idea in one picture

```
 LIBRARY        your project's main folder. Read-only. Always current. Nobody edits here.
 ROOM           a private copy for ONE task. Opened from the latest library. Deleted when done.
 SHIP           the only way work leaves a room: a branch and a pull request (PR).
 MERGE          your decision to accept a PR into the library. Often this deploys.
 STEWARD        the agent role that opens rooms, ships, sweeps, and never merges on its own.
```

**The library is not a desk.** Every problem this vocabulary prevents — lost work, "which version is live?", agents overwriting each other, 100 stale copies, a database nobody can describe — comes from people and agents working directly in the main folder. Stop that, and the rest follows.

---

## 1. Nouns — the things

| Term | Plain meaning | The git/infra word |
|---|---|---|
| **Library** | The main folder of a project. Read-only. Always matches what's on GitHub. | main checkout, `main` branch |
| **Room** | One task's private copy of the project. Starts from the latest library. Removed when the task ends. | worktree |
| **Branch** | The named line of work a room writes to. Lives on GitHub once shipped. | branch |
| **PR** | A request to put a branch into the library, with a plain-language description you can judge. | pull request |
| **Gate** | The build and tests that must pass before anything ships. Each project declares its own. | CI, pre-push hook |
| **Ship** | Save → run the gate → push the branch → open the PR. Runs in the background. | commit + push + `gh pr create` |
| **Merge** | Accepting a PR into the library. **Check whether merging deploys before you say it.** | squash-merge |
| **Sync** | Bring the library up to the latest merged state. Safe by construction — it can never lose work. | fast-forward |
| **Park** | Save work-in-progress to its branch and pause. The room stays. | WIP commit + push |
| **Note** | A thought you want kept but not acted on now. Surfaces later as "follow-ups". | — |
| **Label** | The one name a piece of work goes by: on the room, on the session, and as a `Supergit-Room:` trailer on every commit it ships. `label "…"` sets it — a harness-made worktree (Claude Code opens its own per session) becomes a room the first time it's labelled. | sidecar `task` |
| **Direct push** | A commit that reached the library's main branch without a PR — nothing reviewed it, nothing gated it. `audit` lists any from the last 24h; `brief` counts them. | push to `main` |
| **Rescue branch** | A backup branch made before a room is removed, so nothing is ever lost. | `rescue/*` |
| **Foreign room** | A room the steward didn't create. Reported, never touched unless you say so. | — |
| **TTL** | How long an idle, clean, shipped room may sit before it is swept. Dirty rooms are never swept. | time-to-live |
| **Ledger** | The database's own record of which migrations have been applied. | `schema_migrations` |
| **Migration** | One file describing one change to the database. Its filename carries a timestamp. | SQL migration |
| **Preview / Production** | A build of a branch for looking at, vs. the live site. Both cost build minutes. | deployment target |
| **You decide** | The last block of every steward reply: at most three items, one-word answers. | — |

---

## 2. Authority — who may do what

A steward is instructions, not a permission source. Authority comes from you.

| Tier | Operations | What unlocks it |
|---|---|---|
| **0 — Always** | look (status, brief, where), open a room, note, sync, audit, sweep *its own* expired clean shipped rooms, build, test | nothing — the agent just does it |
| **1 — Per task** | ship, park | you say "ship it" / "park it", or you granted it when the task started |
| **2 — Named, every time** | merge, undo, abandon a dirty room, touch the library, rewrite history, delete a branch with unpushed work, apply a database migration, deploy | you name the exact PR, file or room, and say yes |

Anything not on this table is Tier 2.

---

## 3. Verbs — four families, sixteen words

You will really only say eight: *start · note · ship · done · what's the state · is it safe · merge it · clean up.*

### Daily — know where you are
| Verb | Does | You say |
|---|---|---|
| `brief` | Morning page across all projects: PRs waiting, rooms stuck, libraries behind, expired rooms a cleanup would sweep, any pair of live rooms editing the same files, and — on projects with a host — whether production runs what's on main, two production builds landing too close together, and how many previews are failing | "morning", "what's waiting" |
| `status` | Every room of one project: who, what, age, clean/dirty, shipped or not, plus any file-level overlap between rooms with unshipped work | "what's the state", "why is this slow" |
| `where` | Finds a feature: which room, branch, PR; merged or not; live or not | "did X ship?", "is X live?" |

### Task — the daily loop
| Verb | Does | You say |
|---|---|---|
| `start` | Opens a room from the latest library; warns if a related room exists | "start on X" |
| `start --grant-ship` | Same, plus permission to ship when the gate is green — no round-trip later | "start on X and ship it when green" |
| `note` | Keeps a thought on the room | "note this", "also we should…" |
| `park` | Saves progress to the branch, room stays | "park it", "put this aside" |
| `ship` | Commit → gate → push branch → PR, **in the background** | "ship it", "push" |
| `finish` | Closes a clean, shipped room. Refuses otherwise and offers ship / park / abandon | "done", "wrap up" |
| `label` | Names the room you're in — and adopts a harness-made worktree as a room the first time it's used | "call this X", "what is this room for" |

### Decide — only you
| Verb | Does | You say |
|---|---|---|
| `review` | Plain-language walkthrough of a PR: what changed, what was verified, risk, "safe to merge: yes/no because…" | "is PR 42 safe?" |
| `merge` | Gate green → rebase if behind → merge → sync library → close room. Warns if it deploys. | "merge it" (with a number) |
| `undo` | Opens a revert PR for a merged PR. Never rewrites history. | "undo that", "roll back" |
| `abandon` | Throws a room away on purpose, including unsaved work. Shows the diff first. | "scrap this", "start over" |

### Keep clean — structure and hygiene
| Verb | Does | You say |
|---|---|---|
| `sync` | Library ← latest. Refuses if the library is dirty and says who/what. | "sync", "get latest" |
| `cleanup` | Dry run first. Sweeps expired clean rooms, deletes merged branches, flags junk. | "clean up", "too many branches" |
| `audit` | Structure + git + database + deploy health. Reports; never moves or deletes files. | "is this organised?", "check my setup" |
| `init` | Sets a new project up the same way every time (rules file, gate, ignores, hooks) | "set up a new project" |
| `migrate` | Applies ONE database migration file, with the file's timestamp as the ledger version, in one transaction. `--check` runs it and rolls back. | "apply this migration" |

---

## 4. The reply contract — what every steward answer ends with

```
✅ Done        one line per thing that happened
⏳ Waiting     what runs in the background and how you'll hear back
❓ You decide  at most 3 items, each answerable with one word — or "nothing"
```

No commit hashes, refs or file paths in those blocks unless you ask for details. If an agent picks the wrong verb, you see it in one line and redirect.

---

## 5. Ambiguity rules — when your words could mean two things

| You say | It could mean | The steward does |
|---|---|---|
| "clean up" | rooms? branches? files? | dry run, shows the plan, asks: go / rooms only / branches only |
| "deploy" | merge a PR — or a manual deploy command | asks which; never runs a manual deploy from the steward |
| "push" | ship — or push to main | always ship. Pushing to main is not a word the steward knows. |
| "commit" | commit only — or ship | ship if a grant exists; otherwise commit and ask "ship it?" |
| "done" | finish this room — or done for the day | finish the current room; brief if there is none |
| "remember this" | a note — or the agent's memory | a note, and says so |
| "merge" with no number | — | lists open PRs with one-liners; never picks one |
| "apply the migration" with no file | — | lists pending files; never picks one |
| "show me on preview" | — | ships the branch; the host builds a preview automatically, `review N` shows the link |
| "put it live" (with a PR number) | — | `merge N` — production is reached only by merging, never by a push |

---

## 6. The database layer — the part everyone gets wrong

Three things can drift apart: **the files** in the repo, **the ledger** in the database, and **the live schema**. When they do, nobody can say from the repo what is actually in production.

**How drift happens:** an agent writes a migration file with one timestamp, then applies it through a tool that stamps its *own* timestamp. Same change, two version numbers. Or a change is applied in a SQL editor and no file is ever written. Or a file is written and never applied, and the code that needs it ships anyway.

**The rules that stop it:**
1. **One path applies migrations.** `migrate <file>` — the file's timestamp becomes the ledger version, and the DDL and the ledger row commit together or not at all. Agents never call the raw apply tool.
2. **"Not in the ledger" does not mean "not in production."** Always probe the object: does the table / column / function exist?
3. **Never bulk-push migrations** (`db push`) against a ledger you don't trust. It will replay things that already exist, and the ones that don't error are the dangerous ones.
4. **A migration in a PR is flagged loudly:** *merging does NOT apply it; applying is a separate, named step.*
5. **Baseline before you enforce.** If the ledger is already wrong, reconcile it first (back it up in-database, re-key rows whose SQL provably matches the file, recover production-only changes into files), then turn rule 1 on.

**Signs you have this problem:** a feature's button errors with "relation does not exist"; a table has zero rows ever; a settings column silently comes back empty; the same migration name appears twice in the ledger.

---

## 7. The deploy layer — preview vs. production

supergit reads the host's actual deployment state through GitHub's own deployments API (`gh api repos/…/deployments`) — no platform token needed, and it works for any host (Vercel, Netlify, …) that reports deployments to GitHub. This shows up automatically:

- **`brief`** adds a phrase per project: `prod ✅` when production is running what's on main, `prod ⏳` while a build is presumably in flight, `prod ❌` on a failed build, `prod ⚠️ N builds in 30 min` when pushes landed close enough together to race, plus `previews ❌ N/M` and a count of commits that reached main without a PR in the last 24h.
- **`audit`** turns those into findings, plus the last several deployments with their outcomes and links.
- **`review N`** shows that PR's own preview build — built, failed, or still going — so you look at the actual thing before merging, not just a green checkmark.
- **`ship`** tells you a preview is coming; **`merge`** tells you production is building and how to undo.

The things reading that state doesn't replace:

- **Every push to every branch builds a preview** unless you tell the platform otherwise. Backup and housekeeping branches (`rescue/*`) must be excluded by name, or you pay for builds nobody will look at and get a failure email for each.
- **A red preview check is not proof the PR is broken.** Read the build log — a preview can fail on a limit production doesn't hit (a function-size cap the Preview environment lacks an env var for is a common one).
- **Merge is deploy** on most setups. The steward re-shows that warning before every merge.
- **Production incidents:** the platform's own rollback (to the previous deployment) is faster and safer than a revert PR. Roll back first, open the revert PR afterwards.
- **Set a spend cap** on the platform's billing page. No agent can do this for you, and nothing else protects your card.
- **Real branch protection** (blocking a push to main outright, not just refusing it in a local hook) may need a paid plan on some hosts — check before assuming it's available.

---

## 8. Rules for AI agents — paste these into your project's rules file

1. The main folder is a library: read-only. Work in a room started from the latest library, never from a stale local copy.
2. Rooms are opened with `start` and closed with `finish`. `ship` is the only push path. No agent pushes main.
3. `ship` runs in the background. Never sit in the foreground waiting on a build, and never end a turn with "say the word and I'll push" when a grant already exists — ask for the grant at the start instead.
4. Every reply that touches git, the database or deployments ends with **Done / Waiting / You decide**.
5. When a phrase is ambiguous, run `status` first and put the interpretation under "You decide". Never guess.
6. A worker agent never ships, merges, finishes or abandons. The parent does, once, after reading the real diff.
7. Database migrations are applied only through `migrate`, one file at a time, with the file's timestamp. Merging a PR never applies one.
8. Before removing anything — a room, a branch, a table — there is a backup (a rescue branch, an in-database copy) and the reply says how to recover.

---

## 9. Quick start — a whole task in eight lines

```
start on the classroom export and ship it when green     → room opened from the latest library
…build…                                                    → agent works; you don't think about git
note: the student page needs a loading state             → kept for the PR's follow-ups
(agent ships in the background)                          → PR opens with a plain-language body
is PR 42 safe?                                           → walkthrough + "safe to merge: yes, because…"
merge it                                                 → warns "this deploys", waits for your yes
done                                                     → room closed, library synced
clean up                                                 → dry-run plan, then your "go"
```
