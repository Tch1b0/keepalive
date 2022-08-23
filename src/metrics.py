import shutil


class Metrics:
    storage_total: int
    storage_left: int
    storage_used: int

    def __init__(self):
        self.collect_metrics()

    def collect_metrics(self):
        disk_usage = shutil.disk_usage("/")
        self.storage_total, self.storage_used, self.storage_left = [
            x // (2**30) for x in disk_usage]
