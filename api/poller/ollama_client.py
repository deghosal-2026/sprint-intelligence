"""omlx client — OpenAI-compatible API for local LLM (Llama-3.2-3B-Instruct-4bit)."""

import os
import re
import requests

OMLX_URL = os.getenv("OMLX_URL", "http://host.docker.internal:8000")
OMLX_API_KEY = os.getenv("OMLX_API_KEY", "omlx-test")
OMLX_MODEL = os.getenv("OMLX_MODEL", "Llama-3.2-3B-Instruct-4bit")
TIMEOUT = int(os.getenv("OMLX_TIMEOUT", "120"))


def _strip_thinking(text):
    """Remove Qwen's thinking/reasoning prefix from model output."""
    lines = text.split("\n")
    clean = []
    in_thinking = False
    for line in lines:
        if re.match(r"^\d+\.\s+\*\*Analyze|^Thinking", line):
            in_thinking = True
        if not in_thinking:
            clean.append(line)
        if in_thinking and re.match(r"^\d+\.\s", line) and "→" in line:
            in_thinking = False
            clean.append(line)
            continue
    if not clean:
        clean = lines[len(lines)//2:]
    return "\n".join(clean).strip()


def chat(prompt, system=None, model=None, max_tokens=1024):
    url = f"{OMLX_URL}/v1/chat/completions"
    model = model or OMLX_MODEL
    headers = {
        "Authorization": f"Bearer {OMLX_API_KEY}",
        "Content-Type": "application/json",
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        resp = requests.post(
            url, headers=headers,
            json={"model": model, "messages": messages, "stream": False, "max_tokens": max_tokens},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        raw = data["choices"][0]["message"]["content"].strip()
        return _strip_thinking(raw)
    except Exception:
        return None


def is_available():
    try:
        resp = requests.get(f"{OMLX_URL}/v1/models", headers={"Authorization": f"Bearer {OMLX_API_KEY}"}, timeout=3)
        return resp.status_code == 200
    except Exception:
        return False
