from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["logs_db"]
collection = db["eventos"]

# 1. Cargar datos
logs = list(collection.find())
df = pd.DataFrame(logs)

# 2. Preprocesamiento
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["minute"] = df["timestamp"].dt.floor("T")

# 3. Feature engineering
grouped = df.groupby(["ip", "minute"]).agg({
    "status": lambda x: (x == "fail").sum(),
    "response_time_ms": "mean",
    "attempts": "sum",
    "attack_label": lambda x: x.mode()[0]  # etiqueta dominante
}).rename(columns={
    "status": "failed_requests",
    "response_time_ms": "avg_response_time",
    "attempts": "total_attempts"
})

grouped["requests"] = df.groupby(["ip", "minute"]).size()
grouped["error_rate"] = grouped["failed_requests"] / grouped["requests"]

grouped = grouped.reset_index()

# 4. Features y target
X = grouped[[
    "failed_requests",
    "avg_response_time",
    "total_attempts",
    "requests",
    "error_rate"
]]

y = grouped["attack_label"]

# 5. Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 6. Modelo
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 7. Evaluación
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 8. Guardar modelo
joblib.dump(model, "models/model.pkl")

print("✅ Modelo entrenado y guardado")