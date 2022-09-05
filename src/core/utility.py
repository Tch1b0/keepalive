import logging
from subprocess import call

log = logging.getLogger()


class Emoji:
    ROCKET = "\U0001F680"
    CHECK_MARK = "\U00002705"
    CROSS_MARK = "\U0000274C"


def time_in_seconds(seconds: float = 0, minutes: float = 0, hours: float = 0, days: float = 0) -> float:
    return seconds + minutes * 60 + hours * 60 * 60 + days * 60 * 60 * 24


def exec_sh(command: str) -> tuple[int, str]:
    """
    execute shell command
    """
    log.info(f"Executing shell command \"{command}\"")
    code = call(command, shell=True)
    return code
