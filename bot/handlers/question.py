from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboard.for_questions import get_yes_no_kb

router = Router() # [1]

@router.message(Command("start")) # [1]
async def cmd_start(message: Message):
    await message.answer("Вам подобається ваша робота", reply_markup=get_yes_no_kb())


@router.message(Text(text="так", ignore_case=True))
async def answer_yes(message: Message):
    await message.answer("Це круто", reply_markup=ReplyKeyboardRemove())


@router.message(Text(text="ні", ignore_case=True))
async def answer_no(message: Message):
    await message.answer("Погано кидай роботу", reply_markup=ReplyKeyboardRemove())
