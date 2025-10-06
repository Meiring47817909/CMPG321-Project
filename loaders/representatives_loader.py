from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_representatives(file_path):
    df = load_sheet(file_path, "Representatives")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"
    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    docs = []
    for _, row in df.iterrows():
        docs.append({
            "_id": safe_str(row["REP_CODE"]),
            "repDesc": safe_str(row["REP_DESC"]),
            "commMethod": safe_str(row["COMM_METHOD"]),
            "commission": safe_float(row["COMMISSION"])
        })

    db.representatives.insert_many(docs)