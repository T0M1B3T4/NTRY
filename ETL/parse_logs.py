import json
import os
import pandas as pd
import hashlib
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

INPUT_FILE = os.getenv(
    "INPUT_FILE",
    "/data/raw/login_logs.jsonl"
)

OUTPUT_FILE = os.getenv(
    "OUTPUT_FILE",
    "/data/processed/dataset.csv"
)

records = []

with open(INPUT_FILE, "r") as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        try:
            records.append(json.loads(line))

        except json.JSONDecodeError:
            print(f"Registro inválido ignorado: {line}")

df = pd.DataFrame(records)

required_columns = [
    "timestamp",
    "event",
    "ip",
    "username",
    "success"
]

df = df.dropna(subset=required_columns)

if df.empty:
    print("No hay registros válidos para procesar")
    exit()

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.day_name()

df["date"] = df["date"].astype(str)
df["day_of_week"] = df["day_of_week"].astype(str)

df = df.sort_values("timestamp")

df["attempts_by_ip"] = (
    df.groupby("ip")
      .cumcount() + 1
)

df["attempts_by_user"] = (
    df.groupby("username")
      .cumcount() + 1
)

df["suspicious"] = (
    df["attempts_by_ip"] > 10
)

df["event_id"] = df.apply(
    lambda row: hashlib.sha256(
        f"{row['timestamp']}|"
        f"{row['ip']}|"
        f"{row['username']}|"
        f"{row['event']}".encode()
    ).hexdigest(),
    axis=1
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)
records = df.to_dict("records")

client = MongoClient(
    os.getenv(
        "MONGO_URI",
        "mongodb://mongodb:27017"
    )
)

db = client["cyberlab"]

collection = db["login_events"]
collection.create_index(
    "event_id",
    unique=True
)

try:
    collection.insert_many(
        records,
        ordered=False
    )

except BulkWriteError as e:
    print(
        f"Duplicados detectados: "
        f"{len(e.details['writeErrors'])}"
    )

print(
    f"Dataset generado correctamente: "
    f"{OUTPUT_FILE}"
)

print(
    f"Registros procesados: {len(df)}"
)