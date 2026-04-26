import re
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from src.utils.formatter import format_emoji_list

router = Router()

# More robust pattern for Telegram links (supports dots, underscores, and full URLs)
PACK_LINK_PATTERN = re.compile(r"(?:https?://)?(?:t\.me/addemoji/|tg://addemoji\?set=)([a-zA-Z0-9_\.]+)")

@router.message(F.text.regexp(PACK_LINK_PATTERN))
async def handle_pack_link(message: Message, bot: Bot):
    match = PACK_LINK_PATTERN.search(message.text)
    if match:
        pack_name = match.group(1).strip().strip('/') # Clean trailing slashes
        wait_msg = await message.answer(f"🔄 Fetching pack info for <code>{pack_name}</code>...", parse_mode="HTML")
        result = await format_emoji_list(bot, pack_name)
        await wait_msg.edit_text(result, parse_mode="HTML")

@router.callback_query(F.data.startswith("pack_"))
async def cb_pack(callback: CallbackQuery, bot: Bot):
    # Use slicing instead of split to handle pack names with underscores
    pack_name = callback.data[5:] 
    await callback.message.edit_text(f"🔄 Fetching pack info for <code>{pack_name}</code>...", parse_mode="HTML")
    result = await format_emoji_list(bot, pack_name)
    await callback.message.edit_text(result, parse_mode="HTML")
    await callback.answer()
