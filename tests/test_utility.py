import import_fix

from src.process import Process
from src.core.utility import time_in_seconds


def test_process():
    p = Process()
    assert p.is_terminating == False
    p.exit_gracefully()
    assert p.is_terminating == True


def test_time():
    assert time_in_seconds(1) == 1
    assert time_in_seconds(seconds=5) == 5
    assert time_in_seconds(minutes=1) == 60
    assert time_in_seconds(hours=1) == 60**2
    assert time_in_seconds(days=1) == 60**2 * 24

    assert (
        time_in_seconds(seconds=5, minutes=15, hours=2, days=1)
        == 5 + 15 * 60 + 2 * 60**2 + 60**2 * 24
    )
