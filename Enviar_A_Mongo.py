from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()    

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

df = pd.read_csv("/home/T0M1/Desktop/T0M1/NTRY/Datos_Procesados.csv")

for _, row in df.iterrows():
    log_entry = {
        "timestamp": row["timestamp"],
        "ip": row["ip"],
        "intentos": row["intentos"],
        "resultado": row["resultado"],
        "usuario": row["usuario"]
    }
    collection.insert_one(log_entry)

print("Logs enviados a MongoDB con éxito.")
print("db:", DB_NAME)