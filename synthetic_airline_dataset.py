import pandas as pd
import random

# Sample data
airlines = ["Delta", "American Airlines", "United", "Southwest", "JetBlue", "Spirit", "Frontier"]
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]

# Generate synthetic data
data = {
    "Airline": [random.choice(airlines) for _ in range(200)],
    "Origin": [random.choice(cities) for _ in range(200)],
    "Destination": [random.choice(cities) for _ in range(200)],
    "Flight Number": [random.randint(1000, 9999) for _ in range(200)],
    "Price ($)": [random.randint(50, 500) for _ in range(200)],
    "Flight Duration (hrs)": [random.uniform(1, 6) for _ in range(200)]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Ensure Origin and Destination are not the same
df = df[df["Origin"] != df["Destination"]]

# Save as CSV
df.to_csv("synthetic_airlines_dataset.csv", index=False)

print(df.head())
