import json
import os
import pandas as pd

INPUT_FILE = os.getenv(
    "INPUT_FILE",
    "/home/T0M1/Desktop/T0M1/NTRY/backend/login_logs.json"
)

OUTPUT_FILE = os.getenv(
    "OUTPUT_FILE",
    "/home/T0M1/Desktop/T0M1/NTRY/ETL/dataset.csv"
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

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.day_name()

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

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"Dataset generado correctamente: "
    f"{OUTPUT_FILE}"
)