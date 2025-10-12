import json
import re
from telethon import TelegramClient, events
from transformers import pipeline

# ========== Fill in your keys ==========
api_id = 21377580
api_hash = '60815b4a66d3c361f789f62218cc54cd'
invite_link = 'https://t.me/joinchat/+VCpvxO-uy4M5ZjNk'
# ======================================

client = TelegramClient('session', api_id, api_hash)

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
categories = ["football", "boxing", "basketball", "miscellaneous"]

def parse_message(message):
    """
    Parses the message for channel number, event name, and time.
    Assumes message format: 'Channel X: Event Name at TIME'
    """
    match = re.match(r'Channel (\d+): (.+?) at (\d{1,2}:\d{2}\s?[APMapm]{2})', message)
    if match:
        channel_number = int(match.group(1))
        event_name = match.group(2).strip()
        event_time = match.group(3).strip()
        return channel_number, event_name, event_time
    else:
        # If parsing fails, use defaults
        return 0, message, "TBD"

def update_json(channel_number, event_text, time):
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except:
        data = []

    result = classifier(event_text, candidate_labels=categories)
    tag = result['labels'][0]

    # Append new event
    data.append({
        "channel": channel_number,
        "event": event_text,
        "time": time,
        "category": tag
    })

    # Save
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

async def main():
    # Get channel entity from invite link
    channel = await client.get_entity(invite_link)

    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        message = event.message.message
        channel_number, event_name, event_time = parse_message(message)
        update_json(channel_number, event_name, event_time)
        print(f"Added event: Channel {channel_number} | {event_name} | {event_time}")

    print("Listening for new messages...")
    await client.run_until_disconnected()

client.start()
client.loop.run_until_complete(main())
