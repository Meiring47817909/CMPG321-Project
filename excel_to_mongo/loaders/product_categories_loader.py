from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_product_categories(file_path):
    df = load_sheet(file_path, "Product_Categories")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    docs = []
    for _, row in df.iterrows():
        doc = {
            "_id": safe_str(row["PRODCAT_CODE"]),
            "prodCatDesc": safe_str(row["PRODCAT_DESC"]),
            "brandCode": safe_str(row["BRAND_CODE"]),  # reference to productBrands
            "pranCode": safe_str(row["PRAN_CODE"])     # reference to productRanges
        }
        docs.append(doc)

    db.productCategories.insert_many(docs)