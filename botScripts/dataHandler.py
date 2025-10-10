import json
import os


class DataHandler:
    FILE_PATH = "resources/userClasses.json"

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
                # Se il file è vuoto o corrotto, ripristina un dizionario vuoto
                self.usersClassesJson = {}

    def get_user_class(self, userChatId: int):
        return self.usersClassesJson.get(str(userChatId), False)

    def set_user_class(self, userChatId: int, userClass: str):
        userChatId = str(userChatId)
        self.usersClassesJson[userChatId] = userClass.upper()

        with open(self.FILE_PATH, "w") as f:
            json.dump(self.usersClassesJson, f, indent=4)

def is_class_supported(userClass: str):
    with open("resources/supportedClasses.json") as f:
        supportedClasses = json.load(f)
        if userClass in supportedClasses:
            return True
        else:
            return False


if __name__ == "__main__":
    handler = DataHandler()
    handler.set_user_class(500, "5f")
    print(handler.get_user_class(500))

