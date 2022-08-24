import asyncio
from uuid import UUID, uuid4
from datetime import datetime
from typing import Callable
from telegram import Bot, User, Message, Chat
from telegram.ext import Updater
from telegram.request import BaseRequest

from src.core.utility import Emoji


class TelegramBot(Bot):
    chat: Chat
    admin: User
    admin_id: str
    update_queue: asyncio.Queue
    updater: Updater
    base_message: Message = None

    currently_interacting: bool = False
    informants: list[Callable[[], str]] = []
    decision_stack: list[UUID] = []

    def __init__(self, token: str, admin_id: str, base_url: str = "https://api.telegram.org/bot", base_file_url: str = "https://api.telegram.org/file/bot", request: BaseRequest = None, get_updates_request: BaseRequest = None, private_key: bytes = None, private_key_password: bytes = None):
        super().__init__(token, base_url, base_file_url, request,
                         get_updates_request, private_key, private_key_password)

        self.admin_id = admin_id
        self.update_queue = asyncio.Queue()
        self.updater = Updater(self, self.update_queue)

    async def start(self) -> None:
        self.admin = await self.get_chat_member(self.admin_id, self.admin_id)
        self.chat = await self.get_chat(self.admin_id)
        self.base_message = await self.chat.send_message(self.get_info_board())
        await self.updater.initialize()
        await self.updater.start_polling(.5, drop_pending_updates=True)

    async def stop(self) -> None:
        if self.base_message:
            await self.base_message.delete()

    async def update_base_message(self):
        content = self.get_info_board()
        if content != self.base_message.text:
            await self.base_message.edit_text(content)

    async def update_base_message_loop(self):
        while True:
            await asyncio.sleep(60)
            await self.update_base_message()

    def get_info_board(self) -> str:
        msg = f"{Emoji.ROCKET.value} keepalive is currently keeping alive\n" + \
            f"Last ping: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        msg += "\n".join(f() for f in self.informants)
        return msg

    async def decide(self, question: str, answers: list[str]) -> int:
        decision_id = uuid4()
        if self.currently_interacting:
            self.decision_stack.append(decision_id)

        # wait until no interaction is done
        while self.currently_interacting and (len(self.decision_stack) != 0 and self.decision_stack[0] != decision_id):
            await asyncio.sleep(1)

        if len(self.decision_stack) != 0:
            self.decision_stack.pop()

        self.currently_interacting = True
        msg = await self.chat.send_poll(question, answers)
        # wait until the given update is received
        while not hasattr(await self.update_queue.get(), "poll"):
            asyncio.sleep(1)

        poll = await msg.stop_poll()
        for i, answer in enumerate(poll.options):
            if answer.voter_count != 0:
                await msg.delete()
                self.update_queue.task_done()
                return i

        self.update_queue.task_done()
        await msg.delete()
        raise Exception("Poll was not answered")
