import logging
import sys
import aiogram
import asyncio
from aiogram.client.session.aiohttp import AiohttpSession
import aiogram.types as aio_types
from botScripts.commandHandler import command_handler


ownerChatId = 6089716018

botToken = input("Inserisci token del bot:")

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
                            logging.FileHandler("resources/garvisLog.log", mode="a", encoding="utf-8")
                        ]
                        )

    asyncio.run(main())
