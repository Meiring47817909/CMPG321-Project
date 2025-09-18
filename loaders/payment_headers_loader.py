from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_payment_headers(file_path):
    df = load_sheet(file_path, "Payment_Header")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    docs = []
    for _, row in df.iterrows():
        doc = {
            "_id": {
                "depositRef": safe_str(row["DEPOSIT_REF"]),
                "customerNumber": safe_str(row["CUSTOMER_NUMBER"])
            },
            "customerNumber": safe_str(row["CUSTOMER_NUMBER"])
        }
        docs.append(doc)

    db.paymentHeaders.insert_many(docs)