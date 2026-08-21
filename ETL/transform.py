import pandas as pd
import hashlib
from extract import df

REQUIRED_COLUMNS = [
    "timestamp",
    "event",
    "ip",
    "username",
    "success"
]

def transform_logs(dataframe, required_columns=REQUIRED_COLUMNS):

    # Validar y limpiar
    df = dataframe.dropna(subset=required_columns).copy()
    
    if df.empty:
        raise ValueError("No hay registros válidos para procesar")
    
    # Procesar timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["date"] = df["timestamp"].dt.date.astype(str)
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.day_name().astype(str)
    
    # Ordenar por timestamp
    df = df.sort_values("timestamp")
    
    # Calcular intentos
    df["attempts_by_ip"] = df.groupby("ip").cumcount() + 1
    df["attempts_by_user"] = df.groupby("username").cumcount() + 1
    
    # Detectar actividad sospechosa
    df["suspicious"] = df["attempts_by_ip"] > 10
    
    # Generar event_id
    df["event_id"] = df.apply(
        lambda row: hashlib.sha256(
            f"{row['timestamp']}|"
            f"{row['ip']}|"
            f"{row['username']}|"
            f"{row['event']}".encode()
        ).hexdigest(),
        axis=1
    )
    
    return df

try:
    df = transform_logs(df, required_columns=REQUIRED_COLUMNS)
except ValueError as e:
    print(f"Error: {e}")
    exit()