import helper
import pandas as pd
import os

## SPLIT DATASET TO N PARTS
def split_dataset(file_, n_parts_):
  df = pd.read_csv(f"{file_}.csv")
  parts = helper.split_df(df, n_parts_)
  for i in range(len(parts)):
      parts[i].to_csv(f"{file_}_{i}.csv", index=False, encoding="utf-8")

## MERGE HANDLED DATASET
def merge_dataset(from_, to_, file_="poems_dataset_proc0"):
  df0_processed = pd.read_csv(f"handled_dataset/poems_dataset_processed.csv")
  df0_raw = pd.read_csv(f"handled_dataset/poems_dataset_raw.csv")
  dfs = []
  print(f"Current data in TARGET FILE:\n{len(df0_processed)} - handled_dataset/poems_dataset_processed.csv")
  print(f"{len(df0_raw)} - handled_dataset/poems_dataset_raw.csv\n")
  print(f"New handled data:")
  for i in range(from_, to_+1):
    try:
      df_i = pd.read_csv(f"{file_}_{i}_handled.csv")
      print(f"{len(df_i[df_i['Genre'].notna() & (df_i['Genre'] != 'Xóa')])}/{len(df_i)} - {file_}_{i}_handled.csv")
      dfs.append(df_i)
    except Exception:
      print("Invalid")
      continue
  df = helper.merge_dataframes(dfs)
  print(f"Processed: {len(df[df['Genre'].notna() & (df['Genre'] != 'Xóa')])}/{len(df.drop_duplicates(['Edited']))}")
  df = helper.merge_dataframes([df0_processed, df0_raw] + dfs)
  df1_processed = df[df["Genre"].notna() & (df["Genre"] != "Xóa")].drop_duplicates(["Edited"])
  df1_raw = df[df["Genre"].isna() & (df["Genre"] != "Xóa")].drop_duplicates(["Edited"])

  df1_processed.to_csv("handled_dataset/poems_dataset_processed.csv", index=False)
  df1_raw.to_csv("handled_dataset/poems_dataset_raw.csv", index=False)
  print("\n... Saved dataset")

  print(f"New data in TARGET FILE:\n{len(df1_processed)} - handled_dataset/poems_dataset_processed.csv")
  print(f"{len(df1_raw)} - handled_dataset/poems_dataset_raw.csv")


# split_dataset(file_="poems_dataset_proc1", n_parts_=6)
## >>> Example:
## Chia file poems_dataset_proc1.csv thành: từ "poems_dataset_proc1_0.csv" đến "poems_dataset_proc1_5.csv"
## Thì dùng: split_dataset(file_="poems_dataset_proc1", n_parts_=6)

# merge_dataset(from_=6, to_=9, file_="poems_dataset_proc0")
## >>> Example:
## merge file: từ "poems_dataset_proc0_0_handled.csv" đến "poems_dataset_proc0_5_handled.csv"
## Thì dùng: merge_dataset(from_=0, to_=5, file_="poems_dataset_proc0")