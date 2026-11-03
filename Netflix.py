import csv

import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.stdout.reconfigure(encoding="utf-8")
#==============================
#LOAD DATASET 
#==============================
df = pd.read_csv("NETFLIX.csv", encoding="utf-8")
df["Date_Added"] = pd.to_datetime(
    df["Date_Added"],
    errors="coerce"
)

df["Year_Added"] = df["Date_Added"].dt.year

df["Month_Added"] = df["Date_Added"].dt.month

print(df[["Date_Added", "Year_Added", "Month_Added"]].head(10))

print("Missing dates:", df["Date_Added"].isna().sum())

print(df["Date_Added"].isna().sum())

print(df.isnull().sum())

print(df.head())
print(df.info())
print(df.shape)
#==============================
#CHECK DUPLICATES 
#==============================
print(df.duplicated().sum())




#==============================
#CLEAN DURATION COLUMN
#==============================
df["Duration_Value"] = df["Duration"].str.extract(r"(\d+)")[0]
df["Duration_Value"] = pd.to_numeric(df["Duration_Value"])

df["Duration_Unit"] = df["Duration"].str.extract(r"([A-Za-z]+)")

df["Duration_Unit"] = df["Duration_Unit"].replace({
    "min": "Minutes",
    "Season": "Seasons"
})

print(df[["Duration","Duration_Value","Duration_Unit"]].head(20))

print(df["Duration_Unit"].value_counts(dropna=False))

print(df[df["Duration_Unit"] == "Unknown"][["Title", "Type", "Duration"]])
#==============================
#COUNTRY ANALYSIS
#==============================
print(df["Country"].head(20))

df["Country"] = df["Country"].str.strip()

Country_df = df[["Show_ID", "Title", "Country"]].copy()

Country_df["Country"] = Country_df["Country"].str.split(",")

Country_df = Country_df.explode("Country")
Country_df["Country"] = Country_df["Country"].str.strip()
print(Country_df.head(20))

#==============================
#GENRE ANALYSIS
#==============================
print(df["Listed_in"].head(20))

ListedIn_df = df[["Show_ID", "Title", "Listed_in"]].copy()
ListedIn_df["Listed_in"] = ListedIn_df["Listed_in"].str.split(",")
ListedIn_df = ListedIn_df.explode("Listed_in")
ListedIn_df["Listed_in"] = ListedIn_df["Listed_in"].str.strip()

#==============================
#FINAL DATASET
#==============================

print("Total Titles:", len(df))

print("\nMovies vs TV Shows:")
print(df["Type"].value_counts())

print("\nRatings:")
print(df["Ratings"].value_counts())

print("\nTop Countries:")
print(Country_df["Country"].value_counts().head(10))

print("\nTop Genres:")
print(ListedIn_df["Listed_in"].value_counts().head(10))

print(df[df["Ratings"].isin(["74 min", "84 min", "66 min"])]
      [["Show_ID", "Title", "Type", "Ratings", "Duration"]])


# Correct incorrect values in Ratings
df.loc[df["Show_ID"] == "s5542", "Ratings"] = "Unknown"
df.loc[df["Show_ID"] == "s5795", "Ratings"] = "Unknown"
df.loc[df["Show_ID"] == "s5814", "Ratings"] = "Unknown"

# Recover the durations
df.loc[df["Show_ID"] == "s5542", "Duration"] = "74 min"
df.loc[df["Show_ID"] == "s5795", "Duration"] = "84 min"
df.loc[df["Show_ID"] == "s5814", "Duration"] = "66 min"

df["Duration_Value"] = df["Duration"].str.extract(r"(\d+)")[0]

df["Duration_Value"] = pd.to_numeric(
    df["Duration_Value"],
    errors="coerce"
)

df["Duration_Unit"] = df["Duration"].str.extract(
    r"([A-Za-z]+)"
)[0]

df["Duration_Unit"] = df["Duration_Unit"].replace({
    "min": "Minutes",
    "Season": "Seasons"
})

print(
    df[df["Show_ID"].isin(["s5542", "s5795", "s5814"])]
    [["Show_ID", "Title", "Ratings", "Duration",
      "Duration_Value", "Duration_Unit"]]
)

# ==========================================
# EDA 1 - MOVIES VS TV SHOWS
# ==========================================

type_count = df["Type"].value_counts()

print(type_count)

type_percentage = (
    df["Type"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)
print(type_percentage)

total_titles = df["Show_ID"].nunique()
print("Total Titles:", total_titles)

content_by_year = df["Year_Added"].value_counts().sort_index()
print("\nContent Added by Year:")
print(content_by_year)

#==============================
# EDA 2: PLOT CONTENT ADDED BY YEAR
#==============================

plt.figure(figsize=(10, 5))

plt.plot(
    content_by_year.index,
    content_by_year.values,
    marker="o", 
)

plt.title("Netflix Content Added by Year")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.xticks(content_by_year.index)
plt.grid(True)
plt.show()

#==============================
# EDA 3: RATING ANALYSIS
#==============================

top_ratings = df["Ratings"].value_counts().head(10)

print("\nTop 10 Ratings:")
print(top_ratings)

#==============================
# EDA 4: TOP COUNTRIES ANALYSIS
#==============================

Country_count =(
    Country_df[Country_df["Country"] != "Unknown"]
    ["Country"]
    .value_counts()
)

print("\nTop Countries:")
print(Country_count.head(10))

#==============================
# EDA 5: TOP GENRES ANALYSIS
#==============================

genre_count=(
    ListedIn_df["Listed_in"]
    .value_counts()
)

print("\nTop Genres:")
print(genre_count.head(10))

#==============================
# EDA 6: DURATION ANALYSIS
#==============================

movie_duration =df[(df["Type"] == "Movie") & (df["Duration_Unit"] == "Minutes")]["Duration_Value"]

average_movie_duration = movie_duration.mean()
print(f"\nAverage Movie Duration: {average_movie_duration:.2f} minutes")

tvShow_Seasons =df[(df["Type"] == "TV Show") & (df["Duration_Unit"] == "Seasons")]["Duration_Value"]
average_tvshow_seasons = tvShow_Seasons.mean()
print(f"Average TV Show Seasons: {average_tvshow_seasons:.2f} seasons")

#==============================
# EDA 7: RELEASE YEAR ANALYSIS
#==============================

release_year_count =(
    df["Release_Year"]
    .value_counts()
    .sort_index()
)
print("\nContent Released by Year:")
print(release_year_count)


country_total =(
    Country_df[Country_df["Country"] != "Unknown"]["Country"]
    .nunique()
)
print("\nTotal Countries:", country_total)

print("Final rows:", len(df))
print("Final columns:", len(df.columns))
print(df.shape)

print(
    df[df["Title"].str.contains("Memphis Belle", case=False, na=False)]
    [["Show_ID", "Type", "Title", "Director", "Cast", "Country", "Date_Added"]]
)

df.to_excel("Netflix_Cleaned.xlsx", index=False)

with pd.ExcelWriter("Netflix_Cleaned.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Netflix", index=False)
    Country_df.to_excel(writer, sheet_name="Countries", index=False)
    ListedIn_df.to_excel(writer, sheet_name="Genres", index=False)

print("Excel file created successfully!")