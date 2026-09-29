import discord

from agent import build_graph
from config import DISCORD_TOKEN

from flask import Flask
from threading import Thread
import os

# -------------------------
# Render Web Server
# -------------------------


app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web_server, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
graph = build_graph()


def format_reply(result: dict) -> str:
    if not result.get("topic"):
        return result["answer"]

    parts = [
        f"**Unit {result['unit_no']}: {result['unit_name']}**",
        f"**Topic:** {result['topic']}",
        "",
        result["answer"],
        "",
        "**Related PYQs on this topic:**",
    ]
    for i, p in enumerate(result["related_pyqs"], 1):
        year = f" ({p['year']})" if p["year"] else ""
        parts.append(f"{i}. {p['question']}{year}")
    return "\n".join(parts)


def chunks(text: str, size: int = 1900):
    while text:
        yield text[:size]
        text = text[size:]


@client.event
async def on_ready():
    print("=" * 60)
    print(f"✅ DISCORD BOT IS ONLINE AND READY!")
    print(f"Logged in as: {client.user} (ID: {client.user.id})")
    print(f"Connected to {len(client.guilds)} server(s)")
    print("Listening for mentions and DMs...")
    print("=" * 60)


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    # Respond in DMs, or when the bot is @mentioned in a server
    is_dm = isinstance(message.channel, discord.DMChannel)
    if not is_dm and client.user not in message.mentions:
        return

    question = message.content.replace(f"<@{client.user.id}>", "").strip()
    if not question:
        return

    print(f"📩 Received question from {message.author}: {question}")
    async with message.channel.typing():
        result = await graph.ainvoke({"question": question})

    reply_text = format_reply(result)
    for part in chunks(reply_text):
        await message.reply(part)
    print(f"📤 Replied to {message.author}")


if __name__ == "__main__":
    import sys

    # Ensure Windows console encoding
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    if "--check" in sys.argv:
        # Local self-test. Run from the project root with:
        #     python bot.py --check
        print("=== bot.py self-test (--check mode, no Discord connection) ===\n")

        sample_result = {
            "unit_no": 4,
            "unit_name": "Memory Management",
            "topic": "Paging and Segmentation",
            "answer": "Paging splits memory into fixed-size blocks called pages.",
            "related_pyqs": [
                {"question": "Explain paging with a diagram.", "year": "2022"},
                {"question": "What is a page table?", "year": ""},
            ],
        }
        print("--- format_reply() output for a matched question ---")
        print(format_reply(sample_result))

        print("\n--- format_reply() output for a not-found question ---")
        print(format_reply({"answer": "I couldn't match this question.", "topic": None}))

        long_text = "x" * 4200
        parts = list(chunks(long_text))
        print(f"\n--- chunks() split a {len(long_text)}-char string into {len(parts)} part(s) ---")
        for i, p in enumerate(parts, 1):
            print(f"   part {i}: {len(p)} chars")

        ok = (
            "Unit 4: Memory Management" in format_reply(sample_result)
            and len(parts) == 3
            and sum(len(p) for p in parts) == 4200
        )
        print("\nSUCCESS: bot.py helper functions work correctly." if ok else "\nFAILED: output did not match expectations.")
    else:
        if not DISCORD_TOKEN or DISCORD_TOKEN == "your_discord_bot_token":
            print("\n❌ ERROR: DISCORD_TOKEN is not set in your .env file!")
            print("Please add your Discord bot token to .env and try again.")
            sys.exit(1)

        print("\n🚀 Starting Discord Bot... Connecting to Discord...")
        try:
            client.run(DISCORD_TOKEN)
        except discord.errors.LoginFailure:
            print("\n❌ Login Failed: Improper or invalid Discord bot token.")
            print("👉 Check your DISCORD_TOKEN in .env (make sure there are no trailing spaces or quotes).")
        except discord.errors.PrivilegedIntentsRequired:
            print("\n❌ Privileged Intent Error: 'Message Content Intent' is disabled.")
            print("👉 Enable it: https://discord.com/developers/applications -> Bot -> Privileged Gateway Intents -> Enable 'MESSAGE CONTENT INTENT'.")

