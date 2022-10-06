import asyncio
import logging

from src.process import Process
from src.register_jobs import jobs, bot, metrics

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
process = Process()


async def main():
    log.info("starting loops update loops")
    asyncio.create_task(metrics.update_loop())
    asyncio.create_task(bot.update_base_message_loop())

    log.info("starting bot")
    await bot.start()

    log.info("starting jobs")
    await jobs.start()

    await process.termination()
    log.info("terminating process")
    await bot.stop()


asyncio.run(main())
