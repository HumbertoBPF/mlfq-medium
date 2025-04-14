import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self):
        self.t = 0
        self.plot_args = []
        _, self.ax = plt.subplots(1)

    def _update_plot(self, delta_t: int, plot_color: str, idle: bool):
        """
        This function updates the scheduling plot (displayed at the end of a run) and must be run every time the
        scheduler completes a cycle (i.e. when running a job or being idle for TIME_INTERRUPT while waiting for an
        incoming job)
        :param delta_t: time range for this fraction of the plot
        :param plot_color: color to be used in this fraction of the plot
        :param idle: whether the scheduler is idle
        :return:
        """
        x = [self.t, self.t + delta_t]
        y_bottom = np.array([0, 0])

        # If the scheduler has no job to run (is idle), nothing must be plotted
        y_top = np.array([int(not idle), int(not idle)])

        self.plot_args.append(x)
        self.plot_args.append(y_top)
        self.plot_args.append(plot_color)

        self.ax.fill_between(x, y_bottom, y_top, where=(y_top > y_bottom), color=plot_color, alpha=0.3)

    def _plot_scheduling(self):
        """
        Finishes building and displays the scheduling plot.
        :return:
        """
        self.ax.plot(*self.plot_args)

        # Configure x axis
        self.ax.set_xlabel('Time (seconds)')
        self.ax.set_xlim([0, self.t])

        # Configure y axis
        self.ax.set_yticklabels([])
        self.ax.set_ylim([0, 2])

        plt.show()
