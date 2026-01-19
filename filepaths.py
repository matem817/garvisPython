import pathlib as pl

PROJECTDIR = pl.Path(__file__).parent.resolve()
LAUNCERDIR = PROJECTDIR / "launcher"

RESOURCEDIR = PROJECTDIR / "resources"

DATAFOLDER = RESOURCEDIR / "data"
USERSDATAFOLDER = RESOURCEDIR / "users"

SETTINGSFILE = LAUNCERDIR / "settings.json"



if __name__ == '__main__':
    raise Exception("This file is only for providing paths to other scripts it should never be run")