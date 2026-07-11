# Goal Patterns

Use these as compact patterns. Adapt them to the actual repo, task, and available verification commands.

## Existing Repo Code Change

```text
/goal Implement [specific behavior] in the existing repo while preserving unrelated behavior.
Verification: inspect `AGENTS.md`, project scripts, nearby tests, and existing implementation first; run the smallest relevant lint/typecheck/test command; add or update a focused regression test when practical; report command output.
Constraints: keep public APIs, schemas, secrets, unrelated UI copy, and existing workflow gates unchanged.
Boundaries: edit only the files directly related to [feature/bug] plus tests/fixtures required for verification.
Iteration policy: make one focused change, rerun the failing or relevant check, inspect logs before changing strategy, and stop after 3 focused repair rounds with remaining blockers listed.
Stop when: the targeted behavior is proven by tests or runtime evidence and relevant checks pass, or missing project checks are explicitly reported.
Pause if: credentials, production data, destructive changes, schema ownership, payment behavior, or product decisions are required.
```

## New Local App Or Tool

```text
/goal Create a first-version local MVP for [tool/app] that lets the user complete [core workflow] end to end.
Verification: create or inspect the project run commands, start the local runtime, complete the core workflow once, and capture logs/screenshots or command output as evidence.
Constraints: do not add accounts, paid services, production deployment, analytics, unrelated features, or external dependencies unless needed for the MVP.
Boundaries: write only inside the new project directory and generated artifacts required for verification.
Iteration policy: build the smallest working path first, then do at most 3 focused usability or reliability improvements based on runtime evidence.
Stop when: the core workflow works locally and verification evidence is reported.
Pause if: deployment, credentials, paid APIs, account systems, copyrighted assets, or larger product scope is required.
```

## Research Or Content

```text
/goal Produce a source-backed [research brief/content package] for [topic] that is ready for review but not publishing.
驗證：檢查相關 tracker/repo 來源、官方或可信來源、已有 tone/content rules；列出來源連結、claim risk、建議下一步和任何 blocker。
約束：不可發布、排程、上傳、DM、標記 final approval，亦不可把未驗證傳聞寫成事實。
邊界：只建立或更新研究、草稿、brief、guide、caption 或 review payload；不改動發佈系統和審批狀態。
迭代策略：先收集來源，再做取捨和 angle；如資料不足，列 blocker，不用幻想補齊。
完成條件：交付可審核的 source-backed 產物，並清楚標示 claim risk、審批 gate、下一步。
暫停條件：需要負責人審批、平台登入、私人資料、未驗證高風險 claim、發佈/排程/上傳/DM 權限時暫停。
```

## Visual, Carousel, Deck, Or Frontend QA

```text
/goal Create or improve [visual/frontend artifact] so [target user] can understand [primary message/workflow] without layout breakage.
驗證：使用相關設計/品牌 skill 或既有設計系統；產出桌面和手機截圖或 contact sheet；檢查文字可讀性、層級、safe area、重疊、對比、claim/source 對應。
約束：保持品牌方向一致、文案語言準確性、來源 claim safety 和審批 gate；不可直接發布或標記 final。
邊界：只修改相關 HTML/CSS/component/render scripts/generated asset folder；不做無關 redesign。
迭代策略：先完成可檢視版本，再基於截圖做最多 3 輪聚焦改善。
完成條件：輸出路徑、檢查結果和剩餘風險清楚列明，且核心畫面在目標尺寸無明顯破損。
暫停條件：需要品牌決策、未授權素材、平台上傳、外部審批或超出本輪範圍的新視覺方向時暫停。
```

## Automation Or Scheduled Monitor

```text
/goal Define or update [automation] so it performs [recurring check/report] safely on [cadence] with clear memory and blockers.
Verification: inspect existing automation config, memory, source docs, and checker scripts; run dry-run or validation commands where available; confirm the active/paused state and expected output.
Constraints: do not enable publishing, uploads, DMs, destructive actions, or workflow status transitions beyond the approved gate.
Boundaries: edit only the automation contract, memory, docs, and directly related checker scripts.
Iteration policy: validate config first, make the smallest contract change, run checks, and report blockers instead of forcing a run through missing credentials.
Stop when: the automation contract is valid, expected cadence/output is documented, and safety gates are explicit.
Pause if: connector auth, credentials, external platform state, publish permissions, or owner approval is required.
```

## Skill Creation Or Skill Update

```text
/goal Create or update the Codex skill [name] so it captures [workflow] as a concise, reusable, validated operating procedure.
Verification: inspect existing runtime and repo-mirrored skills, create/update `SKILL.md` and only necessary references/scripts, run skill frontmatter validation, and run any included linter on a sample output.
Constraints: keep the skill concise, avoid duplicating existing skills, do not include secrets or broad unrelated docs, and preserve any approval gates.
Boundaries: write only under the target skill directory and its repo mirror unless the user asks for docs updates.
Iteration policy: implement the smallest useful skill first, validate structure, then add references or scripts only where they improve reliability.
Stop when: runtime and mirror copies match, validation passes, and usage/trigger boundaries are clear.
Pause if: naming, ownership, licensing, external import rights, or overlapping-skill consolidation decisions are unclear.
```

## Deployment Or External Service

```text
/goal Prepare [project] for [deployment/external service action] without making production changes until verification and approval are clear.
Verification: inspect official docs and project config, run local build/tests, identify required environment variables and account permissions, and report the exact deploy command or checklist.
Constraints: do not expose secrets, mutate production data, change DNS, charge paid services, or publish publicly without explicit approval.
Boundaries: edit only deployment config/docs and directly required code changes.
Iteration policy: separate local readiness from live deploy; resolve build/config errors with evidence; pause before irreversible or paid actions.
Stop when: local readiness is proven and the remaining live action is documented or explicitly completed with approval.
Pause if: credentials, billing, production data, DNS, account ownership, or irreversible deployment decisions are required.
```
