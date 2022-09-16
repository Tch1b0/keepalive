import logging
from subprocess import call

log = logging.getLogger()


class Emoji:
    ROCKET = "\U0001F680"
    CHECK_MARK = "\U00002705"
    CROSS_MARK = "\U0000274C"


def time_in_seconds(
    seconds: float = 0, minutes: float = 0, hours: float = 0, days: float = 0
) -> float:
    """
    converts the given time into seconds

    :examples:
    ```py
    time_in_seconds(minutes=1)          # => 60
    time_in_seconds(hours=1)            # => 3600
    time_in_seconds(minutes=3, hours=2) # => 7330
    ```
    """
    return seconds + minutes * 60 + hours * 60 * 60 + days * 60 * 60 * 24


def exec_sh(command: str) -> tuple[int, str]:
    """
    execute shell command
    """
    log.info(f'Executing shell command "{command}"')
    code = call(command, shell=True)
    return code
