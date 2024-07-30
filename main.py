import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.tg_auth_data import BotToken
from telegram_bot.bot.handlers import router

from backend.database.db_update_data import db_loop_update_orders_data


async def main():
    bot = Bot(token=BotToken().token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def start_work():
    await asyncio.gather(db_loop_update_orders_data(), main())

if __name__ == "__main__":
    asyncio.run(start_work())
