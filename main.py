import logging
import sys
import aiogram
import asyncio
import datetime
import aiogram.types as aio_types
from aiogram.client.session.aiohttp import AiohttpSession
from botScripts.commandHandler import command_handler
import launcher.settingParser as sP

botToken=sP.ReadSettings().token
if botToken is None:
    botToken=input("Enter bot token: ")
    sP.write_setting("token", botToken)

session = AiohttpSession()
dispatcher = aiogram.Dispatcher()

@dispatcher.message()
async def message_handler(message: aio_types.Message):
    await command_handler(message)

async def main() -> None:
    bot = aiogram.Bot(botToken, session=session)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s | %(filename)s | %(levelname)s: %(message)s',
                        handlers = [
                            logging.StreamHandler(sys.stdout),  # Log su stdout
                            logging.FileHandler(f"resources/garvisLog{datetime.datetime.today().date()}.log", mode="a", encoding="utf-8")
                        ]
                    )
    asyncio.run(main())
