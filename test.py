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
  print(f"{len(df1_raw)} - handled_dataset/poems_dataset_raw.csv\n")

merge_dataset(0, 4)