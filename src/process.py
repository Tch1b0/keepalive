import signal

from src.core.utility import idle


class Process:
    def __init__(self) -> None:
        self.is_terminating = False
        for sig in [signal.SIGTERM, signal.SIGINT]:
            signal.signal(sig, self.exit_gracefully)

    def exit_gracefully(self, *_):
        self.is_terminating = True

    async def termination(self):
        """
        sleep until the process is being terminated.

        Method does NOT terminate the process like the name might suggest.
        The name was chosen because of the syntactic sugar `await process.termination()`
        """
        while not self.is_terminating:
            await idle(0.1)
