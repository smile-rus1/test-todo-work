import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from dependencies import register_handlers

logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.token)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    logging.info("Starting bot setup...")
    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
