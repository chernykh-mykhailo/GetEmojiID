from aiogram import Bot
from src.utils.db import get_user_settings

def get_emoji_suffix(emoji_str: str, show_bound: bool) -> str:
    if not emoji_str or not show_bound:
        return ""
    return f" ➔ {emoji_str}"

async def format_emoji_list(bot: Bot, pack_name: str, user_id: int) -> list[str]:
    try:
        sticker_set = await bot.get_sticker_set(name=pack_name)
        is_custom = sticker_set.sticker_type == "custom_emoji"
        
        type_label = "Emoji Pack" if is_custom else "Sticker Pack"
        link_prefix = "t.me/addemoji/" if is_custom else "t.me/addstickers/"
        
        header = f"<b>{type_label}:</b> <code>{sticker_set.title}</code>\n"
        header += f"<b>Link:</b> {link_prefix}{pack_name}\n\n"
        header += f"<b>List of {'emoji' if is_custom else 'sticker'} IDs:</b>\n\n"
        
        messages = []
        current_msg = header
        
        settings = await get_user_settings(user_id)
        show_bound = settings["show_bound_emoji"]
        
        for i, sticker in enumerate(sticker_set.stickers, 1):
            if is_custom:
                emoji_id = sticker.custom_emoji_id
                suffix = get_emoji_suffix(sticker.emoji, show_bound)
                line = f"{i:02d}) <code>{emoji_id}</code> <tg-emoji emoji-id=\"{emoji_id}\">{sticker.emoji}</tg-emoji>{suffix}\n"
            else:
                line = f"{i:02d}) <code>{sticker.file_id}</code> {sticker.emoji if sticker.emoji else ''}\n"
            
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
