import pandas as pd

dir_df = pd.read_csv("../logs/directory_log.csv")
print("directory log:")
print(dir_df)

event_counts = dir_df["Event"].value_counts()
print("\nFile event summary:")
print(event_counts)


import matplotlib.pyplot as plt

event_counts.plot(kind="bar")
plt.title("Directory File Events")
plt.xlabel("Event Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("../visuals/file_events.png")
plt.close()


with open("../reports/summary_report.txt", "w") as f:
    f.write("Directory Monitoring Summary\n")
    f.write(event_counts.to_string())
