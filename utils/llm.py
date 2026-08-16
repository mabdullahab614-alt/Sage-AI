"""
Thin wrapper around the Groq API for chat + code generation.
"""
import os
from groq import Groq

# IMPORTANT: llama-3.3-70b-versatile and llama-3.1-8b-instant were
# deprecated by Groq (announced June 17, 2026) and are shut down as of
# August 16, 2026 — selecting either now returns a hard API error, not a
# slow/degraded response. They are deliberately NOT listed below. Current
# production replacements per Groq's own migration guidance:
# https://console.groq.com/docs/deprecations
AVAILABLE_MODELS = {
    "GPT-OSS 120B — best all-round (default)": "openai/gpt-oss-120b",
    "GPT-OSS 20B — fastest": "openai/gpt-oss-20b",
    "Qwen 3.6 27B — flagship reasoning + coding": "qwen/qwen3.6-27b",
}
DEFAULT_MODEL = "openai/gpt-oss-120b"

# Vision-capable model for image attachments. qwen/qwen3.6-27b is Groq's
# current multimodal option, but Groq itself documents it as a *preview*
# model (evaluation, not production) — so occasional flakiness/rate limits
# here are a known Groq-side limitation, not a bug in this app. There is
# currently no stable production vision model on Groq to fall back to.
VISION_MODEL = "qwen/qwen3.6-27b"

SYSTEM_PROMPT = (
    "You are Sage, a helpful AI assistant that can chat normally, answer "
    "questions grounded in documents the user uploads, and write/explain code. "
    "When you write Python code that the user could plausibly want to run, "
    "put it in a single fenced ```python code block so it can be executed. "
    "Be concise and direct."
)


def get_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY environment variable is not set. "
            "Get a free key at https://console.groq.com/keys and set it before running."
        )
    return Groq(api_key=api_key)


def chat_completion(messages: list[dict], model: str = DEFAULT_MODEL, temperature: float = 0.4) -> str:
    client = get_client()
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    response = client.chat.completions.create(
        model=model,
        messages=full_messages,
        temperature=temperature,
        max_tokens=2048,
    )
    return response.choices[0].message.content


def transcribe_audio(audio_bytes: bytes, filename: str = "voice.wav") -> str:
    client = get_client()
    transcription = client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model="whisper-large-v3-turbo",
        response_format="text",
    )
    return transcription if isinstance(transcription, str) else transcription.text


def extract_python_code_blocks(text: str) -> list[str]:
    """Pulls out ```python ... ``` blocks from a model response."""
    import re
    pattern = r"```python\s*\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [m.strip() for m in matches]
