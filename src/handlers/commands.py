from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.utils.db import get_user_settings, update_user_settings

router = Router()

def get_settings_keyboard(settings: dict):
    builder = InlineKeyboardBuilder()
    
    bound_status = "✅" if settings["show_bound_emoji"] else "❌"
    
    builder.button(
        text=f"{bound_status} Прив'язані емодзі / Bound Emojis",
        callback_data="toggle_bound"
    )
    builder.adjust(1)
    return builder.as_markup()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Hi! Send me a link to a premium emoji pack, a single premium emoji, "
        "or text containing premium emojis to get their IDs.\n\n"
        "⚙️ Use /settings to configure how emoji information is displayed."
    )

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    settings = await get_user_settings(message.from_user.id)
    text = (
        "⚙️ <b>Налаштування відображення емодзі / Emoji Display Settings</b>\n\n"
        "Оберіть, що показувати поруч з преміум емодзі:\n"
        "Choose what to display next to premium emojis:\n\n"
        "<b>Прив'язані емодзі</b> — стандартні емодзі, до яких прив'язані преміум емодзі.\n"
    )
    await message.answer(text, reply_markup=get_settings_keyboard(settings), parse_mode="HTML")

@router.callback_query(F.data.startswith("toggle_"))
async def cb_toggle_settings(callback: CallbackQuery):
    user_id = callback.from_user.id
    settings = await get_user_settings(user_id)
    
    action = callback.data.split("_")[1]
    if action == "bound":
        settings["show_bound_emoji"] = not settings["show_bound_emoji"]
        
    await update_user_settings(
        user_id,
        show_bound_emoji=settings["show_bound_emoji"],
        show_emoji_text=settings["show_emoji_text"]
    )
    
    await callback.message.edit_reply_markup(
        reply_markup=get_settings_keyboard(settings)
    )
    await callback.answer("Налаштування оновлено! / Settings updated!")
