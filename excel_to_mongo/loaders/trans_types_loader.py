from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_trans_types(file_path):
    df = load_sheet(file_path, "Trans_Types")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    docs = []
    for _, row in df.iterrows():
        docs.append({
            "_id": safe_str(row["TRANSTYPE_CODE"]),
            "transtypeDesc": safe_str(row["TRANSTYPE_DESC"])
        })

    db.transTypes.insert_many(docs)