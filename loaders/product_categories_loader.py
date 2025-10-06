from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_product_categories(file_path):
    df = load_sheet(file_path, "Product_Categories")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    def safe_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return -1  # or None if you prefer to skip invalid entries

    docs = []
    for _, row in df.iterrows():
        doc = {
            "_id": safe_int(row["PRODCAT_CODE"]),
            "prodCatDesc": safe_str(row["PRODCAT_DESC"]),
            "brandCode": safe_int(row["BRAND_CODE"]),  # reference to productBrands
            "pranCode": safe_int(row["PRAN_CODE"])     # reference to productRanges
        }
        docs.append(doc)

    db.productCategories.insert_many(docs)