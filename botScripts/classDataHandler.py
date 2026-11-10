import datetime
import json
import logging
import os
from filepaths import USERCLASSES, ADMINLIST, SUPPORTEDCLASSES
import mysql.connector
import launcher.settingParser as sP


mydb = mysql.connector.connect(
    host=sP.ReadSettings().dbhost,
    user=sP.ReadSettings().dbusr,
    passwd=sP.ReadSettings().dbpsw,
    database=sP.ReadSettings().dbname,
)
myC = mydb.cursor()

class ClassDataHandler:
    def __init__(self):
        self.usersClassesJson = None
        if not os.path.exists(USERCLASSES):
            with open(USERCLASSES, "w") as f:
                json.dump({}, f)
        self.load_data()

    def load_data(self):
        with open(USERCLASSES, "r") as f:
            try:
                self.usersClassesJson = json.load(f)
            except json.JSONDecodeError:
                logging.error(f"{USERCLASSES} Corrupted!!!!!")
                self.usersClassesJson = {}

    def get_user_class(self, user_chat_id: int) -> str | None:
        myC.execute(
            "SELECT classeUtente FROM users WHERE telegramID = %s",
            (user_chat_id,),
        )
        row = myC.fetchone()
        return row[0] if row else None

    def set_user_class(self, user_chat_id: int, user_class: str):
        if self.get_user_class(user_chat_id) is None:
            print("INSERTING USER")
            now=datetime.datetime.now().strftime("%Y-%m-%d")
            myC.execute(
                "INSERT INTO `users` VALUES (%s,%s,%s,%s,%s)",
                (user_chat_id,user_class,0,now,0),
            )
        else:
            print("UPDATING USER")
            myC.execute(
                "UPDATE users SET classeUtente=%s WHERE telegramID=%s;",
                (user_class, user_chat_id,),
            )
        mydb.commit()

def is_class_supported(user_class: str):
    with open(SUPPORTEDCLASSES) as f:
        supported_classes = json.load(f)
        return user_class in supported_classes

def is_user_admin(user_id: int) -> bool:
    myC.execute(
        "SELECT lvlAdmin FROM users WHERE telegramID = %s",
        (user_id,),
    )
    row = myC.fetchone()
    return row[0]>=2 if row else False

if __name__ == "__main__":
    raise RuntimeError("This file is only for providing class data handling to other scripts it should never be run")

