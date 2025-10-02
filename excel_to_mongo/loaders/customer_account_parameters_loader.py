from config.mongo_config import db
import pandas as pd
from loaders.base_loader import load_sheet

def load_customer_account_parameters(file_path):
    df = load_sheet(file_path, "Customer_Account_Parameters")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    # Group parameters by CUSTOMER_NUMBER
    grouped = df.groupby("CUSTOMER_NUMBER")["PARAMETER"].apply(
        lambda x: [safe_str(param) for param in x if pd.notna(param)]
    ).reset_index()

    records = []
    for _, row in grouped.iterrows():
        record = {
            "_id": safe_str(row["CUSTOMER_NUMBER"]),
            "parameters": row["PARAMETER"]
        }
        records.append(record)

    db.customer_account_parameters.insert_many(records)