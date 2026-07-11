# MiniMax API Notes

Sources checked on 2026-06-23:

- OpenAI-compatible text API: `https://platform.minimax.io/docs/api-reference/text-openai-api`
- T2A HTTP API: `https://platform.minimax.io/docs/api-reference/speech-t2a-http`
- API overview: `https://platform.minimax.io/docs/api-reference/api-overview`

## MiniMax-M3 Chat

- Base URL: `https://api.minimax.io/v1`.
- OpenAI-compatible endpoint: `POST /chat/completions`.
- Model ID: `MiniMax-M3`.
- Authorization: `Authorization: Bearer $MINIMAX_API_KEY`.
- M3 supports long-context coding, agentic reasoning, tool use, text, image, and video inputs.
- Use `max_completion_tokens` for generation limits.
- Use `thinking: {"type": "disabled"}` for direct planning output when hidden reasoning is not needed.
- Do not print, save, or forward raw reasoning details unless the user explicitly needs provider-debug output.

## T2A Speech

- Endpoint: `POST https://api.minimax.io/v1/t2a_v2`.
- Alternative lower-TTFA endpoint: `https://api-uw.minimax.io/v1/t2a_v2`.
- Authorization: `Authorization: Bearer $MINIMAX_API_KEY`.
- Required request fields: `model`, `text`.
- Current speech models include `speech-2.8-hd`, `speech-2.8-turbo`, `speech-2.6-hd`, `speech-2.6-turbo`, `speech-02-hd`, `speech-02-turbo`, `speech-01-hd`, and `speech-01-turbo`.
- Text must be under 10,000 characters. For over 3,000 characters, streaming is recommended.
- Non-streaming output supports `mp3`, `wav`, and `flac`.
- Non-streaming `output_format` can be `hex` or `url`; `hex` is easiest for deterministic local file writes.
- For Cantonese, set `language_boost` to `Chinese,Yue`.
- Pause control is supported with markers like `<#0.5#>` between speakable text segments.
- Inline pronunciation can use Cantonese Jyutping in parentheses, for example `啲(di1)`.

## Voice selection

Set `MINIMAX_VOICE_ID` (and `MINIMAX_GROUP_ID` where the API requires it) via environment
variables to the voice your MiniMax account has access to. Never hardcode a voice or group
ID in the skill.
