# TEST FUNCTION
import pandas as pd
import random
import os


# df0 = pd.read_csv("poems_dataset_proc0_0_handled.csv")
# df1 = pd.read_csv("poems_dataset_proc0_1_handled.csv")
# df2 = pd.read_csv("poems_dataset_proc0_2_handled.csv")
# df = pd.concat([df0, df1, df2])
# authors_not_in_thivien = df.loc[df["Genre"].notna(), "Author"].dropna().str.lower().unique()
# pd.DataFrame(authors_not_in_thivien, columns=["Author"]).to_csv("authors_in_thivien.csv", index=False)
# print(df.count("index")["Genre"])

# df = pd.read_csv("poems_dataset_proc1_0.csv")
# print(len(df.drop_duplicates(["Edited"])))