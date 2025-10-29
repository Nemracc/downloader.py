import asyncio
import time

class BandwidthMonitor:
    def __init__(self, update_interval=2):
        self.total_bytes = 0
        self.last_check = time.time()
        self.speed_mbps = 0
        self.update_interval = update_interval
        self._lock = asyncio.Lock()

    async def add_bytes(self, num_bytes):
        async with self._lock:
            self.total_bytes += num_bytes

    async def measure_speed(self):
        while True:
            await asyncio.sleep(self.update_interval)
            async with self._lock:
                now = time.time()
                elapsed = now - self.last_check
                self.speed_mbps = (self.total_bytes / elapsed) / (1024 * 1024)
                self.total_bytes = 0
                self.last_check = now

    def get_speed(self):
        return round(self.speed_mbps, 2)
