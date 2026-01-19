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

    def get_user_class(self, userChatId: int):
        return self.usersClassesJson.get(str(userChatId), False)

    def set_user_class(self, userChatId: int, userClass: str):
        userChatId = str(userChatId)
        self.usersClassesJson[userChatId] = userClass.upper()

        with open(USERCLASSES, "w") as f:
            json.dump(self.usersClassesJson, f, indent=4)

def is_class_supported(userClass: str):
    with open(SUPPORTEDCLASSES) as f:
        supported_classes = json.load(f)
        if userClass in supported_classes:
            return True
        else:
            return False

def is_user_admin(userId: int) -> bool:
    with open(ADMINLIST) as f:
        admin_list = json.load(f)
        admin=False
        for i in admin_list:
            admin= admin or int(i) == userId
        return admin

if __name__ == "__main__":
    handler = ClassDataHandler()
    handler.set_user_class(500, "5f")
    print(handler.get_user_class(500))

