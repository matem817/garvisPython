import logging
import aiogram
import sys
import asyncio
from aiogram.client.session.aiohttp import AiohttpSession
import aiogram.types as aio_types
import aiogram.filters as aio_filters
from commandHandler import command_handler, HELPCOMMAND, TODAYCLASSES, TOMORROWCLASSES

ownerChatId = 6089716018
botToken = "7978317162:AAH3Wgzjs8f2egRCiKcqU6cXkNL8vzTYogo"

session = AiohttpSession()

dispatcher = aiogram.Dispatcher()

@dispatcher.message()
async def message_handler(message: aio_types.Message):
    await command_handler(message)



async def main() -> None:
    bot = aiogram.Bot(botToken, session=session)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s | %(filename)s | %(levelname)s: %(message)s')
    asyncio.run(main())
