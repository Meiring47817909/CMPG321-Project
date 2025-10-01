from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd
from datetime import datetime, timedelta

def excel_date_to_iso(value):
    """Convert Excel serial date or pandas Timestamp to ISO format."""
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    try:
        base_date = datetime(1899, 12, 30)
        return (base_date + timedelta(days=int(value))).isoformat()
    except Exception:
        return None

def safe_str(val):
    return str(val).strip() if pd.notna(val) else "N/A"

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def load_payment_headers(file_path):
    header_df = load_sheet(file_path, "Payment_Header")
    lines_df = load_sheet(file_path, "Payment_Lines")

    # Merge headers and lines on CUSTOMER_NUMBER + DEPOSIT_REF
    merged_df = pd.merge(
        lines_df,
        header_df,
        how="inner",
        on=["CUSTOMER_NUMBER", "DEPOSIT_REF"]
    )

    # Group by CUSTOMER_NUMBER + DEPOSIT_REF
    grouped = merged_df.groupby(["CUSTOMER_NUMBER", "DEPOSIT_REF"])

    docs = []
    for (customer_number, deposit_ref), group in grouped:
        payment_lines = []
        for _, row in group.iterrows():
            payment_lines.append({
                "finPeriod": safe_str(row["FIN_PERIOD"]),
                "depositDate": excel_date_to_iso(row["DEPOSIT_DATE"]),
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