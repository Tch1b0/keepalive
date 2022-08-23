import asyncio
import logging
from typing import Callable, Coroutine

JobCallable = Coroutine

log = logging.getLogger()


class Job:
    # job should run every `timeout` seconds
    callback: JobCallable
    timeout: float
    active: bool
    run_initially: bool

    def __init__(self, callback: JobCallable, timeout: float, run_initially: bool) -> None:
        self.callback = callback
        self.timeout = timeout
        self.active = False
        self.run_initially = run_initially

    async def start(self) -> None:
        """
        start the job loop
        """
        self.active = True
        if self.run_initially:
            await self.callback()
        asyncio.create_task(self.job_loop())

    async def job_loop(self) -> None:
        while self.active:
            await asyncio.sleep(self.timeout)
            # double check of `active` is required, because it might have changed
            # while the sleep took place
            if self.active:
                log.info(f"Executing job: {self.callback.__name__}")
                await self.callback()

    def stop(self) -> None:
        """
        stop the job loop
        """
        self.active = False


class Jobs:
    jobs: list[Job] = []

    def register(self, timeout: float, run_initially: bool = True) -> Callable[[JobCallable], None]:
        def inner(callable: JobCallable) -> None:
            job = Job(callable, timeout, run_initially)
            self.jobs.append(job)

        return inner

    async def start(self):
        """
        start all jobs
        """
        for job in self.jobs:
            if not job.active:
                await job.start()
