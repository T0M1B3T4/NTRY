from extract import extract_logs, INPUT_FILE
from transform import transform_logs
from load_mongo import load_to_mongo

df = extract_logs(INPUT_FILE)

df = transform_logs(df)

load_to_mongo(df)