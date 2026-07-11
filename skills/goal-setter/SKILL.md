---
name: goal-setter
description: Turn vague, risky, or multi-step agent work into a bounded `/goal` contract for coding, research, content, and automation tasks. Use when the user asks to write, improve, review, activate, or translate a goal, goal-setting skill, `/goal` prompt, success criteria, verification plan, stop condition, pause condition, task contract, or agent work definition.
---

# Goal Setter

Use this skill to turn an ambiguous request into a copy-ready Codex `/goal` with a clear outcome, verification, constraints, boundaries, iteration policy, completion evidence, and pause conditions.

Default stance: produce the best executable goal first. Do not make the user fill out a form unless the missing decision changes cost, risk, ownership, production state, or product direction.

## Operating Mode

- The output command starts with `/goal`, even when the rest is Traditional Chinese.
- Do not start the work described by the goal unless the user explicitly asks to execute or activate it.
- If the user asks to activate the goal in the current Codex thread, use the available goal tool after drafting the final objective.
- If the user asks only to draft, return the goal text and stop.
- Match the user's language: if they write in Chinese, respond in the same variety and register they use.
- For technical team handoff, English is fine unless the user asks otherwise.
- Prefer conservative defaults, narrow write boundaries, concrete verification, and explicit pause conditions.

## Workflow

1. Convert the request into a result, not an activity.
2. Classify risk:
   - Low: local prototype, docs, toy data, local UI, isolated script, non-destructive repo work.
   - Medium: existing repo changes, shared config, migrations in dev, public copy, browser/mobile/runtime checks.
   - High: production data, credentials, payments, destructive actions, legal/medical/financial judgment, private user data, publishing, uploads, scheduling, account ownership.
3. Discover context before inventing commands:
   - In a repo, inspect `AGENTS.md`, package scripts, `Makefile`, `scripts/`, CI config, docs, and nearby tests.
   - For content or publishing work, preserve any tracker/status gates and your team's approval rules.
4. Draft a goal with these fields:
   - Outcome
   - Verification
   - Constraints
   - Boundaries
   - Iteration policy
   - Stop when
   - Pause if
5. Ask only targeted multiple-choice questions when needed. Keep defaults explicit.
6. If the domain is unfamiliar, write a discovery-first goal that requires authoritative local docs, official docs, source data, or user-provided material before implementation.
7. If saving a goal contract to a file, run `scripts/lint_goal_contract.py` against it.

## Output Contract

For English output:

```text
/goal [concrete outcome].
Verification: [commands, runtime checks, screenshots, logs, files, API responses, or artifacts that prove completion].
Constraints: [behavior, data, public APIs, secrets, style, approvals, or branch rules that must not change].
Boundaries: [allowed files/directories and forbidden systems/paths].
Iteration policy: [one focused change at a time, rerun checks, inspect logs, cap improvement rounds].
Stop when: [specific evidence proves the work is complete].
Pause if: [human decision, credentials, auth, budget, destructive action, production data, or repeated blocker is required].
```

For Traditional Chinese output:

```text
/goal [具體完成結果]。
驗證：[命令、runtime 檢查、截圖、日誌、文件、API 回應或產物，用來證明完成]。
約束：[不可改變的行為、資料、公開 API、密鑰、風格、審批或分支規則]。
邊界：[允許寫入的位置，以及禁止觸碰的系統或路徑]。
迭代策略：[每次只做一個聚焦改動，重跑檢查，先讀日誌，限制改進輪數]。
完成條件：[有甚麼具體證據就可以停止]。
暫停條件：[需要人工決定、憑證、登入、預算、破壞性操作、生產資料或重複阻塞時暫停]。
```

When the request is vague but low-risk, output:

1. `推薦執行版（可直接複製）`
2. `預設選擇理由`
3. `可選調整`
4. `你可以直接回覆`

Keep optional adjustments short:

```text
可選調整
1. 形態：A 本地 MVP（預設） / B 改現有專案 / C 先做原型
2. 範圍：A 核心流程（預設） / B 加常見增強 / C 做完整產品
3. 驗證：A 本地檢查（預設） / B 瀏覽器/真機檢查 / C 部署後檢查

你可以直接回覆：按預設，或回覆 1B 2A 3C。
```

## Content And Publishing Defaults

- Treat any tracker/status fields as gates, not suggestions.
- Do not publish, schedule, upload, DM, or mark final approval unless the owner explicitly approves.
- Keep secrets, cookies, tokens, private credentials, and `.env*` files out of Git.
- Save durable workflow artifacts under the working repo when the goal asks for reusable output.
- For content, research, guide, visual, video, and deck tasks, require source-backed claims and approval checkpoints.
- For frontend/visual tasks, require desktop and mobile visual verification when a browser-rendered result exists.

## Quality Bar

A strong goal:

- has one concrete outcome
- names exact checks or discovery steps
- protects unrelated files, secrets, production data, and approval gates
- defines where the agent may write
- tells the agent how to iterate after failures
- says when completion is proven
- says when to pause for the user

Reject or revise a goal that:

- says only `make it better`, `finish this`, or `fix bugs`
- lacks verification
- allows broad edits without reason
- says to keep trying without new evidence
- omits pause conditions for auth, payments, production, destructive operations, or ambiguous decisions
- leaves placeholders in the final executable draft

## References

Read `references/goal-patterns.md` when drafting goals for coding, research, content, automations, visual QA, deployment, or skill creation.
