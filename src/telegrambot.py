import asyncio
from datetime import datetime, timedelta
from telegram import Bot, User, Message, Chat
from telegram.ext import Updater
from telegram.request import BaseRequest

try:
    from src.utility import Emoji
except:
    from utility import Emoji

ADMIN_CHAT_ID = "188838345"
BOT_TOKEN = "5337387114:AAFKz7jBGQi76RqyefHYfxurqYqOWOVuda8"


class TelegramBot(Bot):
    chat: Chat
    admin: User
    update_queue: asyncio.Queue
    updater: Updater
    base_message: Message = None
    currently_interacting: bool = False

    def __init__(self, token: str, base_url: str = "https://api.telegram.org/bot", base_file_url: str = "https://api.telegram.org/file/bot", request: BaseRequest = None, get_updates_request: BaseRequest = None, private_key: bytes = None, private_key_password: bytes = None):
        super().__init__(token, base_url, base_file_url, request,
                         get_updates_request, private_key, private_key_password)

        self.update_queue = asyncio.Queue()
        self.updater = Updater(self, self.update_queue)

    async def start(self) -> None:
        self.admin = self.get_chat_member(ADMIN_CHAT_ID, ADMIN_CHAT_ID)
        self.chat = await self.get_chat(ADMIN_CHAT_ID)
        self.base_message = await self.chat.send_message(self.get_info_board())
        await self.updater.initialize()
        await self.updater.start_polling(.5)

    async def stop(self) -> None:
        if self.base_message:
            await self.base_message.delete()

    async def update_base_message(self):
        content = self.get_info_board()
        if content != self.base_message.text:
            await self.base_message.edit_text(content)

    def get_info_board(self) -> str:
        return f"{Emoji.ROCKET} keepalive is currently keeping alive\n" + \
               f"Last ping: {datetime.now().strftime('%d.%m.%Y %H:%M')}"

    async def decide(self, question: str, answers: list[str]) -> int:
        # wait until no interaction is done
        while self.currently_interacting:
            await asyncio.sleep(1)

        self.currently_interacting = True
        msg = await self.chat.send_poll(question, answers)
        # wait until the given update is received
        while not hasattr(await self.update_queue.get(), "poll"):
            pass
        poll = await msg.stop_poll()
        for i, answer in enumerate(poll.options):
            if answer.voter_count != 0:
                await msg.delete()
                return i

        await msg.delete()
        raise Exception("Poll was not answered")


bot = TelegramBot(BOT_TOKEN)


async def main():
    await bot.start()
    print(await bot.decide("Favourite Food?", ["Pizza", "Pasta"]))
    try:
        await asyncio.Future()
    except:
        await bot.stop()

asyncio.run(main())
