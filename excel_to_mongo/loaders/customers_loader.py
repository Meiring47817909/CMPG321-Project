from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_customers(file_path):
    # Load both sheets
    customer_df = load_sheet(file_path, "Customer")
    params_df = load_sheet(file_path, "Customer_Account_Parameters")

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

    def parse_params(group):
        return [safe_str(p) for p in group["PARAMETER"].dropna().unique()]

    # Group parameters by customerNumber
    param_groups = params_df.groupby("CUSTOMER_NUMBER")

    docs = []
    for _, row in customer_df.iterrows():
        cust_id = safe_str(row["CUSTOMER_NUMBER"])
        account_params = parse_params(param_groups.get_group(cust_id)) if cust_id in param_groups.groups else []

        doc = {
            "_id": cust_id,
            "ccatCode": safe_str(row["CCAT_CODE"]),
            "regionCode": safe_str(row["REGION_CODE"]),
            "repCode": safe_str(row["REP_CODE"]),
            "settleTerms": safe_int(row.get("SETTLE_TERMS")),
            "normalPayterms": safe_int(row.get("NORMAL_PAYTERMS")),
            "discount": safe_float(row.get("DISCOUNT")),
            "creditLimit": safe_float(row.get("CREDIT_LIMIT")),
            "accountParams": account_params
        }
        docs.append(doc)

    db.customers.insert_many(docs)