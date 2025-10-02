from config.mongo_config import db
import pandas as pd

def load_customer_categories(file_path):
    df = pd.read_excel(file_path, sheet_name="Customer_Categories")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    def safe_int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return None  # skip invalid IDs

    for _, row in df.iterrows():
        _id = safe_int(row["CCAT_CODE"])
        if _id is None:
            continue

        doc = {
            "_id": _id,
            "ccatDesc": safe_str(row["CCAT_DESC"])
        }

        db.customerCategories.replace_one({"_id": _id}, doc, upsert=True)