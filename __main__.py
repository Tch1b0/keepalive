import asyncio
import logging
try:
    import systemd  # type: ignore
except ImportError:
    import src.non_systemd as systemd

from src.register_jobs import jobs, bot, metrics

logging.basicConfig(level=logging.INFO)


async def main():
    asyncio.create_task(metrics.update_loop())
    asyncio.create_task(bot.update_base_message_loop())
    await bot.start()
    await jobs.start()
    systemd.daemon.notify(systemd.daemon.Notification.READY)
    try:
        await asyncio.Future()
    except:
        await bot.stop()

asyncio.run(main())
systemd.daemon.notify(systemd.daemon.Notification.STOPPING)
