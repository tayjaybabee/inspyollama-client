from datetime import datetime
from inspyollama_client.log_engine import ROOT_LOGGER as PARENT_LOGGER


MOD_LOGGER = PARENT_LOGGER.get_child('helpers')


class TimedText:
    """
    A class to hold timed text strings for use by spinners
    """
    def __init__(self, text):
        self.text = text
        self._start = datetime.now()

    def __str__(self):
        now = datetime.now()
        delta = now - self._start
        return f"{self.text} ({round(delta.total_seconds(), 1)}s)"
