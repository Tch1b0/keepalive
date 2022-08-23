import docker
import asyncio
import logging

from src.jobs import Jobs
from src.metrics import Metrics
from src.utility import decide_bool, free_storage, inform

log = logging.getLogger()
logging.basicConfig(level=logging.INFO)

docker_client = docker.from_env()
jobs = Jobs()
metrics = Metrics()


@jobs.register(5, False)
async def check_storage():
    metrics.collect_metrics()
    free_percentage: float = metrics.storage_left/metrics.storage_total
    if free_percentage <= 0.1 or metrics.storage_left <= 1:
        inform(
            f"Warning: Only {metrics.storage_left} GB of {metrics.storage_total} left on the device")
        if decide_bool("Prune docker containers and images for storage?"):
            old_left = metrics.storage_left
            free_storage()
            metrics.collect_metrics()
            inform(f"Space reclaimed: {old_left - metrics.storage_left} GB")


# let the jobs execute forever
async def main():
    await jobs.start()
    await asyncio.Future()

asyncio.run(main())
