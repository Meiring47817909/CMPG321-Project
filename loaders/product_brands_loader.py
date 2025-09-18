from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_product_brands(file_path):
    df = load_sheet(file_path, "Product_Brands")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    docs = []
    for _, row in df.iterrows():
        doc = {
            "_id": safe_str(row["PRODBRA_CODE"]),
            "prodBraDesc": safe_str(row["PRODBRA_DESC"])
        }
        docs.append(doc)

    db.productBrands.insert_many(docs)