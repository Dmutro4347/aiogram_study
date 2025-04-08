import asyncio
import logging
from random import randint

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from magic_filter import F
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder
from contextlib import suppress
from typing import Optional
from aiogram.filters.callback_data import CallbackData

from read_configs import configs 

bot = Bot(configs.bot_token.get_secret_value())
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def cmd_calculator(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(0, 10):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)

    await message.answer(
            "Виберіть два числа",
            reply_markup=builder.as_markup(resize_keyboard=True),
            )


@dp.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяє сформувати ряд
    # із одної або декількох кнопок наприклад перший ряд буде складатися з декількох кнопок
    builder.row(
            types.KeyboardButton(text="Запросити геолокацію", request_location=True),
            types.KeyboardButton(text="Запросити контакт", request_contact=True)
            ) 
    builder.row(
            types.KeyboardButton(text="Створити вікторину", request_poll=types.KeyboardButtonPollType(type="quiz"))
            )
    builder.row(
            types.KeyboardButton(text="Вибір користувачів", request_user=types.KeyboardButtonRequestUser(request_id=1)),
            types.KeyboardButton(text="Вибір групи", request_chat=types.KeyboardButtonRequestChat(request_id=2, chat_is_channel=False))
            )

    await message.answer("Виберіть дію", reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(F.user_shared)
async def on_user_shared(message: types.Message):
    print(
        f"Request {message.user_shared.request_id}. "
        f"User ID: {message.user_shared.user_id}"
    )


@dp.message(F.chat_shared)
async def on_chat_shared(message: types.Message):
    print(
        f"Request {message.chat_shared.request_id}. "
        f"User ID: {message.chat_shared.chat_id}"
    )


@dp.message(Command("inline_url"))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(
            types.InlineKeyboardButton(text="Github", url="https://github.com/Dmutro4347")
            )
    builder.row(
            types.InlineKeyboardButton(text="Telegram", url="tg://resolve?domain=telegram")
            )
    # Щоб мати можливість показати ID-кнопку
    # У користувача повинен бути False флаг has_private_forwards
    user_id = 1061708541 
    chat_info = await bot.get_chat(user_id)
    if not chat_info.has_private_forwards:
       builder.row(types.InlineKeyboardButton(text="Якись користувач", url=f"tg://user?id={user_id}"))

    await message.answer("Вибери посилання", reply_markup=builder.as_markup())


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Інлайн кнопка", callback_data="random_value"))
    await message.answer("Нажміть на кнопку", reply_markup=builder.as_markup())


@dp.callback_query(Text("random_value"))
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer(text="Дякую що використали бота!", show_alert=True)
    # або просто await callback.answer()


user_data = {}

class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int]


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="-2", callback_data=NumbersCallbackFactory(action="change", value=-2)
    )
    builder.button(
        text="-1", callback_data=NumbersCallbackFactory(action="change", value=-1)
    )
    builder.button(
        text="+1", callback_data=NumbersCallbackFactory(action="change", value=1)
    )
    builder.button(
        text="+2", callback_data=NumbersCallbackFactory(action="change", value=2)
    )
    builder.button(text="Підтвердити", callback_data=NumbersCallbackFactory(action="finish"))
    builder.adjust(4) # вирівнюємо кнопки по 4 в ряд щоб получилось 4 + 1
    return builder.as_markup()


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Вкажіть число: {new_value}",
            reply_markup=get_keyboard_fab()
        )

@dp.message(Command("numbers_fab"))
async def cmd_numbers_fab(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Вкажіть число число: 0", reply_markup=get_keyboard_fab())

@dp.callback_query(NumbersCallbackFactory.filter())
async def callbacks_num_change_fab(callback: types.CallbackQuery, callback_data: NumbersCallbackFactory):
    # теперішнє значення
    user_value = user_data.get(callback.from_user.id, 0)
    # якщо число потрібно змінити
    if callback_data.action == "change":
        user_data[callback.from_user.id] = user_value + callback_data.value
        await update_num_text_fab(callback.message, user_value + callback_data.value)
    # якщо число потібно зафіксувати
    else:
        await callback.message.edit_text(f"Того: {user_value}")
    await callback.answer()


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "change"))
async def callbacks_num_change_fab(callback: types.CallbackQuery, callback_data: NumbersCallbackFactory):
    # теперішнє значення
    user_value = user_data.get(callback.from_user.id, 0)

    user_data[callback.from_user.id] = user_value + callback_data.value
    await update_num_text_fab(callback.message, user_value + callback_data)
    await callback.answer()

# натискання на кнопку підтвердити
@dp.callback_query(NumbersCallbackFactory.filter(F.action == "finish"))
async def callback_num_finish_fab(callback: types.CallbackQuery):
# теперішнє значення
    user_value = user_data.get(callback.from_user.id, 0)

    await callback.message.edit_text(f"Итого: {user_value}")
    await callback.answer()

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
