import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.tg_auth_data import BotToken
from telegram_bot.bot.handlers import router

from backend.database.db_update_data import db_update_orders_data


async def main():
    bot = Bot(token=BotToken().token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    '''asyncio.run(db_update_orders_data())
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())'''

    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(db_update_orders_data()),
        ioloop.create_task(main())
    ]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()
