import json
import logging
import os

USERSDATAFOLDER= "resources/usersData"
DATAFOLDER= "resources/data"

class ClassDataHandler:
    FILE_PATH = USERSDATAFOLDER + "/userClasses.json"
    def __init__(self):
        self.usersClassesJson = None
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                json.dump({}, f)

        self.load_data()

    def load_data(self):
        with open(self.FILE_PATH, "r") as f:
            try:
                self.usersClassesJson = json.load(f)
            except json.JSONDecodeError:
                logging.error(f"{self.FILE_PATH} Corrupted!!!!!")
                self.usersClassesJson = {}

    def get_user_class(self, userChatId: int):
        return self.usersClassesJson.get(str(userChatId), False)

    def set_user_class(self, userChatId: int, userClass: str):
        userChatId = str(userChatId)
        self.usersClassesJson[userChatId] = userClass.upper()

        with open(self.FILE_PATH, "w") as f:
            json.dump(self.usersClassesJson, f, indent=4)

class NotificationDataHandler:
    FILE_PATH = USERSDATAFOLDER + "/subscriberList.json"

    def __init__(self):
        self.subscribersList: list[int] = []
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                json.dump({}, f)
        self.load_data()

    def load_data(self):
        with open(self.FILE_PATH, "r") as f:
            try:
                self.subscribersList = json.load(f)
            except json.JSONDecodeError:
                logging.error(f"{self.FILE_PATH} Corrupted!!!!!")
                self.subscribersList = []

    def get_subscriber_list(self) -> list[int]:
        return self.subscribersList

    def add_subscriber(self, _subId) -> None:
        self.subscribersList.append(_subId)
        with open(self.FILE_PATH, "w") as f:
            json.dump(self.subscribersList, f, indent=4)

def is_class_supported(userClass: str):
    with open(DATAFOLDER + "/supportedClasses.json") as f:
        supportedClasses = json.load(f)
        if userClass in supportedClasses:
            return True
        else:
            return False

def is_user_admin(userId: int) -> bool:
    with open(USERSDATAFOLDER + "/adminList.json") as f:
        supportedClasses = json.load(f)
        admin=False
        for i in supportedClasses:
            admin= admin or int(i) == userId
        return admin

if __name__ == "__main__":
    handler = ClassDataHandler()
    handler.set_user_class(500, "5f")
    print(handler.get_user_class(500))

