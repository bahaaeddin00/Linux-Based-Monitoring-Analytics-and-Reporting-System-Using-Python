import pandas as pd

cpu_df = pd.read_csv("../logs/system_log.csv")

print("CPU Log Summary:")
print(cpu_df.describe())

cpu_df.to_csv("../reports/summary_log.csv", index=False)
