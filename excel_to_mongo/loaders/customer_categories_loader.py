from config.mongo_config import db
import pandas as pd

def load_customer_categories(file_path):
    # Force CCAT_CODE to be read as string
    df = pd.read_excel(file_path, sheet_name="Customer_Categories", dtype={"CCAT_CODE": str})

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    docs = []
    for _, row in df.iterrows():
        doc = {
            "_id": safe_str(row["CCAT_CODE"]),
            "ccatDesc": safe_str(row["CCAT_DESC"])
        }
        docs.append(doc)

    db.customerCategories.insert_many(docs)