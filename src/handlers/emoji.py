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
    custom_emojis = [e for e in message.entities if e.type == "custom_emoji"]
    
    if not custom_emojis:
        return

    is_single_emoji = len(custom_emojis) == 1 and len(message.text.strip()) <= 3
    
    if is_single_emoji:
        emoji_id = custom_emojis[0].custom_emoji_id
        stickers = await bot.get_custom_emoji_stickers([emoji_id])
        pack_name = stickers[0].set_name if stickers else None
        
        builder = InlineKeyboardBuilder()
        builder.button(text="Just this one", callback_data=f"one_{emoji_id}")
        if pack_name:
            builder.button(text="Whole pack", callback_data=f"pack_{pack_name}")
        
        await message.answer(
            "Found a premium emoji! What do you want to get?",
            reply_markup=builder.as_markup()
        )
        return

    # To safely handle HTML and Telegram's UTF-16 offsets, we encode to utf-16-le
    from aiogram.utils.markdown import html_decoration as hd
    
    text = message.text
    # Each UTF-16 code unit is 2 bytes in utf-16-le
    text_utf16 = text.encode("utf-16-le")
    
    last_offset = 0
    parts = []
    
    # Sort entities by offset to process them in order
    sorted_entities = sorted(custom_emojis, key=lambda e: e.offset)
    
    for ent in sorted_entities:
        # Calculate byte offsets (Telegram offset * 2)
        start_byte = ent.offset * 2
        end_byte = (ent.offset + ent.length) * 2
        
        # Add escaped text before the emoji
        prev_text = text_utf16[last_offset*2:start_byte].decode("utf-16-le")
        parts.append(hd.quote(prev_text))
        
        # Add the emoji itself and its ID in code tags
        emoji_char = text_utf16[start_byte:end_byte].decode("utf-16-le")
        parts.append(f"{emoji_char} [<code>{ent.custom_emoji_id}</code>]")
        
        last_offset = ent.offset + ent.length
    
    # Add the remaining text
    remaining_text = text_utf16[last_offset*2:].decode("utf-16-le")
    parts.append(hd.quote(remaining_text))
    
    final_text = "".join(parts)
    await message.answer(f"<b>Processed text:</b>\n\n{final_text}", parse_mode="HTML")

@router.callback_query(F.data.startswith("one_"))
async def cb_one(callback: CallbackQuery, bot: Bot):
    # Use slicing to be safe
    emoji_id = callback.data[4:]
    stickers = await bot.get_custom_emoji_stickers([emoji_id])
    emoji_char = stickers[0].emoji if stickers else "?"
    
    response = f"<b>Emoji ID:</b>\n1) <code>{emoji_id}</code> <tg-emoji emoji-id=\"{emoji_id}\">{emoji_char}</tg-emoji>"
    await callback.message.edit_text(response, parse_mode="HTML")
    await callback.answer()
