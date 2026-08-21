import json
import os
import pandas as pd

INPUT_FILE = os.getenv(
    "INPUT_FILE",
    "/data/raw/login_logs.jsonl"
)

OUTPUT_FILE = os.getenv(
    "OUTPUT_FILE",
    "/data/processed/dataset.csv"
)

def extract_logs(input_file):
    
    records = []
    
    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            
            if not line:
                continue
            
            try:
                records.append(json.loads(line))
            
            except json.JSONDecodeError:
                print(f"Registro inválido ignorado: {line}")
    
    return pd.DataFrame(records)

df = extract_logs(INPUT_FILE)