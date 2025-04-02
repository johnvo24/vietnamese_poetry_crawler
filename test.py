import pandas as pd

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

df = pd.read_csv('handled_dataset/poems_dataset_processed_0.csv')
# df_filtered = df[df["Genre"].isin(poem_genres)]
# print(df_filtered["Genre"].unique())
print(len(df))