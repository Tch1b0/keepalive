import asyncio
import logging

from src.register_jobs import jobs, bot, metrics

logging.basicConfig(level=logging.INFO)


async def main():
    asyncio.create_task(metrics.update_loop())
    await bot.start()
    await jobs.start()
    try:
        await asyncio.Future()
    except:
        await bot.stop()

asyncio.run(main())
