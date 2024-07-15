import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import main_commands_handlers, authorization_handlers


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(main_commands_handlers.router)
    dp.include_router(authorization_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print('Exit')
