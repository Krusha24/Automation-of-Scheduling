import asyncio
import logging 

from Bot.config import bot, dp
from Bot.Handlers.student_handlers import student_router
from Bot.Handlers.teacher_handlers import teacher_router
from Bot.Handlers.dean_handlers import dean_router
from Bot.Handlers.common_handlers import common_router

from DataBase.base import async_main

async def main():
    await async_main()
    dp.include_router(student_router)
    dp.include_router(teacher_router)
    dp.include_router(dean_router)
    dp.include_router(common_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')