import logging
import os
import docker
from dotenv import load_dotenv
from src.core.utility import exec_sh, time_in_seconds

from src.core.jobs import Jobs
from src.core.metrics import Metrics
from src.core.telegrambot import TelegramBot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

log = logging.getLogger()
docker_client = docker.from_env()
jobs = Jobs()
metrics = Metrics(docker_client)
bot = TelegramBot(BOT_TOKEN, ADMIN_ID)

bot.informants.append(
    lambda: f"Storage: {metrics.storage_left} GB of {metrics.storage_total} GB left")
bot.informants.append(
    lambda: f"Running Containers: {metrics.running_container_count}"
)


@jobs.register(time_in_seconds(hours=1))
# JOB: storage checker
async def check_storage():
    if metrics.storage_left/metrics.storage_total < .1 or metrics.storage_left < 2:
        question = f"Storage is low: only {metrics.storage_left} GB left. Clear dangling docker images/containers?"
        if await bot.decide(question, ["yes", "no"]) == 0:
            image_prune_result = docker_client.images.prune()
            container_prune_result = docker_client.containers.prune()
            log.info(f"Pruned: {image_prune_result}")
            log.info(f"Pruned: {container_prune_result}")


@jobs.register(time_in_seconds(minutes=1))
# JOB: cloud verifier
async def verify_cloud():
    nx_containers = []
    for container in docker_client.containers.list(True):
        if container.name in ["nextcloud", "nextcloud-db"]:
            nx_containers.append(container)

    if any(c.status != "running" for c in nx_containers):
        question = f"Nexcloud containers are not running. Restart the nextcloud and the database container?"
        if await bot.decide(question, ["yes", "no"]) == 0:
            for container in nx_containers:
                container.restart()


@jobs.register(time_in_seconds(days=3), run_initially=False)
# JOB: apdater
async def update_packages():
    # TODO: process return code
    code = exec_sh("apt-get update")
    if await bot.decide(f"`apt-get update` returned status code {code}. Run `apt-get upgrade`?", ["yes", "no"]) == 0:
        # TODO: process return code
        code = exec_sh("apt-get upgrade -y")
