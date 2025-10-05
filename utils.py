import datetime
import aiogram.types as aio_types
import orario

HELPCOMAND = "/help"
TODAYCLASSES = "/buongiorno"
TOMORROWCLASSES = "/orariodomani"


async def command_handler(message: aio_types.Message):

    user_message = message.text
    user_fullname = message.chat.full_name
    user_name = message.chat.first_name
    userinfo = f"{user_fullname}({message.chat.id})"

    print(f"{userinfo} >> \n{user_message}\n----------ENDMSG----------")
    today = datetime.datetime.today().weekday()

    if user_message == HELPCOMAND:
        text = (f"Ciao {user_fullname}!\n"
                f"Io sono Garvis, un bot ideato e programmato da Cristian(matem817)\n"
                f"I comandi che supporto sono:\n"
                f"{HELPCOMAND} : mostra questo messaggio\n"
                f"{TODAYCLASSES} : mostra i prof. che avrai oggi\n"
                f"{TOMORROWCLASSES} : mostra i prof. che avrai domani\n")

    if user_message == TODAYCLASSES:
        classes = orario.get_for_day(today)
        text = f"Buongiorno {user_name}! :D\nL'orario di oggi è:\n{classes}"

    if user_message == TOMORROWCLASSES:
        classes = orario.get_for_day((today + 1)%7)
        text = f"Ciao {user_name}!\nL'orario di domani sarà:\n{classes}"

    else:
        text = (
            "Scusami ma non supporto messaggi al di fuori di comandi x_x\n"
            "Prova a usare:\n"
            "/help"
        )

    print(f"{userinfo} << \n{text}\n----------ENDMSG----------")
    await message.answer(text)





