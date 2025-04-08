import asyncio
from aiogram import Bot, Dispatcher
from read_configs import configs
from handlers import question, different_types
import logging

async def main() -> None:
    logging.basicConfig(level=logging.INFO) 

    bot = Bot(token=configs.bot_token.get_secret_value())
    dp = Dispatcher()
        
    dp.include_routers(question.router, different_types.router)
    # можна зарейструвати роутери по одному dp.include_router()
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
	asyncio.run(main())

