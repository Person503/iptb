import os
import json
from telethon import TelegramClient
from datetime import datetime

# === Get environment variables from GitHub Secrets ===
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# === Create client ===
client = TelegramClient("bot_session", API_ID, API_HASH)

# === Start using bot token automatically (no input) ===
if BOT_TOKEN:
    client.start(bot_token=BOT_TOKEN)
else:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN not found in environment variables.")

# === Channel username or ID ===
CHANNEL_USERNAME = "your_channel_username_here"  # e.g. "mychannel" or "-1001234567890"

# === JSON data file path ===
DATA_FILE = "data.json"

# === Helper to load old data ===
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# === Helper to save new data ===
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# === Main async function ===
async def main():
    print(f"📡 Fetching messages from {CHANNEL_USERNAME}...")
    old_data = load_data()
    old_ids = {msg["id"] for msg in old_data}

    messages = []
    async for message in client.iter_messages(CHANNEL_USERNAME, limit=50):
        if message.text and message.id not in old_ids:
            messages.append({
                "id": message.id,
                "date": message.date.strftime("%Y-%m-%d %H:%M:%S"),
                "text": message.text,
            })

    if messages:
        print(f"✅ {len(messages)} new messages fetched.")
        new_data = messages + old_data
        save_data(new_data)
    else:
        print("ℹ️ No new messages found.")

    print("💾 data.json updated successfully.")

# === Run ===
with client:
    client.loop.run_until_complete(main())
