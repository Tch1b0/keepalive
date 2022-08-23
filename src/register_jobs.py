import logging
import os
import docker
from dotenv import load_dotenv

from src.core.jobs import Jobs
from src.core.metrics import Metrics
from src.core.telegrambot import TelegramBot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

log = logging.getLogger()

docker_client = docker.from_env()
jobs = Jobs()
metrics = Metrics()
bot = TelegramBot(BOT_TOKEN, ADMIN_ID)

bot.informants.append(
    lambda: f"Storage: {metrics.storage_left} GB of {metrics.storage_total} GB left")


@jobs.register(5, False)
async def check_storage():
    pass
