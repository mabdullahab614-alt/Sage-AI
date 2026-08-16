"""
Thin wrapper around the Groq API for chat + code generation.
"""

import os
from groq import Groq

# Groq-hosted models available for selection in the UI. Verified against
# Groq's own "Production Models" list (console.groq.com/docs/models) — only
# models that appear there are included. llama3-70b-8192 and gemma2-9b-it
# were removed from that list (retired) and are deliberately NOT offered
# here; openai/gpt-oss-120b and openai/gpt-oss-20b are their current
# production-tier replacements. If Groq retires or renames a model, update
# this list — the app will surface Groq's own error message if a stale
# model id is selected, it won't fail silently.
AVAILABLE_MODELS = {
    "Llama 3.3 70B — best all-round (default)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B — fastest": "llama-3.1-8b-instant",
    "GPT-OSS 120B — OpenAI open-weight, reasoning": "openai/gpt-oss-120b",
    "GPT-OSS 20B — OpenAI open-weight, fast": "openai/gpt-oss-20b",
}
DEFAULT_MODEL = "llama-3.3-70b-versatile"

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
    """
    messages: list of {"role": "user"|"assistant"|"system", "content": str}
    model: any Groq model id (see AVAILABLE_MODELS for the ones surfaced in the UI)
    Returns the assistant's reply text.
    """
    client = get_client()
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    response = client.chat.completions.create(
        model=model,
        messages=full_messages,
        temperature=temperature,
        max_tokens=2048,
    )
    return response.choices[0].message.content


def extract_python_code_blocks(text: str) -> list[str]:
    """Pulls out ```python ... ``` blocks from a model response."""
    import re

    pattern = r"```python\s*\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [m.strip() for m in matches]
