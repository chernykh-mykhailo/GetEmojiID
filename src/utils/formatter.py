from aiogram import Bot

async def format_emoji_list(bot: Bot, pack_name: str) -> str:
    try:
        sticker_set = await bot.get_sticker_set(name=pack_name)
        if sticker_set.sticker_type != "custom_emoji":
            return "This is not a custom emoji pack (it's a regular sticker pack)."
        
        response = f"<b>Emoji Pack:</b> <code>{sticker_set.title}</code>\n"
        response += f"<b>Link:</b> t.me/addemoji/{pack_name}\n\n"
        response += "<b>List of emoji ids:</b>\n\n"
        
        for i, sticker in enumerate(sticker_set.stickers, 1):
            emoji_id = sticker.custom_emoji_id
            response += f"{i:02d}) <code>{emoji_id}</code> <tg-emoji emoji-id=\"{emoji_id}\">{sticker.emoji}</tg-emoji>\n"
        
        return response
    except Exception as e:
        return f"❌ <b>Error fetching pack</b> <code>{pack_name}</code>:\n<code>{str(e)}</code>"
