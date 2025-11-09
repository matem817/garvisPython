import datetime

import aiogram.types as aio_types
from aiogram.types import FSInputFile

import botScripts.orario as orario
import logging

from botScripts.dataHandler import DataHandler, is_class_supported

VERSION = "0.3.1beta"
OWNERID = 6089716018
HELPCOMMAND = "/help"
TODAYCLASSES = "/buongiorno"
TOMORROWCLASSES = "/orariodomani"
STARTCOMMAND = "/start"
ADMINGETLOGS = "/getlogs"
SETCLASS = "/ic"
GETCLASSESFORDAY = "/orarioper"
GETCLASSESCOMANDS = [TODAYCLASSES, TOMORROWCLASSES, GETCLASSESFORDAY]

logger = logging.getLogger(__name__)

dH = DataHandler()
getClass = dH.get_user_class


async def command_handler(message: aio_types.Message):


    raw = (message.text or "").strip().lower()
    commandArgs = raw.split()

    first_token = commandArgs[0]  # "/help@MyBot" oppure "/help"
    user_message = first_token.split("@", 1)[0]

    user_fullname = message.chat.full_name
    user_name = message.chat.first_name
    userClass = dH.get_user_class(message.chat.id)
    userinfo = f"{user_fullname}({message.chat.id})[{userClass or None}]"

    today = datetime.datetime.today().weekday()

    logging.info(f"MESSAGE RECIVED:\n{userinfo} >> \n{message.text}\n----------ENDMSG----------\nAFTER ELABORATION:{commandArgs}\n")

    # Se l'utente ha eseguito /ic
    if user_message == SETCLASS:
        if len(commandArgs) != 2:
            text=(
                f"Sembra che tu non abbia inserito il comando correttamente. .-.\n"
                f"Andrebbe scritto così: {SETCLASS} 3C\n"
                f"Ti consiglio di scriverlo a mano!\n"
            )
        else:
            userClass_ = commandArgs[1]
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
        text = (f"Ciao {user_fullname}!\n"
                f"Io sono Garvis, un bot ideato e programmato da Cristian (@matem817)\n"
                f"I comandi che supporto sono:\n"
                f"{HELPCOMMAND} : mostra questo messaggio\n\n"
                f"{TODAYCLASSES} : mostra i prof. che avrai in orario oggi\n\n"
                f"{TOMORROWCLASSES} : mostra i prof. che avrai in orario domani\n\n"
                f"{GETCLASSESFORDAY} : mostra l'orario che avrai in un gioano che specifichi tu\n"
                f"i giorni vanno abbreviati alle loro prime 3 lettere.\n"
                f"Es. {GETCLASSESFORDAY} lun\n\n"
                f"{SETCLASS} : imposta la classe a cui fai parte in modo che ti possa dare l'orario corretto\n"
                f"Andrebbe usato così: {SETCLASS} <la tua classe>\n\n"
                f"Attualmente la versione del mio codice è {VERSION}")

    # Se l'utente chiede i logs (/getlogs)
    elif user_message == ADMINGETLOGS:
        if message.chat.id == OWNERID:
            logs = FSInputFile("resources/garvisLog.log")
            logging.info(f"DOCUMENT SENT:\n{userinfo} << \n resources/garvisLog.log \n----------ENDMSG----------\n")
            await message.answer_document(logs)
        else:
            await message.answer("Non hai i permessi necessari, X-x")
            logging.warning(f"{userinfo} tried {ADMINGETLOGS}")
        return

    # Se l'utente non ha una classe assegnata e ha provato a eseguire un comando che lo richiede
    elif not userClass and (user_message in GETCLASSESCOMANDS):
        text=(f"Uff....\n"                                      
              f"Non riesco a trovare a che classe fai parte O.o\n"
              f"fai {SETCLASS} seguito dalla tua classe per impostarla\n")

    # Se la classe del utente è supportata E ha eseguito un comando in GETCLASSESCOMMAND
    elif not is_class_supported(userClass) and (user_message in GETCLASSESCOMANDS):
        text = (f"Scusa ma non ho l'orario per la tua classe.\n"
                f" Manda un messaggio a Cristian(@matem817) per aggiungerla!")

    # Se l'utente chiede l'orario del giorno
    elif user_message == TODAYCLASSES:
        classes = orario.get_for_day(userClass,today)
        text = f"Buongiorno {user_name}! :D\nL'orario di oggi è:\n{classes}"

    # Se l'utente chiede l'orario del giorno dopo
    elif user_message == TOMORROWCLASSES:
        classes = orario.get_for_day(userClass,(today + 1)%7)
        text = f"Ciao {user_name}!\nL'orario di domani sarà:\n{classes}"

    # Se l'utente chiede l'orario per un giorno specifico
    elif user_message == GETCLASSESFORDAY:
        if len(commandArgs) > 1:
            day = commandArgs[1]
            dayNum, fullDayName = orario.get_day_from_string(day)
            if  dayNum != -1:
                text = (f"L'orario per {fullDayName} è:\n"
                        f"{orario.get_for_day(userClass, dayNum)}")
            else:
                text = (f"Il giorno inserito non sembra essere valido. u.u\n"
                        f"I giorni della settimana vanno abbreviati alle prime 3 lettere. :3\n")


        else:
            text = (f"La sintassi del comando sembra essere sbagliata. x-x\n"
                    f"Andrebbe usato così: {GETCLASSESFORDAY} <lun, mar, mer...>\n"
                    f"es.: {GETCLASSESFORDAY} lun\n")

    # Se l'utente ha scritto gibberish
    else:
        text = (
            "Scusami ma non supporto messaggi al di fuori di comandi x_x\n"
            "Prova a usare:\n"
            "/help"
        )

    logging.info(f"MESSAGE SENT:\n{userinfo} << \n{text}\n----------ENDMSG----------\n")
    await message.answer(text)

