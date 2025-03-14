import helper
import pandas as pd
import os

## SPLIT DATASET TO N PARTS
# df = pd.read_csv("poems_dataset_proc0_5.csv")
# parts = helper.split_df(df, 6)
# for i in range(len(parts)):
#     parts[i].to_csv(f"poems_dataset_proc0_{i}.csv", index=False, encoding="utf-8")


# df0 = pd.read_csv("poems_dataset_proc0_0_handled.csv")
# df1 = pd.read_csv("poems_dataset_proc0_1_handled.csv")
# df2 = pd.read_csv("poems_dataset_proc0_2_handled.csv")
# df = pd.concat([df0, df1, df2])
# authors_not_in_thivien = df.loc[df["Genre"].notna(), "Author"].dropna().str.lower().unique()
# pd.DataFrame(authors_not_in_thivien, columns=["Author"]).to_csv("authors_in_thivien.csv", index=False)
# print(df.count("index")["Genre"])

df0 = pd.read_csv(f"handled_dataset/poems_dataset_processed.csv")
dfs = []
print(len(df0))
for i in range(0, 5):
  try:
    df_i = pd.read_csv(f"poems_dataset_proc0_{i}_handled.csv")
    print(len(df_i[df_i["Genre"].notna() & (df_i["Genre"] != "Xóa")]))
    dfs.append(df_i)
  except Exception:
    print("Invalid")
    continue
df = helper.merge_dataframes([df0,] + dfs)
df = df[df["Genre"].notna() & (df["Genre"] != "Xóa")].drop_duplicates(["Edited"])
print(len(df))
df.to_csv("handled_dataset/poems_dataset_processed.csv", index=False)
