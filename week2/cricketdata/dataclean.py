import os
import pandas as pd

base_dir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(base_dir, "matches.csv"))

print("Null Count Per Column(before data cleaning): ")
print(df.isnull().sum())

print("\nData cleaning operation is applying.....")

df["city"] = df["city"].fillna("Unknown")
df = df.dropna(subset="winner")
df["player_of_match"] = df["player_of_match"].fillna("N/A")
df["method"] = df["method"].fillna("Normal")
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year


if df.duplicated().sum():
    print(f"\nThere are {df.duplicated().sum()} rows exist in your data")
    df = df.drop_duplicates()
else:
    print("\nNo Duplicate Row in the data")

df["city"] = df["city"].str.strip()
df["city"] = df["city"].str.title()

print("\nData cleaning operation complete")

print("\nNull Count Per Column(after data cleaning): ")
print(df.isnull().sum())

df.to_csv(os.path.join(base_dir, "cleaned_matches.csv"), index=False)
print("\nNew file cleaned_matches.csv created with cleaned data")