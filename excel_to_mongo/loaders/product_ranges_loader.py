from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_product_ranges(file_path):
    df = load_sheet(file_path, "Product_Ranges")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    docs = []
    for _, row in df.iterrows():
        doc = {
            "_id": safe_str(row["PRAN_CODE"]),
            "pranDesc": safe_str(row["PRAN_DESC"])
        }
        docs.append(doc)

    db.productRanges.insert_many(docs)