import psutil
import time
from config import RAM_TRACKING_INTERVAL
from threading import Thread


class RamTracker(Thread):
    """This class supports monitoring RAM usage of a process within the testbed."""
    def __init__(self, pid):
        Thread.__init__(self)
        self.process = psutil.Process(pid)
        self.ram_usage = []
        self.track = True

    def get_ram_usage(self):
        measured, mem = False, 0
        while not measured:
            try:
                mem = self.process.memory_info().rss
                measured = True
            except OSError:
                pass
        return mem

    def get_ram_usage_mb(self):
        return self.get_ram_usage() / 1024 / 1024

    def get_ram_usage_gb(self):
        return self.get_ram_usage_mb() / 1024

    def run(self):
        while self.track:
            self.ram_usage.append(self.get_ram_usage())
            time.sleep(RAM_TRACKING_INTERVAL)
