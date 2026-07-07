# 🎯 Telegram Premium Emoji & Sticker ID Bot

<p align="left">
  <b>🇺🇸 English</b> | <a href="./README.ua.md">🇺🇦 Українська</a>
</p>

A Telegram bot designed to quickly retrieve system IDs for premium custom emojis, stickers, GIFs, and other media files to facilitate bot development and profile customization.

---

## 🚀 Features

- **Pack Analysis**: Send any sticker or emoji pack link (e.g. `https://t.me/addemoji/...` or `https://t.me/addstickers/...`), and the bot returns a complete list of all items with their corresponding unique IDs.
- **Single File Processor**: Send any custom premium emoji, sticker, animated GIF, video, photo, document, or voice note to immediately get its raw Telegram file/custom emoji ID.
- **Inline Text Parsing**: Send any text paragraph containing premium custom emojis, and the bot will return the formatted string with the parsed ID appended after each emoji in `[ID]` format.
- **One-Click Copying**: All IDs are formatted as monospace HTML code (`<code>`), enabling one-click copying on all Telegram clients.

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Bot Engine**: `aiogram 3.x`
- **Deployment**: Docker, Docker Compose

## 📁 Project Structure

- `src/handlers/` — Message handlers, pack links parser, and media validators.
- `src/utils/` — Message formatting helper functions.
- `main.py` — Bot initialization and pooling loop.

## ⚙️ Configuration & Run

### 1. Environment Settings
Create a `.env` file in the root directory:
```env
BOT_TOKEN=your_telegram_bot_token
```

### 2. Deploy with Docker (Recommended)
```bash
docker compose up -d --build
```

### 3. Run Locally
```bash
pip install -r requirements.txt
python main.py
```

---
*Developed by Mykhailo Chernykh.*
