import requests

BASE = "http://127.0.0.1:8000"

# 1️⃣ Register raw table
requests.post(f"{BASE}/raw/register", json={
    "name": "transactions",
    "source_type": "csv",
    "location": "data/transactions.csv",
    "entity_column": "user_id"
})

# 2️⃣ Register feature
requests.post(f"{BASE}/feature/register", json={
    "name": "avg_spend",
    "entity": "user_id",
    "raw_table_id": 1,
    "description": "Average transaction amount"
})

# 3️⃣ Compute feature
requests.post(f"{BASE}/feature/compute", json={
    "feature_id": 1,
    "logic": "df.groupby('user_id')['amount'].mean()"
})

# 4️⃣ Fetch feature vector
response = requests.get(
    f"{BASE}/feature/vector/101",
    params={"features": "avg_spend"}
)

print("Status Code:", response.status_code)
print("Raw Response Text:", response.text)


