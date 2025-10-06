from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd
from datetime import datetime

def parse_fin_period(val):
    try:
        return datetime.strptime(str(val), "%Y%m")
    except (ValueError, TypeError):
        return None

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def safe_str(val):
    return str(val).strip() if pd.notna(val) else "N/A"

def load_payment_headers(file_path):
    header_df = load_sheet(file_path, "Payment_Header")
    lines_df = load_sheet(file_path, "Payment_Lines")

    merged_df = pd.merge(
        lines_df,
        header_df,
        how="inner",
        on=["CUSTOMER_NUMBER", "DEPOSIT_REF"]
    )

    grouped = merged_df.groupby(["CUSTOMER_NUMBER", "DEPOSIT_REF"])

    docs = []
    for (customer_number, deposit_ref), group in grouped:
        payment_lines = []
        for _, row in group.iterrows():
            payment_lines.append({
                "finPeriod": parse_fin_period(row["FIN_PERIOD"]),
                "depositDate": row["DEPOSIT_DATE"],  # already datetime from Excel
                "bankAmt": safe_float(row["BANK_AMT"]),
                "discount": safe_float(row["DISCOUNT"]),
                "totPayment": safe_float(row["TOT_PAYMENT"])
            })

        doc = {
            "_id": {
                "customerNumber": safe_str(customer_number),
                "depositRef": safe_str(deposit_ref)
            },
            "paymentLines": payment_lines
        }
        docs.append(doc)

    db.paymentHeaders.insert_many(docs)