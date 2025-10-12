import json
import gc

weekDay = ["lun","mar","mer","gio","ven", "sab","dom"]

with open("resources/orario.json") as f:
    orarioJson = json.loads(f.read())

def get_day_from_string(day: str) -> int:
    if not day in weekDay:
        return -1
    return weekDay.index(day)

def get_for_day(class_, day) -> str:
    classjson = orarioJson[class_]
    orario = classjson[weekDay[day]]
    out = ""
    for i in orario:
        out += f"   {i}:{orario[i]}\n"
    return out


if __name__ == "__main__":
    print(get_for_day(0))

gc.collect()