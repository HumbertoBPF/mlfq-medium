import time
from collections import deque
from datetime import datetime
from typing import List, Tuple


def is_overlap(i1, i2):
    return i1[0] < i2[1] and i2[0] < i1[1]


class Job:
    def __init__(self, job_id: str, execution_time: int, color: str, arriving_time: int = 0, io_requests: List[Tuple[int, int]] = None):
        if io_requests is None:
            io_requests = []

        if execution_time <= 0:
            raise AttributeError("The execution time of a job must be positive")

        if arriving_time < 0:
            raise AttributeError("The arriving time of a job must be non-negative")

        self.job_id = job_id
        self.execution_time = execution_time
        self.color = color
        self.arriving_time = arriving_time

        for io_request in io_requests:
            lower_bound = io_request[0]
            upper_bound = io_request[1]

            if lower_bound < arriving_time:
                raise AttributeError(f"Invalid lower bound: {lower_bound}")

            if upper_bound > arriving_time + execution_time:
                raise AttributeError(f"Invalid upper bound: {upper_bound}")

            if lower_bound >= upper_bound:
                raise AttributeError(f"Invalid interval: ({lower_bound}, {upper_bound})")

        io_requests_sorted = sorted(io_requests, key=lambda x: x[0])

        for i in range(len(io_requests_sorted) - 1):
            io_request_1 = io_requests_sorted[i]
            io_request_2 = io_requests_sorted[i + 1]

            if is_overlap(io_request_1, io_request_2):
                raise AttributeError(f"Overlapping I/O requests: ({io_request_1[0]}, {io_request_1[1]}) and ({io_request_2[0]}, {io_request_2[1]})")

        self.io_requests = deque()

        for io_request in io_requests_sorted:
            self.io_requests.append(io_request)

    def run(self, delta_t):
        print(f"Start running job {self.job_id} at starting time = {datetime.now()}")
        time.sleep(delta_t)
        print(f"Finished running job {self.job_id} at ending time = {datetime.now()}")

    def __lt__(self, other):
        if not isinstance(other, Job):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.job_id < other.job_id

    def __str__(self):
        return f"Job ID: {self.job_id} - Execution time: {self.execution_time} - Arriving time: {self.arriving_time}"

    def __repr__(self):
        return f"Job ID: {self.job_id} - Execution time: {self.execution_time} - Arriving time: {self.arriving_time}"
