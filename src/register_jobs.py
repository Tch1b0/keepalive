import logging
import os
import docker
from dotenv import load_dotenv
from src.core.utility import free_storage, time_in_seconds

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


@jobs.register(time_in_seconds(hours=1))
async def check_storage():
    if metrics.storage_left/metrics.storage_total < .1 or metrics.storage_left < 2:
        question = f"Storage is low: only {metrics.storage_left} GB left. Clear dangling docker images/containers?"
        if await bot.decide(question, ["yes", "no"]) == 0:
            free_storage()
