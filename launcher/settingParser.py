import json
import filepaths as fp
class ReadSettings:
    def __init__(self):
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
