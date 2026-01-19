import datetime

import aiogram.types as aio_types
from aiogram.types import FSInputFile
import botScripts.orario as orario
import logging
from resources.constants.commands import *

from botScripts.classDataHandler import ClassDataHandler, is_class_supported, is_user_admin
VERSION = "0.5.0beta"
GETCLASSESCOMANDS = [TODAYCLASSES, TOMORROWCLASSES, GETCLASSESFORDAY]

logger = logging.getLogger(__name__)

dH = ClassDataHandler()
getClass = dH.get_user_class

async def command_handler(message: aio_types.Message):
    raw = (message.text or "").strip().lower()
    command_args = raw.split()

    first_token = command_args[0]  # "/help@MyBot" oppure "/help"
    user_message = first_token.split("@", 1)[0]

    user_fullname = message.chat.full_name
    user_name = message.chat.first_name
    user_class = dH.get_user_class(message.chat.id)
    userinfo = f"{user_fullname}({message.chat.id})[{user_class or None}]"

    today = datetime.datetime.today().weekday()

    logging.info(f"MESSAGE RECIVED:\n{userinfo} >> \n{message.text}\n----------ENDMSG----------\nAFTER ELABORATION:{command_args}\n")
    is_admin=is_user_admin(message.chat.id)

    # Se l'utente ha eseguito /ic
    if user_message == SETCLASS:
        if len(command_args) != 2:
            text=(
                f"Sembra che tu non abbia inserito il comando correttamente. .-.\n"
                f"Andrebbe scritto così: {SETCLASS} 3C\n"
                f"Ti consiglio di scriverlo a mano!\n"
            )
        else:
            userClass_ = command_args[1]
            userClassCharList = list(userClass_)

            logging.debug(userClassCharList)

            if userClassCharList[0].isnumeric() and not userClassCharList[1].isnumeric() :
                userClass_ = userClassCharList[0] + userClassCharList[1]
                text= f"Ok! La tua classe è stata impostata su {userClass_}\n"
                logging.info(f"{userinfo} class has been set to {userClass_}")
                dH.set_user_class(message.chat.id, userClass_)
            else:
                text= f"Sembra che tu abbia inserito un valore non valido :/\n"

    # Se l'utente ha eseguito /start o /help
    elif  user_message == HELPCOMMAND or user_message == STARTCOMMAND:
        text = (
                f"Ciao {user_fullname}!\n"
                f"Io sono Garvis, un bot ideato e programmato da Cristian (@matem817)\n"
                f"I comandi che supporto sono:\n"
                f"{HELPCOMMAND} : mostra questo messaggio\n\n"
                f"{TODAYCLASSES} : mostra i prof. che avrai in orario oggi\n\n"
                f"{TOMORROWCLASSES} : mostra i prof. che avrai in orario domani\n\n"
                f"{GETCLASSESFORDAY} : mostra l'orario che avrai in un gioano che specifichi tu\n"
                f"i giorni vanno abbreviati alle loro prime 3 lettere.\n"
                f"Es. {GETCLASSESFORDAY} lun\n"
                f"Se invece specifichi anche la classe (es. {GETCLASSESFORDAY} lun 3c) verra mostrato l'orario per quella classe.\n\n"
                f"{SETCLASS} : imposta la classe a cui fai parte in modo che ti possa dare l'orario corretto\n"
                f"Andrebbe usato così: {SETCLASS} <la tua classe>\n\n"
                f"Se vuoi ricevere notifiche sui nuovi aggiornamenti del mio codice entra in questo canale:\n"
                f"https://t.me/+USfaUkiGmkBlZGJk\n"
                f"Attualmente la versione del mio codice è {VERSION}"
            )

    # Se l'utente chiede i logs (/getlogs)
    elif user_message == ADMINGETLOGS:
        if is_admin:
            logs = FSInputFile(f"resources/garvisLog{datetime.datetime.today().date()}.log")
            logging.info(f"DOCUMENT SENT:\n{userinfo} << \n resources/garvisLog.log \n----------ENDMSG----------\n")
            await message.answer_document(logs)
        else:
            await message.answer("Non hai i permessi necessari, X-x")
            logging.warning(f"{userinfo} tried {ADMINGETLOGS}")
        return

    # Se l'utente non ha una classe assegnata e ha provato a eseguire un comando che lo richiede
    elif not user_class and (user_message in GETCLASSESCOMANDS):
        text=(f"Uff....\n"                                      
              f"Non riesco a trovare a che classe fai parte O.o\n"
              f"fai {SETCLASS} seguito dalla tua classe per impostarla\n")

    # Se la classe del utente non è supportata E ha eseguito un comando in GETCLASSESCOMMAND
    elif not is_class_supported(user_class) and (user_message in GETCLASSESCOMANDS):
        text = (f"Scusa ma non ho l'orario per la tua classe.\n"
                f" Manda un messaggio a Cristian(@matem817) per aggiungerla!")

    # Se l'utente chiede l'orario del giorno
    elif user_message == TODAYCLASSES:
        classes = orario.get_for_day(user_class, today)
        text = f"Buongiorno {user_name}! :D\nL'orario di oggi è:\n{classes}"

    # Se l'utente chiede l'orario del giorno dopo
    elif user_message == TOMORROWCLASSES:
        classes = orario.get_for_day(user_class, (today + 1) % 7)
        text = f"Ciao {user_name}!\nL'orario di domani sarà:\n{classes}"

    # Se l'utente chiede l'orario per un giorno specifico
    elif user_message == GETCLASSESFORDAY:
        if len(command_args) > 1:
            day = command_args[1]
            if len(command_args) > 2 and is_class_supported(command_args[2].upper()):
                class_=command_args[2].upper()
            else: class_=user_class
            dayNum, fullDayName = orario.get_day_from_string(day)
            if  dayNum != -1:
                text = (f"L'orario della {class_} per {fullDayName} è:\n"
                        f"{orario.get_for_day(class_, dayNum)}")
            else:
                text = (f"Il giorno inserito non sembra essere valido. u.u\n"
                        f"I giorni della settimana vanno abbreviati alle prime 3 lettere. :3\n")
        else:
            text = (f"La sintassi del comando sembra essere sbagliata. x-x\n"
                    f"Andrebbe usato così: {GETCLASSESFORDAY} <lun, mar, mer...>\n"
                    f"es.: {GETCLASSESFORDAY} lun\n")

    elif user_message == "/gay":
        text=(
            f"Ciao Stefano, ecco l'orario della tua classe ;D\n"
            f"{orario.get_for_day("2F",today)}"
        )
    # Se l'utente ha scritto gibberish
    else:
        text = (
            "Scusami ma non supporto messaggi al di fuori di comandi x_x\n"
            "Prova a usare:\n"
            "/help"
        )

    logging.info(f"MESSAGE SENT:\n{userinfo} << \n{text}\n----------ENDMSG----------\n")
    await message.answer(text)

