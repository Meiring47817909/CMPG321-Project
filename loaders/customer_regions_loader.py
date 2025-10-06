from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_customer_regions(file_path):
    df = load_sheet(file_path, "Customer_Regions")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    docs = []
    for _, row in df.iterrows():
        docs.append({
            "_id": safe_str(row["REGION_CODE"]),
            "regionDesc": safe_str(row["REGION_DESC"])
        })

    db.customerRegions.insert_many(docs)