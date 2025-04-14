from typing import List, Tuple

from common.job import Job
from common.plotter import Plotter

TIMER_INTERRUPT = 1


class JobQueue:
    def __init__(self, jobs: List[Job], next_job: int):
        self.jobs = jobs
        self.next_job = next_job


class MLFQScheduler(Plotter):
    def __init__(self, n_queues):
        super().__init__()

        self.n_queues = n_queues
        self.queues: List[JobQueue] = [JobQueue([], 0) for _ in range(n_queues)]
        self.incoming_jobs = []

    def _get_highest_priority(self) -> int | None:
        """
        Gets the priority of the queue to be processed next.
        :return: the index of the queue to be processed next
        """
        for i in range(self.n_queues - 1, -1, -1):
            if len(self.queues[i].jobs) > 0:
                return i

        return None

    def _run_queue_in_round_robin(self, priority: int):
        """
        Runs the queue with the given priority in Round Robin.
        :param priority: priority of the queue
        :return:
        """
        job_queue = self.queues[priority]
        queued_jobs = job_queue.jobs
        job_index = job_queue.next_job

        # Run job
        running_job = queued_jobs[job_index]
        delta_t = min(running_job.execution_time, TIMER_INTERRUPT)
        running_job.run(delta_t=delta_t)

        # Update scheduler's state
        self._update_plot(delta_t=delta_t, plot_color=running_job.color, idle=False)
        self.t += delta_t

        # The execution_time attribute stores the time the job will run until completion, so it must be updated
        # every time a job runs
        remaining_time = running_job.execution_time - delta_t
        running_job.execution_time = remaining_time
        queued_jobs[job_index] = running_job

        # Remove the job if it is completed
        if remaining_time == 0:
            del queued_jobs[job_index]

        # Update the job index to loop through the queue
        job_index -= 1

        if job_index < 0:
            job_index = len(queued_jobs) - 1

        # Update the scheduler queues
        job_queue.jobs = queued_jobs
        job_queue.next_job = job_index
        self.queues[priority] = job_queue

    def _check_for_incoming_jobs(self):
        """
        Checks whether there is an incoming job that should be scheduled in the current timestamp, and, if there is,
        adds it to the appropriate queue.
        :return:
        """
        while len(self.incoming_jobs) > 0:
            job, priority = self.incoming_jobs[-1]

            if job.arriving_time <= self.t:
                self.incoming_jobs.pop()
                self.queues[priority].jobs.append(job)
                continue

            break

    def run(self, jobs: List[Tuple[Job, int]]):
        # Validate priority values
        for job, priority in jobs:
            if priority >= self.n_queues or priority < 0:
                raise AttributeError("Priority cannot be negative")

        # Jobs are sorted by arrival time to make adding jobs to the scheduler easier
        self.incoming_jobs = sorted(jobs, key=lambda job: -job[0].arriving_time)

        # Insert jobs arriving at t = 0 in the corresponding queues
        self._check_for_incoming_jobs()

        highest_priority = self._get_highest_priority()

        while (len(self.incoming_jobs) > 0) or (highest_priority is not None):
            # If there is no job currently scheduled, only increment the timestamp
            if highest_priority is None:
                self.t += TIMER_INTERRUPT
            # If there are jobs scheduled, run them in Round Robin
            else:
                self._run_queue_in_round_robin(priority=highest_priority)

            self._check_for_incoming_jobs()
            highest_priority = self._get_highest_priority()

        self._plot_scheduling()
