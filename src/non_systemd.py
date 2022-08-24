"""
this file will be loaded if the systemd module is not installed.

the code in here just works as a placeholder, 
so that nothing breaks when running on a non-linux or non-systemd device.
"""

from enum import Enum, auto


class Daemon:
    def notify(content: str, *args):
        pass

    class Notification(Enum):
        READY = auto()
        STATUS = auto()
        STOPPING = auto()

daemon = Daemon()
