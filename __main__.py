import asyncio
import logging
from process import Process

from src.register_jobs import jobs, bot, metrics

logging.basicConfig(level=logging.INFO)
process = Process()


async def main():
    asyncio.create_task(metrics.update_loop())
    asyncio.create_task(bot.update_base_message_loop())
    await bot.start()
    await jobs.start()

    await process.termination()
    await bot.stop()

asyncio.run(main())
