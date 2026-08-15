"""
Thin wrapper around the Groq API for chat + code generation.
"""

import os
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"  # strong at both chat and code, free tier

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


def chat_completion(messages: list[dict], temperature: float = 0.4) -> str:
    """
    messages: list of {"role": "user"|"assistant"|"system", "content": str}
    Returns the assistant's reply text.
    """
    client = get_client()
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    response = client.chat.completions.create(
        model=MODEL_NAME,
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
