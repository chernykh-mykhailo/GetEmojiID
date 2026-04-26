from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Hi! Send me a link to a premium emoji pack, a single premium emoji, "
        "or text containing premium emojis to get their IDs."
    )
