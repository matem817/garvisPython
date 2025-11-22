import asyncio
from botScripts.commandHandler import command_handler

class Message:
    def __init__(self):
        self.text=input(f"MESSAGE TO SENT TO BOT>>>>")

    class chat:
        full_name="Cristian Salis"
        first_name="Cristian"
        id=6089716018

    async def answer(self, _text):
        print(f"\033[93mFROM BOT>>>\n{_text}\033[0m")


async def main():
    await command_handler(Message())

if __name__ == '__main__':
    while True:
        asyncio.run(main())