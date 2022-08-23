import os


class Emoji:
    ROCKET = "\U0001F680"
    CHECK_MARK = "\U00002705"
    CROSS_MARK = "\U0000274C"


def exec_sh(command: str) -> int:
    return os.system(command)


def free_storage():
    for item in ["image", "container"]:
        exec_sh(f"docker {item} prune")
