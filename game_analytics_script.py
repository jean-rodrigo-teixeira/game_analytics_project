import pandas as pd
import numpy as np
import random
import os

# Number of records
num_rows = 100000

# Get the GAMES_PATH environment variable
games_path = os.getenv("GAMES_PATH", "C:\\Users\\Jean Rodrigo Teixeir\\games")

# Generating unique IDs for players and sessions
player_ids = [f"P{str(i).zfill(5)}" for i in range(1, num_rows // 10 + 1)]
session_ids = [f"S{str(i).zfill(6)}" for i in range(1, num_rows + 1)]

# Function to generate retention (D1, D7, D30) with realistic decay
def retention_probability(day):
    if day == 1:
        return np.random.choice([1, 0], p=[0.45, 0.55])  # 45% retention on D1
    elif day == 7:
        return np.random.choice([1, 0], p=[0.25, 0.75])  # 25% retention on D7
    elif day == 30:
        return np.random.choice([1, 0], p=[0.10, 0.90])  # 10% retention on D30
    return 0

# Creating the data
data = {
    "player_id": np.random.choice(player_ids, num_rows),
    "session_id": session_ids,
    "date": pd.date_range(start="2024-01-01", periods=num_rows, freq="T"),
    "session_length": np.random.randint(5, 120, num_rows),  # Sessions between 5 and 120 minutes
    "session_count": np.random.randint(1, 5, num_rows),  # Between 1 and 5 sessions per day
    "retention_day": np.random.choice([1, 7, 30], num_rows, p=[0.5, 0.3, 0.2]),  # 50% D1, 30% D7, 20% D30
    "churned": np.random.choice([0, 1], num_rows, p=[0.7, 0.3]),  # 30% churn rate
    "in_game_purchases": np.random.choice([0, 0, 0, 1.99, 4.99, 9.99, 49.99], num_rows, p=[0.7, 0.1, 0.1, 0.03, 0.03, 0.02, 0.02]),  
    "ad_revenue": np.round(np.random.uniform(0, 2, num_rows), 2),  # Ad revenue between $0 and $2
    "crashes": np.random.choice([0, 1, 2], num_rows, p=[0.9, 0.08, 0.02]),  # 90% no crash, 8% 1 crash, 2% 2 crashes
    "frame_rate": np.round(np.random.uniform(30, 60, num_rows), 1),  # FPS between 30 and 60
    "acquisition_source": np.random.choice(["Ads", "Organic", "Referral"], num_rows, p=[0.5, 0.4, 0.1]),  
    "cpi": np.round(np.random.uniform(0.5, 5, num_rows), 2),  # CPI between $0.5 and $5
}

# Create DataFrame
df = pd.DataFrame(data)

# Introducing problems in the dataset 🔥

# 🔴 1. Add missing values in some columns
for col in ["session_length", "frame_rate", "cpi"]:
    df.loc[df.sample(frac=0.02).index, col] = np.nan  # 2% missing values

# 🔴 2. Add extreme outliers
outlier_indices = df.sample(frac=0.005).index  # 0.5% extreme values
df.loc[outlier_indices, "session_length"] = np.random.randint(500, 2000, len(outlier_indices))  # Extremely long sessions
df.loc[outlier_indices, "frame_rate"] = np.random.uniform(5, 15, len(outlier_indices))  # Very low FPS
df.loc[outlier_indices, "cpi"] = np.random.uniform(50, 200, len(outlier_indices))  # Unrealistic CPI

# 🔴 3. Add duplicate records (1% duplicates)
duplicated_rows = df.sample(frac=0.01)
df = pd.concat([df, duplicated_rows])

# 🔴 4. Add formatting errors in `acquisition_source`
df.loc[df.sample(frac=0.02).index, "acquisition_source"] = np.random.choice(["Ad$", "0rganic", "refferal", "AdS"], size=int(0.02 * num_rows))

# Adjust retention to keep it consistent
df["retention_day"] = df["retention_day"].apply(retention_probability)

# Calculate ROAS (Return on Ad Spend) = (Total Revenue / Acquisition Cost) * 100
df["roas"] = np.where(df["acquisition_source"].str.contains("Ad", case=False, na=False), 
                      np.round((df["in_game_purchases"] + df["ad_revenue"]) / df["cpi"] * 100, 2), 
                      np.nan)

# Save as CSV to the GAMES_PATH directory
csv_file_path = os.path.join(games_path, "game_analytics_dataset.csv")
df.to_csv(csv_file_path, index=False)

print(f"🚨 Dataset 'game_analytics_dataset.csv' with issues created and saved to: {csv_file_path}")
