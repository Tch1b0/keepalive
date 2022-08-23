import asyncio
import logging
from src.jobs import Jobs
from src.metrics import Metrics
from src.utility import decide, inform
import docker

docker_client = docker.from_env()
jobs = Jobs()
metrics = Metrics()


@jobs.register(5, False)
async def check_storage():
    logging.info("Checking storage...")
    metrics.collect_metrics()
    if metrics.storage_left < 50:
        inform(f"Warning: Only {metrics.storage_left} GB left on the device")


# let the jobs execute forever
async def main():
    decide("Which color?", ["red", "purple", "blue"])
    await jobs.start()
    await asyncio.Future()

asyncio.run(main())
