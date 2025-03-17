import helper
import pandas as pd
import os
from data_handler import DataHandler

## SPLIT DATASET TO N PARTS
def split_dataset(file_, n_parts_):
  df = pd.read_csv(f"{file_}.csv")
  parts = helper.split_df(df, n_parts_)
  for i in range(len(parts)):
    parts[i].to_csv(f"{file_}_{i}.csv", index=False, encoding="utf-8")

## HANDLED FILES
def handle_dataset(from_, to_, file_, driver_type_="firefox", num_processes_=1, allow_overwrite=False):
  data_handler = DataHandler(
    driver_type=driver_type_,
    num_processes=num_processes_
  )
  for i in range(from_, to_+1):
    if os.path.exists(f"{file_}_{i}.csv"):
      if (not allow_overwrite) and (os.path.exists(f"{file_}_{i}_handled.csv")):
        print(f"# {file_}_{i}_handled.csv has been handled!")
        continue
      try:
        print(f"# {file_}_{i}.csv file is being handled!")
        data_handler.handle(file_name=f"{file_}_{i}")
      except Exception:
        print(f"ERROR: File handling failed!")
    else:
      print(f"# {file_}_{i}_handled.csv file not found!")
  
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
  print(f"Processed: {len(df[df['Genre'].notna() & (df['Genre'] != 'Xóa')].drop_duplicates(['Edited']))}/{len(df.drop_duplicates(['Edited']))}")
  df = helper.merge_dataframes([df0_processed, df0_raw] + dfs)
  df1_processed = df[df["Genre"].notna() & (df["Genre"] != "Xóa")].drop_duplicates(["Edited"])
  df1_raw = df[df["Genre"].isna() & (df["Genre"] != "Xóa")].drop_duplicates(["Edited"])

  df1_processed.to_csv("handled_dataset/poems_dataset_processed.csv", index=False)
  df1_raw.to_csv("handled_dataset/poems_dataset_raw.csv", index=False)
  print("\n... Saved dataset")

  print(f"New data in TARGET FILE:\n{len(df1_processed)} - handled_dataset/poems_dataset_processed.csv")
  print(f"{len(df1_raw)} - handled_dataset/poems_dataset_raw.csv")


# split_dataset(file_="poems_dataset_proc3", n_parts_=20)
## >>> Example:
## Chia file poems_dataset_proc1.csv thành: từ "poems_dataset_proc1_0.csv" đến "poems_dataset_proc1_5.csv"
## Thì dùng: split_dataset(file_="poems_dataset_proc1", n_parts_=6)

# handle_dataset(from_=0, to_=20, file_="poems_dataset_proc3", driver_type_="firefox", num_processes_=1, allow_overwrite=False)
## >>> Example:
## Xử lý file: từ "poems_dataset_proc1_0.csv" đến "poems_dataset_proc1_5.csv" thành "poems_dataset_proc1_0_handled.csv" ... "poems_dataset_proc1_5_handled.csv"
## Thì dùng: handle_dataset(from_=0, to_=5, file_="poems_dataset_proc1", driver_type_="firefox", num_processes_=1, allow_overwrite=False)

merge_dataset(from_=0, to_=19, file_="poems_dataset_proc3")
## >>> Example:
## merge file: từ "poems_dataset_proc0_0_handled.csv" đến "poems_dataset_proc0_5_handled.csv"
## Thì dùng: merge_dataset(from_=0, to_=5, file_="poems_dataset_proc0")

# df = pd.read_csv("poems_dataset_proc1_0.csv")
# print(print(df.loc[145:149]))