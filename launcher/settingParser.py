import json
import filepaths as fp
class ReadSettings:
    def __init__(self):
        if not fp.SETTINGSFILE.exists():
            with fp.SETTINGSFILE.open("w") as f:
                json.dump({"token": None}, f, indent=4)
        with fp.SETTINGSFILE.open("r") as f:
            self.SETTINGS = json.load(f)
            self.token = self.SETTINGS["token"]


def write_setting(setting, value):
    settings=None
    with fp.SETTINGSFILE.open("r") as f:
        settings = json.load(f)
    with fp.SETTINGSFILE.open("w") as f:
        settings[setting] = value
        json.dump(settings, f, indent=4)
