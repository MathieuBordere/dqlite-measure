import sys
import time
import psutil
import matplotlib.pyplot as plt

def get_memory_usage(pid):
    process = psutil.Process(pid)
    mem_info = process.memory_info()
    return mem_info.rss / (1024 ** 2)  # return memory usage in MB

def monitor_memory_usage(pid, interval, duration):
    end_time = time.time() + duration
    timestamps = []
    memory_usage = []

    while time.time() < end_time:
        current_time = time.time()
        mem_usage = get_memory_usage(pid)
        timestamps.append(current_time)
        memory_usage.append(mem_usage)
        print(f"{current_time:.2f}s: {mem_usage:.2f}MB")
        time.sleep(interval)

    return timestamps, memory_usage

def plot_memory_usage(timestamps, memory_usage):
    plt.plot(timestamps, memory_usage)
    plt.xlabel('Time (s)')
    plt.ylabel('Memory Usage (MB)')
    plt.title('Memory Usage over Time')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python memory_monitor.py <PID> <interval> <duration>")
        sys.exit(1)

    pid = int(sys.argv[1])
    interval = int(sys.argv[2])
    duration = int(sys.argv[3])

    timestamps, memory_usage = monitor_memory_usage(pid, interval, duration)
    plot_memory_usage(timestamps, memory_usage)

