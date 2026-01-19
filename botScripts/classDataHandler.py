import json
import logging
import os
from filepaths import USERCLASSES, ADMINLIST, SUPPORTEDCLASSES

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

    def get_user_class(self, user_chat_id: int):
        return self.usersClassesJson.get(str(user_chat_id), False)

    def set_user_class(self, user_chat_id: int, user_class: str):
        user_chat_id = str(user_chat_id)
        self.usersClassesJson[user_chat_id] = user_class.upper()

        with open(USERCLASSES, "w") as f:
            json.dump(self.usersClassesJson, f, indent=4)

def is_class_supported(user_class: str):
    with open(SUPPORTEDCLASSES) as f:
        supported_classes = json.load(f)
        if user_class in supported_classes:
            return True
        else:
            return False

def is_user_admin(user_id: int) -> bool:
    with open(ADMINLIST) as f:
        admin_list = json.load(f)
        admin=False
        for i in admin_list:
            admin= admin or int(i) == user_id
        return admin

if __name__ == "__main__":
    handler = ClassDataHandler()
    handler.set_user_class(500, "5f")
    print(handler.get_user_class(500))

