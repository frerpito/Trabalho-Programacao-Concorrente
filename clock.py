import time
import threading
from constants import CLOCK_TICK_MS

class GlobalClock(threading.Thread):
    def __init__(self):
        super().__init__()
        self.tick = 0
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.running = True

    def run(self):
        while self.running:
            time.sleep(CLOCK_TICK_MS / 1000.0)
            with self.condition:
                self.tick += 1
                self.condition.notify_all()
                
    def stop(self):
        self.running = False
        with self.condition:
            self.condition.notify_all()
            
    def wait_ticks(self, num_ticks):
        with self.condition:
            target = self.tick + num_ticks
            while self.tick < target and self.running:
                self.condition.wait()
