import logging
import os
from dotenv import load_dotenv

from typing import Callable, Dict, Awaitable, Any

import asyncio
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import Message

from app.handlers import router
from app.database.db import connect_db

class MessageLogMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info(event.text) # Выводим текст сообщения
        return await handler(event, data)

async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    logging.basicConfig(level=logging.DEBUG, filename='bot.log') # Выставляем уровень логов на INFO
    dp.message.outer_middleware(MessageLogMiddleware())
    await connect_db()
    dp.include_router(router)
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
        print(ex)
        
