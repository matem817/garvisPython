import json
from logging import exception

from filepaths import ORARIO

weekDay = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]
fullWeekDay = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

with open(ORARIO) as f:
    orarioJson = json.loads(f.read())


def get_day_from_string(day: str) -> tuple[int, str]:
    if not day in weekDay:
        return -1, ""
    day_index = weekDay.index(day)
    return day_index, fullWeekDay[day_index]


def get_for_day(class_: str, day: int) -> str:
    classjson = orarioJson[class_]
    orario = classjson[weekDay[day]]
    out = ""
    for i in orario:
        out += f"   {i}:{orario[i]}\n"
    return out


if __name__ == "__main__":
    raise exception("Do not run this file directly!")