import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import argparse

# Constants
REFRESH_INTERVAL = 1000  # in milliseconds
MAX_DATA_POINTS = 100  # maximum number of data points to display
HISTORY_FILE = "cpu_history.txt"  # file to store historical data

# Initialize data arrays
timestamps = []
cpu_percentages = [[] for _ in range(psutil.cpu_count())]

# Initialize figure and axes
fig, ax = plt.subplots()

# Create empty line objects for each CPU core
lines = [ax.plot([], [], label=f"CPU {i + 1}")[0] for i in range(psutil.cpu_count())]

# Set up plot properties
ax.set_xlabel('Time')
ax.set_ylabel('CPU Usage (%)')
ax.set_title('Real-Time CPU Usage')
ax.legend(loc='upper left')
ax.set_ylim(0, 100)

# Function to update the plot
def update_plot(frame):
    # Retrieve CPU usage data
    cpu_percent = psutil.cpu_percent(percpu=True)

    # Append current timestamp
    timestamps.append(frame)

    # Append CPU usage data to respective arrays
    for i, cpu in enumerate(cpu_percent):
        cpu_percentages[i].append(cpu)
        cpu_percentages[i] = cpu_percentages[i][-MAX_DATA_POINTS:]

    # Plot CPU usage for each core
    for i, line in enumerate(lines):
        line.set_xdata(timestamps)
        line.set_ydata(cpu_percentages[i])

    # Set appropriate time axis limit based on number of data points
    ax.set_xlim(max(0, frame - MAX_DATA_POINTS), frame + 1)

    # Set x and y axis labels
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('CPU Usage (%)')

    # Redraw plot
    fig.canvas.draw()

    # Save CPU usage data to history file
    save_cpu_data(frame, cpu_percent)


# Function to save CPU usage data to history file
def save_cpu_data(timestamp, cpu_percent):
    with open(HISTORY_FILE, 'a') as f:
        formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{formatted_time},{','.join(map(str, cpu_percent))}\n")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Real-Time CPU Monitoring Tool")
    parser.add_argument("--cores", type=int, default=psutil.cpu_count(),
                        help="Number of CPU cores to display in the plot")
    parser.add_argument("--width", type=float, default=10,
                        help="Width of the plot")
    parser.add_argument("--height", type=float, default=6,
                        help="Height of the plot")
    parser.add_argument("--refresh", type=int, default=REFRESH_INTERVAL,
                        help="Refresh interval for real-time updates in milliseconds")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Update constants based on command-line arguments
    REFRESH_INTERVAL = args.refresh
    MAX_DATA_POINTS = int(args.width)  # Convert width to integer for maximum data points
    fig.set_size_inches(args.width, args.height)

    # Start animation
    ani = FuncAnimation(fig, update_plot, frames=range(MAX_DATA_POINTS), interval=REFRESH_INTERVAL, cache_frame_data=False)

    # Show the plot
    plt.show()

