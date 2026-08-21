from transform import df
from extract import OUTPUT_FILE
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import os


def load_to_mongo(
    dataframe,
    output_file,
    mongo_uri=None,
    database_name="cyberlab",
    collection_name="login_events",
    unique_field="event_id"
):
    
    # Guardar a CSV
    dataframe.to_csv(output_file, index=False)
    
    # Conectar a MongoDB
    if mongo_uri is None:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
    
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]
    
    # Crear índice único
    collection.create_index(unique_field, unique=True)
    
    # Insertar registros
    records = dataframe.to_dict("records")
    duplicates_count = 0
    
    try:
        collection.insert_many(records, ordered=False)
    except BulkWriteError as e:
        duplicates_count = len(e.details["writeErrors"])
        print(f"Duplicados detectados: {duplicates_count}")
    finally:
        client.close()
    
    return {
        "output_file": output_file,
        "total_records": len(dataframe),
        "duplicates": duplicates_count
    }

# Ejecutar
result = load_to_mongo(df, OUTPUT_FILE)

print(f"Dataset generado correctamente: {result['output_file']}")
print(f"Registros procesados: {result['total_records']}")