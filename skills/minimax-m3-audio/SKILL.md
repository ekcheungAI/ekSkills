---
name: minimax-m3-audio
description: Use this skill when Codex needs to test or use MiniMax API capabilities, especially MiniMax-M3 coding-plan/chat calls through the OpenAI-compatible API and MiniMax Text-to-Speech audio generation. Trigger for requests mentioning MiniMax M3, M3 coding plans, MiniMax API smoke tests, TTS, speech, voice, audio generation, Cantonese narration, or verifying whether Codex can make audio with MiniMax.
---

# MiniMax M3 Audio

## Core Rules

- Never write API keys into Git-tracked files, scripts, prompts, logs, or final answers.
- Read credentials from `MINIMAX_API_KEY`, optionally from an ignored local `.env.local`.
- Save generated audio under the active project, normally `generated-assets/audio/` or a task-specific generated-assets folder.
- Match the narration language/register to the user's brief (e.g. Traditional Chinese with a Hong Kong angle) unless the user asks otherwise.
- Use official MiniMax docs as current authority when endpoint behavior changes. See `references/minimax-api-notes.md`.

## Quick Start

Check that the key is present without printing it:

```bash
test -n "${MINIMAX_API_KEY:-}" && echo "MINIMAX_API_KEY is set"
```

Generate a MiniMax-M3 coding plan:

```bash
python codex/skills/minimax-m3-audio/scripts/minimax_m3_plan.py \
  --prompt "Plan a safe API smoke test for MiniMax TTS." \
  --out generated-assets/minimax-m3-plan.md
```

Generate a short TTS audio file:

```bash
python codex/skills/minimax-m3-audio/scripts/minimax_tts.py \
  --text "Hello from MiniMax. This is a short audio smoke test." \
  --out generated-assets/audio/minimax-smoke-test.mp3
```

For Cantonese/Hong Kong narration:

```bash
python codex/skills/minimax-m3-audio/scripts/minimax_tts.py \
  --language-boost Chinese,Yue \
  --text "大家好，呢段係 MiniMax 語音生成測試。" \
  --out generated-assets/audio/minimax-cantonese-test.mp3
```

## Workflow

1. Identify whether the user wants a coding plan, audio generation, or both.
2. Confirm the relevant environment variables are available without exposing values.
3. For M3 planning, run `scripts/minimax_m3_plan.py` and review the plan before applying it to code.
4. For audio, run `scripts/minimax_tts.py`, then verify the output file exists and is non-empty.
5. Report the output path, model used, and whether the call was live or only locally validated.

## Optional Environment Variables

- `MINIMAX_API_KEY`: required for live API calls.
- `MINIMAX_BASE_URL`: optional OpenAI-compatible base URL, default `https://api.minimax.io/v1`.
- `MINIMAX_TTS_URL`: optional T2A endpoint override, default `https://api.minimax.io/v1/t2a_v2`.
- `MINIMAX_MODEL`: optional chat model override, default `MiniMax-M3`.
- `MINIMAX_TTS_MODEL`: optional speech model override, default `speech-2.8-turbo`.
- `MINIMAX_VOICE_ID`: optional speech voice override.

## Validation

Run these checks after changing the skill:

```bash
python -m py_compile \
  scripts/minimax_m3_plan.py \
  scripts/minimax_tts.py
```
