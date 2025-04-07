import pandas as pd
import helper

poem_genres = [
  "Hai chữ",
  "Bốn chữ",
  "Năm chữ",
  "Sáu chữ",
  "Bảy chữ",
  "Tám chữ",
  "Lục bát",
  "Song thất lục bát",
  "Thất ngôn tứ tuyệt",
  "Thất ngôn bát cú",
  "Thất ngôn cổ phong",
  "Ngũ ngôn bát cú",
  "Ngũ ngôn cổ phong",
  "Ngũ ngôn tứ tuyệt",
]

# df = pd.read_csv('handled_dataset/poems_dataset_processed_0.csv')
# df_filtered = df[df["Genre"].isin(poem_genres)]
# print(df_filtered["Genre"].unique())
# print(len(df))

# df1 = pd.read_csv('handled_dataset/poems_dataset_processed.csv')
df2 = pd.read_csv('handled_dataset/poems_dataset_processed_0.csv')
# df = helper.merge_dataframes(parts=[df1, df2]).drop_duplicates(subset=["Edited"])
# df.to_csv('handled_dataset/poems_dataset_processed.csv', index=False)
# print(len(df1))
print(len(df2))
df2_filtered = df2[df2["Genre"].isin(poem_genres)]
print(len(df2_filtered))
df2_filtered.to_csv("processing_dataset.csv", index=False)
