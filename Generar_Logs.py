import pandas as pd
import random
from datetime import datetime 
def generar_log():
    return{
    "timestamp": datetime.now(),
    "ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}", 
    "intentos": random.randint(1, 20),
    "resultado": random.choice(["1", "0"]),  # Donde 1 es éxito y 0 es fallo
    "usuario": f"user_{random.randint(1, 100)}"
    }

if __name__ == "__main__":
    logs = [generar_log() for _ in range(1000)]
    df = pd.DataFrame(logs)
    df.to_csv("/home/T0M1/Desktop/T0M1/NTRY/Datos_Procesados.csv", index = False)
    print("Logs Generados con éxito y guardados en 'Datos_Procesados.csv'")    