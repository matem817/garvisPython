import pathlib as pl

#####FOLDERS#####

PROJECTDIR = pl.Path(__file__).parent.resolve()
LAUNCERDIR = PROJECTDIR / "launcher"

RESOURCEDIR = PROJECTDIR / "resources"

CONSTANTSDIR = RESOURCEDIR / "constants"

DATAFOLDER = RESOURCEDIR / "data"
LOGSFOLDER = RESOURCEDIR / "logs"
USERSDATAFOLDER = RESOURCEDIR / "usersData"

#####FILES#####
SETTINGSFILE = LAUNCERDIR / "settings.json"

ORARIO = DATAFOLDER / "orario.json"
SUPPORTEDCLASSES = DATAFOLDER / "supportedClasses.json"

ADMINLIST = USERSDATAFOLDER / "adminList.json"
USERCLASSES = USERSDATAFOLDER / "userClasses.json"


if __name__ == '__main__':
    raise RuntimeError("This file is only for providing paths to other scripts it should never be run")