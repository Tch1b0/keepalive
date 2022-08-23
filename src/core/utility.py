import os


class Emoji:
    ROCKET = "\U0001F680"
    CHECK_MARK = "\U00002705"
    CROSS_MARK = "\U0000274C"


def time_in_seconds(seconds: float = 0, minutes=0, hours=0, days=0) -> float:
    return seconds + minutes * 60 + hours * 60 * 60 + days * 60 * 60 * 24


def exec_sh(command: str) -> int:
    return os.system(command)


def free_storage():
    for item in ["image", "container"]:
        exec_sh(f"docker {item} prune -f")
