# Discwaal Stream Link Bot

A Telegram bot that:
- Accepts media from the admin
- Sends it to `@discwaal_bot`
- Waits for a stream link
- Sends a reply with either:
  - a thumbnail and link, or
  - just the link if no thumbnail

## 🔧 Setup

### 1. Create Telegram apps
Get your:
- `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org)

### 2. Generate `SESSION_STRING`
Run this with Telethon to get your session string:

```python
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = 123456
API_HASH = 'your_api_hash'

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print(client.session.save())
