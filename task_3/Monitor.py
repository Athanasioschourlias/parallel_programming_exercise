# import statements go here
import os
import threading
import time
import psutil
import csv
import signal
import logging
import numpy as np
from scipy import stats
import statistics
import random
import matplotlib.pyplot as plt


# Class methods here
class Monitor:
    __num_obj = 0

    def __init__(self, cpu_util, ram_util):
        Monitor.__num_obj += 1
        self.cpu_util = cpu_util
        self.ram_util = ram_util
        self._timestamp = time.time()

    def __call__(self):
        print("CPU utilization: " + str(self.cpu_util))
        print("RAM utilization: " + str(self.ram_util))

    @classmethod
    def get_num_obj(cls):
        return cls.__num_obj

    def get_timestamp(self):
        print(time.ctime(self._timestamp))

    def monitor_cpu(self,stop, time_step=1):
        while True:
            self.cpu_util.append(psutil.cpu_percent(interval=None, percpu=False))
            time.sleep(time_step)
            if stop():
                break

    def monitor_ram(self,stop,  time_step=1):
        while True:
            self.ram_util.append(psutil.virtual_memory()[2])
            time.sleep(time_step)
            if stop():
                break

    def save_cpu_ram(self, filepath, header):
        all_metrics = []
        for cpu, ram in zip(self.cpu_util, self.ram_util):
            two_metrics = []
            two_metrics.append(cpu)
            two_metrics.append(ram)
            all_metrics.append(two_metrics)
            print(two_metrics)

        with open(filepath, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows({'CPU': row[0], 'RAM': row[1]} for row in zip(self.cpu_util, self.ram_util))

    def descriptive_statistics(self, metric):
        if metric.lower() == "cpu":
            data = self.cpu_util
        elif metric.lower() == "ram":
            data = self.ram_util
        else:
            print("Wrong input. Type cpu or ram.")
            return
        print("Min: " + str(stats.describe(data)[1][0]))
        print("Max: " + str(stats.describe(data)[1][1]))
        print("Average: " + str(statistics.mean(data)))
        print("Median (middle value): " + str(statistics.median(data)))
        try:
            print("Mode (most common value): " + str(statistics.mode(data)))
        except:
            print("A random value: " + str(random.choice(data)))
        print("Standard Deviation: " + str(statistics.stdev(data)))

    def statistics_ram(self):
        print("Min: " + self.ram_util)


class VizualizeMonitoring(Monitor):
    def __call__(self):
        data = self.cpu_util
        maximum = lambda a, b: a if a > b else b
        plt.plot(range(1, len(data) + 1), data, label='CPU')  # range(maximum(len(self.cpu_util), len(self.ram_util))+1)
        data = self.ram_util
        plt.plot(range(1, len(data) + 1), data, label='RAM')
        plt.legend()
        plt.xlabel("timesteps")
        plt.ylabel("utilization")
        plt.show()


def handler(sig_num, curr_stack_frame):
    a.save_cpu_ram(os.path.join(os.getcwd(), "task_3", "out", "machine_idle" + ".csv"), ["CPU", "RAM"])
    b = VizualizeMonitoring(a.cpu_util, a.ram_util)
    b()


if __name__ == '__main__':
    a = Monitor([], [])
    """
    TODO- remove the number of steps logic and implement a signal interapt logic in order not to record
    unecessary data
    """
    stop_threads = False
    # signal.signal(signal.SIGINT, handler)

    t1 = threading.Thread(target=a.monitor_cpu, args=(lambda: stop_threads,))
    t2 = threading.Thread(target=a.monitor_ram, args=(lambda: stop_threads,))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    time.sleep(200)
    # signal.pause()
    stop_threads = True
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    a.save_cpu_ram(os.path.join(os.getcwd(), "task_3", "out", "machine_idle" + ".csv"), ["CPU", "RAM"])
    b = VizualizeMonitoring(a.cpu_util, a.ram_util)
    b()
    # print(a.cpu_util)
    # print(psutil.cpu_count(logical=False))
