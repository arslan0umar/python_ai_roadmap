import os
import pandas as pd

base_dir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(base_dir, "matches.csv"))

print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nColumn info:")
print(df.info())
print("\nNumeric stats:")
print(df.describe())
print("\nMissing values per column:")
print(df.isnull().sum())

print("\nEach Team Win count: ")
print(df["winner"].value_counts())

win_by_run = df[df["result"] == "runs"]
grpdata = win_by_run.groupby("season")["result_margin"].mean()

print("\nSeason (year) highest average winning margin (by runs)")
print(grpdata.loc[[grpdata.idxmax()]])

print("\nTop 5 cities hosted the most IPL matches")
print(df["city"].value_counts().head())

df["result_type"] = df["result"].apply(
    lambda x: "Batting Win" if x == "runs" 
    else "Bowling Win" if x == "wickets" 
    else "No Result"
)

df.to_csv(os.path.join(base_dir, "newcsv.csv"), index = False)
print("\n New Column added successfully to new CSV file (newcsv.csv)")