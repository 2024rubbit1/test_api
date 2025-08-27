import time


class CustomSnowflake:
    def __init__(self, worker_id=1, datacenter_id=1):
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = 0
        self.last_timestamp = -1

    def next_id(self):
        timestamp = int(time.time() * 1000)
        if timestamp < self.last_timestamp:
            raise ValueError("Clock moved backwards.")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0x3FFF  # 12位序列号
        else:
            self.sequence = 0
            self.last_timestamp = timestamp

        return ((timestamp << 22) | (self.datacenter_id << 12) | self.sequence)