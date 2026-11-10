import json
import filepaths as fp

class ReadSettings:
    def __init__(self):
        if not fp.SETTINGSFILE.exists():
            with fp.SETTINGSFILE.open("w") as f:
                json.dump({}, f, indent=4)
        with fp.SETTINGSFILE.open("r") as f:
            self.SETTINGS = json.load(f)
            self.token = self.SETTINGS["token"] or None
            self.dbpsw = self.SETTINGS["dbpsw"] or None
            self.dbusr = self.SETTINGS["dbusr"] or None
            self.dbhost = self.SETTINGS["dbhost"] or None
            self.dbname = self.SETTINGS["dbname"] or None


def write_setting(setting, value):
    settings=None
    with fp.SETTINGSFILE.open("r") as f:
        settings = json.load(f)
    with fp.SETTINGSFILE.open("w") as f:
        settings[setting] = value
        json.dump(settings, f, indent=4)
