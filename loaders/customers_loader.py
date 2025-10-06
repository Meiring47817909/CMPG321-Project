from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_customers(file_path):
    customer_df = load_sheet(file_path, "Customer")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    def safe_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return 0

    docs = []
    for _, row in customer_df.iterrows():
        cust_id = safe_str(row["CUSTOMER_NUMBER"])

        doc = {
            "_id": cust_id,
            "ccatCode": safe_int(row["CCAT_CODE"]),
            "regionCode": safe_str(row["REGION_CODE"]),
            "repCode": safe_str(row["REP_CODE"]),
            "settleTerms": safe_int(row.get("SETTLE_TERMS")),
            "normalPayterms": safe_int(row.get("NORMAL_PAYTERMS")),
            "discount": safe_float(row.get("DISCOUNT")),
            "creditLimit": safe_float(row.get("CREDIT_LIMIT"))
        }
        docs.append(doc)

    db.customers.insert_many(docs)