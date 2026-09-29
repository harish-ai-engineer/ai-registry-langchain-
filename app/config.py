"""App configuration loaded from environment variables."""
import os

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "claude-opus-5-5")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "16000"))

SYSTEM_PROMPT = (
    "You are a helpful assistant. You have three tools: a calculator, "
    "a current date/time lookup, and a unit converter. Use a tool whenever "
    "the answer depends on exact arithmetic, the current time, or a unit "
    "conversion; otherwise answer directly. Keep answers short."
)
