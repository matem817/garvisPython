import logging
import aiogram
import sys
import asyncio
from aiogram.client.session.aiohttp import AiohttpSession
import aiogram.types as aio_types
import aiogram.filters as aio_filters
import datetime
import orario

ownerChatId = 6089716018
botToken = "7978317162:AAH3Wgzjs8f2egRCiKcqU6cXkNL8vzTYogo"

session = AiohttpSession()

dispatcher = aiogram.Dispatcher()

@dispatcher.message(aio_filters.Command(commands="buongiorno"))
async def buongiorno_handler(message: aio_types.message):
    print(f"{message.chat.id} >> \n{message.text}\n----------ENDMSG----------")
    today = datetime.datetime.today().weekday()
    classes = orario.get_for_day(today)
    text = f"L'orario di oggi è:\n{classes}"

    await message.answer(text)
    print(f"{message.chat.id} << \n{text}\n----------ENDMSG----------")

@dispatcher.message(aio_filters.Command(commands="orariodomani"))
async def orario_domani_handler(message: aio_types.message):
    print(f"{message.chat.id} >> \n{message.text}\n----------ENDMSG----------")
    today = (datetime.datetime.today().weekday() + 1) % 7
    classes = orario.get_for_day(today)
    text = f"L'orario di domani sarà:\n{classes}"

    await message.answer(text)
    print(f"{message.chat.id} << \n{text}\n----------ENDMSG----------")

@dispatcher.message()
async def message_handler(message: aio_types.message):
    print(f"{message.chat.id} >> \n{message.text}\n----------ENDMSG----------")
    text = (
        "Scusa ma non supporto messaggi al di fuori di comandi x_x\n"
        "Prova a usare:\n"
        "/buongiorno"
    )
    await message.answer(text)
    print(f"{message.chat.id} << \n{text}\n----------ENDMSG----------")



async def main() -> None:
    bot = aiogram.Bot(botToken, session=session)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
