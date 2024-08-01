import logging
import os
import psutil
import docker
from dotenv import load_dotenv

from src.core.utility import exec_sh, time_in_seconds
from src.core.jobs import Jobs
from src.core.metrics import Metrics
from src.core.telegrambot import TelegramBot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if None in [BOT_TOKEN, ADMIN_ID]:
    print("BOT_TOKEN or ADMIN_ID not defined")
    exit()

log = logging.getLogger()
docker_client = docker.from_env()
jobs = Jobs()
metrics = Metrics(docker_client)
bot: TelegramBot = TelegramBot(BOT_TOKEN, ADMIN_ID)

bot.informants.append(
    lambda: f"Storage: {metrics.storage_left} GB of {metrics.storage_total} GB left"
)
bot.informants.append(
    lambda: f"Running Containers: {metrics.running_container_count}")
bot.informants.append(
    lambda: f"Current CPU usage: {psutil.cpu_percent() * 100:.2f}%"
)


@jobs.register(time_in_seconds(hours=1))
# JOB: storage checker
async def check_storage():
    if metrics.storage_left / metrics.storage_total < 0.1 or metrics.storage_left < 2:
        question = f"Storage is low: only {metrics.storage_left} GB left. Clear dangling docker images/containers?"
        if await bot.yesno(question):
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
        question = f"Nextcloud containers are not running. Restart the nextcloud and the database container?"
        if await bot.yesno(question):
            for container in nx_containers:
                container.restart()


@jobs.register(time_in_seconds(days=3), run_initially=False)
# JOB: apdater
async def update_packages():
    update_result = exec_sh("apt-get update")
    question = f"`apt-get update` returned status code {update_result.returncode}. Run `apt-get upgrade`?"
    if await bot.yesno(question):
        exec_sh("apt-get upgrade -y")

@jobs.register(time_in_seconds(days=5), run_initially=False)
# JOB: resend message
async def resend_status_message():
    await bot.stop()
    await bot.start()

@jobs.register(time_in_seconds(seconds=30), run_initially=True)
# JOB: check CPU usage
async def check_cpu_usage(cpu_high=[False]):
    cpu_usage = psutil.cpu_percent()
    if cpu_usage > 0.8:
        if not cpu_high[0]:
            cpu_high[0] = True
            return
        decision = bot.decide("CPU has been over 80%% for at least 1 minute", ["ignore", "reboot", "shutdown"])
        match decision:
            case 1:
                os.system("reboot")
            case 2:
                os.system("shutdown now -h")
    else:
        cpu_high[0] = False
