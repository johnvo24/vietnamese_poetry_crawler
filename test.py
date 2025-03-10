import helper
import pandas as pd

df = pd.read_csv("poems_dataset_proc0.csv")
parts = helper.split_df(df, 10)
for i in range(len(parts)):
    parts[i].to_csv(f"poems_dataset_proc0_{i}.csv", index=False, encoding="utf-8")

# parts[100].to_csv(f"poems_dataset_proc0_{0}.csv", index=False, encoding="utf-8")