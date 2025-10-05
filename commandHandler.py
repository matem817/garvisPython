import datetime
import aiogram.types as aio_types
from aiogram.types import FSInputFile

import orario
import logging

HELPCOMMAND = "/help"
TODAYCLASSES = "/buongiorno"
TOMORROWCLASSES = "/orariodomani"
STARTCOMMAND = "/start"
ADMINGETLOGS = "/getlogs"
OWNERID = 6089716018

logger = logging.getLogger(__name__)


async def command_handler(message: aio_types.message):

    raw = message.text or ""
    raw = raw.strip().lower()
    first_token = raw.split(maxsplit=1)[0]  # "/help@MyBot" oppure "/help"
    user_message = first_token.split("@", 1)[0]
    user_fullname = message.chat.full_name
    user_name = message.chat.first_name
    userinfo = f"{user_fullname}({message.chat.id})"

    today = datetime.datetime.today().weekday()

    logging.info(f"MESSAGE RECIVED:\n{userinfo} >> \n{message.text}\n----------ENDMSG----------\nAFTER ELABORATION:{user_message}\n")

    if  user_message == HELPCOMMAND or user_message == STARTCOMMAND:
        text = (f"Ciao {user_fullname}!\n"
                f"Io sono Garvis, un bot ideato e programmato da Cristian (@matem817)\n"
                f"I comandi che supporto sono:\n"
                f"{HELPCOMMAND} : mostra questo messaggio\n"
                f"{TODAYCLASSES} : mostra i prof. che avrai in orario oggi\n"
                f"{TOMORROWCLASSES} : mostra i prof. che avrai in orario domani\n")

    elif user_message == TODAYCLASSES:
        classes = orario.get_for_day(today)
        text = f"Buongiorno {user_name}! :D\nL'orario di oggi è:\n{classes}"

    elif user_message == TOMORROWCLASSES:
        classes = orario.get_for_day((today + 1)%7)
        text = f"Ciao {user_name}!\nL'orario di domani sarà:\n{classes}"

    elif user_message == ADMINGETLOGS:
        if message.chat.id == OWNERID:
            logging.info(f"DOCUMENT SENT:\n{userinfo} << \n resources/garvisLog.log \n----------ENDMSG----------\n")
            message.answer_document(FSInputFile("resources/garvisLog.log"))
        else:
            message.answer("Non hai i permessi necessari, X-x")
            logging.warn(f"{userinfo} tried {ADMINGETLOGS}")
        return

    else:
        text = (
            "Scusami ma non supporto messaggi al di fuori di comandi x_x\n"
            "Prova a usare:\n"
            "/help"
        )

    logging.info(f"MESSAGE SENT:\n{userinfo} << \n{text}\n----------ENDMSG----------\n")
    await message.answer(text)





