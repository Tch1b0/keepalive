import logging
from enum import Enum, auto
from subprocess import call

log = logging.getLogger()


class Emoji(Enum):
    ROCKET = "\U0001F680"
    CHECK_MARK = "\U00002705"
    CROSS_MARK = "\U0000274C"


class ImportanceLevel(Enum):
    VERY_LOW = auto()
    LOW = auto()
    MEDIUM = auto()
    IMPORTANT = auto()
    URGENT = auto()


def time_in_seconds(seconds: float = 0, minutes=0, hours=0, days=0) -> float:
    return seconds + minutes * 60 + hours * 60 * 60 + days * 60 * 60 * 24


def exec_sh(command: str) -> int:
    log.info(f"Executing shell command \"{command}\"")
    return call(command, shell=True)
