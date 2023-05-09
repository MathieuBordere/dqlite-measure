import sys
import time
import psutil
import matplotlib.pyplot as plt
import datetime
import os

def get_process_info(pid):
    try:
        process = psutil.Process(pid)
        cmdline = ' '.join(process.cmdline())
        mem_info = process.memory_info()
        return cmdline, mem_info.rss / (1024 ** 2)  # return memory usage in MB
    except psutil.NoSuchProcess:
        print(f"No such process: {pid}")
        return None, None

def monitor_memory_usage(pid, interval, duration):
    end_time = time.time() + duration
    timestamps = []
    memory_usage = []

    while time.time() < end_time:
        current_time = time.time()
        cmdline, mem_usage = get_process_info(pid)
        if mem_usage is None:  # process does not exist
            break
        timestamps.append(current_time)
        memory_usage.append(mem_usage)
        print(f"{current_time:.2f}s: {mem_usage:.2f}MB")
        time.sleep(interval)

    return cmdline, timestamps, memory_usage

def save_to_file(filename, cmdline, timestamps, memory_usage):
    with open(filename, 'w') as f:
        f.write(f"Command line: {cmdline}\n")
        for t, m in zip(timestamps, memory_usage):
            f.write(f"{t:.2f}s: {m:.2f}MB\n")

def read_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    cmdline = lines[0].strip().split(': ', 1)[1]
    data = [line.strip().split(': ') for line in lines[1:]]
    timestamps = [float(t[:-1]) for t, _ in data]  # strip 's' from timestamp before conversion
    memory_usage = [float(m[:-2]) for _, m in data]
    return cmdline, timestamps, memory_usage

def plot_memory_usage(cmdline, timestamps, memory_usage, save_path):
    if timestamps and memory_usage:  # only plot if there's data
        plt.plot(timestamps, memory_usage)
        plt.xlabel('Time (s)')
        plt.ylabel('Memory Usage (MB)')
        plt.title(f'Memory Usage over Time for "{cmdline}"')
        plt.grid(True)
        plt.savefig(save_path)  # save plot to file
        plt.show()
    else:
        print("No data to plot.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python memory_monitor.py <PID> <interval> <duration>")
        sys.exit(1)

    pid = int(sys.argv[1])
    interval = int(sys.argv[2])
    duration = int(sys.argv[3])

    cmdline, timestamps, memory_usage = monitor_memory_usage(pid, interval, duration)
    
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"memory_usage_{timestamp_str}.txt"
    dir_path = os.path.join("measurements", filename[:-4])  # create subfolder path
    
    if not os.path.exists(dir_path):  # create subfolder if it does not exist
        os.makedirs(dir_path)

    file_path = os.path.join(dir_path, filename)  # create file path
    save_to_file(file_path, cmdline, timestamps, memory_usage)
    
    cmdline, timestamps, memory_usage = read_from_file(file_path)
    plot_path = os.path.join(dir_path, f"memory_usage_{timestamp_str}.png")  # create plot file path
    plot_memory_usage(cmdline, timestamps, memory_usage, plot_path)


