import asyncio
from uuid import UUID, uuid4
from datetime import datetime
from typing import Callable
from telegram import Bot, ChatMember, Message, Chat
from telegram.ext import Updater

from src.core.utility import Emoji, idle


class TelegramBot(Bot):
    chat: Chat
    admin: ChatMember
    admin_id: str
    update_queue: asyncio.Queue
    updater: Updater

    def __init__(
        self,
        token: str,
        admin_id: str,
    ):
        super().__init__(token)

        self.currently_interacting: bool = False
        self.informants: list[Callable[[], str]] = []
        self.decision_stack: list[UUID] = []
        self.base_message: Message
        self.admin_id = admin_id
        self.update_queue = asyncio.Queue()
        self.updater = Updater(self, self.update_queue)

    async def start(self) -> None:
        self.admin = await self.get_chat_member(self.admin_id, self.admin_id)
        self.chat = await self.get_chat(self.admin_id)
        self.base_message = await self.chat.send_message(self.get_info_board())
        await self.updater.initialize()
        await self.updater.start_polling(0.5, drop_pending_updates=True)

    async def stop(self) -> None:
        if self.base_message:
            await self.base_message.delete()

    async def update_base_message(self):
        content = self.get_info_board()
        if content != self.base_message.text:
            await self.base_message.edit_text(content)

    async def update_base_message_loop(self):
        while True:
            await idle(60)
            await self.update_base_message()

    def get_info_board(self) -> str:
        msg = (
            f"{Emoji.ROCKET} keepalive is currently keeping alive\n"
            + f"Last ping: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        )
        msg += "\n".join(f() for f in self.informants)
        return msg

    async def decide(self, question: str, answers: list[str]) -> int:
        decision_id = uuid4()
        if self.currently_interacting:
            self.decision_stack.append(decision_id)

        # wait until no interaction is done
        while self.currently_interacting and (
            len(
                self.decision_stack) != 0 and self.decision_stack[0] != decision_id
        ):
            await idle()

        if len(self.decision_stack) != 0:
            self.decision_stack.pop()

        self.currently_interacting = True
        msg = await self.chat.send_poll(question, answers)
        # wait until the given update is received
        while not hasattr(await self.update_queue.get(), "poll"):
            await idle()

        poll = await msg.stop_poll()
        for i, answer in enumerate(poll.options):
            if answer.voter_count != 0:
                await msg.delete()
                self.update_queue.task_done()
                return i

        self.update_queue.task_done()
        await msg.delete()
        raise Exception("Poll was not answered")

    async def yesno(self, question: str) -> bool:
        return (await self.decide(question, ["yes", "no"])) == 0
