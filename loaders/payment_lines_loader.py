from config.mongo_config import db
from loaders.base_loader import load_sheet
from utils.date_converter import excel_serial_to_iso
import pandas as pd

def load_payment_lines(file_path):
    df = load_sheet(file_path, "Payment_Lines")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"
    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    docs = []
    for _, row in df.iterrows():
        deposit_date = excel_serial_to_iso(row["DEPOSIT_DATE"])
        doc = {
            "_id": {
                "customerNumber": safe_str(row["CUSTOMER_NUMBER"]),
                "depositRef": safe_str(row["DEPOSIT_REF"]),
                "depositDate": deposit_date  # now part of _id
            },
            "finPeriod": safe_str(row["FIN_PERIOD"]),
            "depositDate": deposit_date,
            "bankAmt": safe_float(row["BANK_AMT"]),
            "discount": safe_float(row["DISCOUNT"]),
            "totPayment": safe_float(row["TOT_PAYMENT"])
        }
        docs.append(doc)

    db.paymentLines.insert_many(docs)