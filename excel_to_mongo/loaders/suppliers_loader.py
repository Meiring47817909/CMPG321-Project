from config.mongo_config import db
import pandas as pd
from loaders.base_loader import load_sheet

def load_suppliers(file_path):
    df = load_sheet(file_path, "Suppliers")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    def safe_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return 0

    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    records = []
    for _, row in df.iterrows():
        record = {
            "_id": safe_str(row["SUPPLIER_CODE"]).zfill(3),
            "supplierDesc": safe_str(row["SUPPLIER_DESC"]),
            "exclsv": safe_str(row["EXCLSV"]),
            "normalPayterms": safe_int(row["NORMAL_PAYTERMS"]),
            "creditLimit": safe_float(row["CREDIT_LIMIT"])
        }
        records.append(record)

    db.suppliers.insert_many(records)