from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(F.sticker)
async def handle_sticker(message: Message, bot: Bot):
    if not message.sticker.is_custom_emoji:
        await message.answer("This is a regular sticker, not a premium emoji.")
        return

    emoji_id = message.sticker.custom_emoji_id
    pack_name = message.sticker.set_name
    
    builder = InlineKeyboardBuilder()
    builder.button(text="Just this one", callback_data=f"one_{emoji_id}")
    if pack_name:
        builder.button(text="Whole pack", callback_data=f"pack_{pack_name}")
    
    await message.answer(
        "Found a premium emoji sticker! What do you want to get?",
        reply_markup=builder.as_markup()
    )

@router.message(F.entities)
async def handle_entities(message: Message, bot: Bot):
    entities = message.entities or []
    custom_emojis = [e for e in entities if e.type == "custom_emoji"]
    
    if not entities:
        return

    # Single emoji shortcut
    if len(custom_emojis) == 1 and len(entities) == 1 and len(message.text.strip()) <= 3:
        emoji_id = custom_emojis[0].custom_emoji_id
        stickers = await bot.get_custom_emoji_stickers([emoji_id])
        pack_name = stickers[0].set_name if stickers else None
        builder = InlineKeyboardBuilder()
        builder.button(text="Just this one", callback_data=f"one_{emoji_id}")
        if pack_name:
            builder.button(text="Whole pack", callback_data=f"pack_{pack_name}")
        await message.answer("Found a premium emoji! What do you want to get?", reply_markup=builder.as_markup())
        return

    # Super robust approach: Use aiogram's built-in HTML generator
    import re
    html_text = message.html_text
    
    # Use temporary markers for IDs to avoid them being caught by general <code> replacement
    pattern = re.compile(r'<tg-emoji emoji-id="(.*?)">(.*?)</tg-emoji>')
    processed_html = pattern.sub(r'\2 [<code>\1</code>]', html_text)
    
    # Convert formatting tags to symbols (EXCEPT <code> for our IDs)
    processed_html = processed_html.replace("<b>", "**").replace("</b>", "**")
    processed_html = processed_html.replace("<i>", "*").replace("</i>", "*")
    processed_html = processed_html.replace("<u>", "__").replace("</u>", "__")
    processed_html = processed_html.replace("<s>", "~~").replace("</s>", "~~")
    processed_html = processed_html.replace("<tg-spoiler>", "||").replace("</tg-spoiler>", "||")
    
    # For actual code/pre blocks in the original message, convert them to backticks
    # (IDs are already wrapped in <code>, but we'll leave them alone)
    processed_html = processed_html.replace("<pre>", "```\n").replace("</pre>", "\n```")
    
    def format_blockquote(match):
        content = match.group(1)
        lines = content.strip().split("\n")
        return "\n".join(f"> {line}" for line in lines)

    processed_html = re.sub(r'<blockquote>(.*?)</blockquote>', format_blockquote, processed_html, flags=re.DOTALL)

    full_response = f"<b>Processed text with symbols:</b>\n\n{processed_html}"
    
    if len(full_response) <= 4096:
        await message.answer(full_response, parse_mode="HTML")
    else:
        # Split by lines as a simple safety measure
        lines = processed_html.split("\n")
        chunk = "<b>Processed text with symbols:</b>\n\n"
        for line in lines:
            if len(chunk) + len(line) + 1 > 4000:
                await message.answer(chunk, parse_mode="HTML")
                chunk = ""
            chunk += line + "\n"
        
        if chunk.strip():
            await message.answer(chunk, parse_mode="HTML")

@router.callback_query(F.data.startswith("one_"))
async def cb_one(callback: CallbackQuery, bot: Bot):
    # Use slicing to be safe
    emoji_id = callback.data[4:]
    stickers = await bot.get_custom_emoji_stickers([emoji_id])
    emoji_char = stickers[0].emoji if stickers else "?"
    
    response = f"<b>Emoji ID:</b>\n1) <code>{emoji_id}</code> <tg-emoji emoji-id=\"{emoji_id}\">{emoji_char}</tg-emoji>"
    await callback.message.edit_text(response, parse_mode="HTML")
    await callback.answer()
