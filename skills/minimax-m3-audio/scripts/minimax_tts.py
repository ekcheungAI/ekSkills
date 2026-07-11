#!/usr/bin/env python3
"""Generate speech with MiniMax T2A HTTP and write a local audio file."""

from __future__ import annotations

import argparse
import binascii
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_TTS_URL = "https://api.minimax.io/v1/t2a_v2"
DEFAULT_TTS_MODEL = "speech-2.8-turbo"
DEFAULT_VOICE_ID = "English_expressive_narrator"


def load_dotenv() -> None:
    for name in (".env.local", ".env"):
        path = Path.cwd() / name
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def read_text_arg(text: str | None, text_file: str | None) -> str:
    if text and text_file:
        raise SystemExit("Use either --text or --text-file, not both.")
    if text_file:
        return Path(text_file).read_text(encoding="utf-8")
    if text:
        return text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Provide --text, --text-file, or stdin text.")


def post_json(url: str, api_key: str, payload: dict) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"MiniMax HTTP {exc.code}: {detail}") from exc


def response_audio_bytes(response: dict) -> bytes:
    base_resp = response.get("base_resp") or {}
    if base_resp and base_resp.get("status_code") not in (0, None):
        raise SystemExit(f"MiniMax error: {json.dumps(base_resp, ensure_ascii=False)}")

    data = response.get("data") or {}
    audio_hex = data.get("audio")
    audio_url = data.get("audio_url") or data.get("url")

    if audio_hex:
        try:
            return binascii.unhexlify(audio_hex)
        except (binascii.Error, TypeError) as exc:
            raise SystemExit("MiniMax returned invalid hex audio data.") from exc

    if audio_url:
        with urllib.request.urlopen(audio_url, timeout=180) as response_obj:
            return response_obj.read()

    raise SystemExit(f"MiniMax response did not include audio data: {json.dumps(response)[:1000]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Text to synthesize.")
    parser.add_argument("--text-file", help="UTF-8 text file to synthesize.")
    parser.add_argument("--out", required=True, help="Output audio path.")
    parser.add_argument("--model", default=os.getenv("MINIMAX_TTS_MODEL", DEFAULT_TTS_MODEL))
    parser.add_argument("--voice-id", default=os.getenv("MINIMAX_VOICE_ID", DEFAULT_VOICE_ID))
    parser.add_argument("--tts-url", default=os.getenv("MINIMAX_TTS_URL", DEFAULT_TTS_URL))
    parser.add_argument("--language-boost", default="auto")
    parser.add_argument("--format", choices=("mp3", "wav", "flac"), default="mp3")
    parser.add_argument("--sample-rate", type=int, default=32000)
    parser.add_argument("--bitrate", type=int, default=128000)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--volume", type=float, default=1.0)
    parser.add_argument("--pitch", type=int, default=0)
    parser.add_argument("--output-format", choices=("hex", "url"), default="hex")
    parser.add_argument("--metadata-out", help="Optional JSON metadata path.")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise SystemExit("MINIMAX_API_KEY is not set. Put it in the environment or ignored .env.local.")

    text = read_text_arg(args.text, args.text_file).strip()
    if not text:
        raise SystemExit("Text is empty.")
    if len(text) >= 10000:
        raise SystemExit("Text must be under 10,000 characters for synchronous MiniMax T2A.")

    payload = {
        "model": args.model,
        "text": text,
        "stream": False,
        "language_boost": args.language_boost,
        "output_format": args.output_format,
        "voice_setting": {
            "voice_id": args.voice_id,
            "speed": args.speed,
            "vol": args.volume,
            "pitch": args.pitch,
        },
        "audio_setting": {
            "sample_rate": args.sample_rate,
            "bitrate": args.bitrate,
            "format": args.format,
            "channel": 1,
        },
    }

    response = post_json(args.tts_url, api_key, payload)
    audio = response_audio_bytes(response)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(audio)

    metadata_path = Path(args.metadata_out) if args.metadata_out else out_path.with_suffix(out_path.suffix + ".json")
    metadata = {
        "model": args.model,
        "voice_id": args.voice_id,
        "language_boost": args.language_boost,
        "output_path": str(out_path),
        "bytes": len(audio),
        "trace_id": response.get("trace_id"),
        "extra_info": response.get("extra_info"),
        "base_resp": response.get("base_resp"),
    }
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
