from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text)
async def answer_text(message: Message):
    await message.answer("Повідомлення типу текст")


@router.message(F.sticker)
async def answer_sticker(message: Message):
    await message.answer("Повідомлення типу стікера")


@router.message(F.animation)
async def answer_animation(message: Message):
    await message.answer("Повідомлення типу гіфки")