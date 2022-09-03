import logging
from docker import DockerClient
import asyncio
import shutil

log = logging.getLogger()

class Metrics:
    storage_total: int
    storage_left: int
    storage_used: int
    running_container_count: int

    def __init__(self, docker_client: DockerClient):
        self.update_loop_active = False
        self.docker_client = docker_client
        self.collect_metrics()

    def collect_metrics(self):
        log.info("Collecting metrics")
        disk_usage = shutil.disk_usage("/")
        self.storage_total, self.storage_used, self.storage_left = [
            x // (2**30) for x in disk_usage]
        self.running_container_count = len(
            self.docker_client.containers.list())

    async def update_loop(self):
        if self.update_loop_active:
            return

        self.update_loop_active = True
        while self.update_loop_active:
            self.collect_metrics()
            await asyncio.sleep(60)
