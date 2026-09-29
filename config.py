import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


if __name__ == "__main__":
    # Local self-test. Run from the project root with:
    #     python config.py
    # No API keys needed - this just shows what config.py read from .env.
    print("=== config.py self-test ===\n")
    print(f"DATA_DIR        : {DATA_DIR}")
    print(f"DATA_DIR exists : {DATA_DIR.exists()}")
    print(f"DISCORD_TOKEN   : {'set (' + str(len(DISCORD_TOKEN)) + ' chars)' if DISCORD_TOKEN else 'NOT SET'}")
    print(f"GOOGLE_API_KEY  : {'set (' + str(len(GOOGLE_API_KEY)) + ' chars)' if GOOGLE_API_KEY else 'NOT SET'}")
    print(f"GEMINI_MODEL    : {GEMINI_MODEL}")

    problems = []
    if not DATA_DIR.exists():
        problems.append("DATA_DIR does not exist.")
    if not DISCORD_TOKEN:
        problems.append("DISCORD_TOKEN is missing - needed to run bot.py for real.")
    if not GOOGLE_API_KEY:
        problems.append("GOOGLE_API_KEY is missing - needed for agent/nodes.py and agent/graph.py.")

    if problems:
        print("\nWarnings:")
        for p in problems:
            print(f"   - {p}")
        print("\nAdd the missing values to your .env file (copy .env.example first).")
    else:
        print("\nSUCCESS: all config values are set.")
