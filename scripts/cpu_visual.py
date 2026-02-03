import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("../logs/system_log.csv")

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Convert CPU idle to CPU usage
df["cpu_usage"] = 100 - df["cpu_idle_percent"]

# Plot CPU usage
plt.figure()
plt.plot(df["timestamp"], df["cpu_usage"])
plt.xlabel("Time")
plt.ylabel("CPU Usage (%)")
plt.title("CPU Usage Over Time")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("../visuals/cpu_usage.png")
plt.show()

