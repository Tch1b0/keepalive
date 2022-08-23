import asyncio
import shutil


class Metrics:
    update_loop: bool = False

    storage_total: int
    storage_left: int
    storage_used: int

    def __init__(self):
        self.collect_metrics()

    def collect_metrics(self):
        disk_usage = shutil.disk_usage("/")
        self.storage_total, self.storage_used, self.storage_left = [
            x // (2**30) for x in disk_usage]

    async def update_loop(self):
        if self.update_loop:
            return

        self.update_loop = True
        while self.update_loop:
            self.collect_metrics()
            asyncio.sleep(60)
