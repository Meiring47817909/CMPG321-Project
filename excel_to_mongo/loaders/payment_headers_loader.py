from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd
from datetime import datetime, timedelta

def excel_date_to_iso(excel_serial):
    """Convert Excel serial date to ISO format."""
    if pd.isna(excel_serial):
        return None
    base_date = datetime(1899, 12, 30)  # Excel's day 1
    return (base_date + timedelta(days=int(excel_serial))).isoformat()

def safe_str(val):
    return str(val).strip() if pd.notna(val) else "N/A"

def safe_float(val):
    return float(val) if pd.notna(val) else 0.0

def load_payment_headers(file_path):
    header_df = load_sheet(file_path, "Payment_Header")
    lines_df = load_sheet(file_path, "Payment_Lines")

    # Group lines by CUSTOMER_NUMBER + DEPOSIT_REF
    grouped_lines = {}
    for _, row in lines_df.iterrows():
        key = f"{safe_str(row['CUSTOMER_NUMBER'])}_{safe_str(row['DEPOSIT_REF'])}"
        line = {
            "finPeriod": safe_str(row["FIN_PERIOD"]),
            "depositDate": excel_date_to_iso(row["DEPOSIT_DATE"]),
            "bankAmt": safe_float(row["BANK_AMT"]),
            "discount": safe_float(row["DISCOUNT"]),
            "totPayment": safe_float(row["TOT_PAYMENT"])
        }
        grouped_lines.setdefault(key, []).append(line)

    # Build final documents
    docs = []
    for _, row in header_df.iterrows():
        customer_number = safe_str(row["CUSTOMER_NUMBER"])
        deposit_ref = safe_str(row["DEPOSIT_REF"])
        key = f"{customer_number}_{deposit_ref}"

        doc = {
            "_id": f"{customer_number}_{deposit_ref}",
            "id": f"{customer_number}_{deposit_ref}",
            "customerNumber": customer_number,
            "depositRef": deposit_ref,
            "paymentLines": grouped_lines.get(key, [])
        }
        docs.append(doc)

    db.paymentHeaders.insert_many(docs)