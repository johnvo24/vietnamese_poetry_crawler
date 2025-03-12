import helper
import pandas as pd

# df = pd.read_csv("poems_dataset_proc0.csv")
# parts = helper.split_df(df, 10)
# for i in range(len(parts)):
#     parts[i].to_csv(f"poems_dataset_proc0_{i}.csv", index=False, encoding="utf-8")

# parts[100].to_csv(f"poems_dataset_proc0_{0}.csv", index=False, encoding="utf-8")

df0 = pd.read_csv("poems_dataset_proc0_0_handled.csv")
df1 = pd.read_csv("poems_dataset_proc0_1_handled.csv")
df2 = pd.read_csv("poems_dataset_proc0_2_handled.csv")
df = pd.concat([df0, df1, df2])
authors_not_in_thivien = df.loc[df["Genre"].notna(), "Author"].dropna().str.lower().unique()
pd.DataFrame(authors_not_in_thivien, columns=["Author"]).to_csv("authors_in_thivien.csv", index=False)
# print(df.count("index")["Genre"])