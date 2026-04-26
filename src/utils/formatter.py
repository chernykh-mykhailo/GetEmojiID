from aiogram import Bot

async def format_emoji_list(bot: Bot, pack_name: str) -> list[str]:
    try:
        sticker_set = await bot.get_sticker_set(name=pack_name)
        if sticker_set.sticker_type != "custom_emoji":
            return ["This is not a custom emoji pack (it's a regular sticker pack)."]
        
        header = f"<b>Emoji Pack:</b> <code>{sticker_set.title}</code>\n"
        header += f"<b>Link:</b> t.me/addemoji/{pack_name}\n\n"
        header += "<b>List of emoji ids:</b>\n\n"
        
        messages = []
        current_msg = header
        
        for i, sticker in enumerate(sticker_set.stickers, 1):
            emoji_id = sticker.custom_emoji_id
            line = f"{i:02d}) <code>{emoji_id}</code> <tg-emoji emoji-id=\"{emoji_id}\">{sticker.emoji}</tg-emoji>\n"
            
            if len(current_msg) + len(line) > 4000:
                messages.append(current_msg)
                current_msg = line
            else:
                current_msg += line
        
        if current_msg:
            messages.append(current_msg)
            
        return messages
    except Exception as e:
        return [f"❌ <b>Error fetching pack</b> <code>{pack_name}</code>:\n<code>{str(e)}</code>"]
