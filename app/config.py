"""App configuration loaded from environment variables."""
import os

from dotenv import load_dotenv

load_dotenv()

# Which LLM provider to use: "anthropic" (Claude) or "google" (Gemini).
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").lower()
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-5-5")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "16000"))

SYSTEM_PROMPT = (
    "You are a helpful assistant. You have three tools: a calculator, "
    "a current date/time lookup, and a unit converter. Use a tool whenever "
    "the answer depends on exact arithmetic, the current time, or a unit "
    "conversion; otherwise answer directly. Keep answers short."
)
