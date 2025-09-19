from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_products(file_path):
    # Load both sheets
    products_df = load_sheet(file_path, "Products")
    styles_df = load_sheet(file_path, "Products_Styles")

    def safe_str(val):
        return str(val).strip() if pd.notna(val) else "N/A"

    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    # Normalize column names for safety
    products_df.columns = products_df.columns.str.strip().str.upper()
    styles_df.columns = styles_df.columns.str.strip().str.upper()

    # Merge on INVENTORY_CODE
    merged_df = pd.merge(
        products_df,
        styles_df,
        how="left",
        on="INVENTORY_CODE",
        suffixes=("", "_style")
    )

    docs = []
    for _, row in merged_df.iterrows():
        doc = {
            "_id": safe_str(row["INVENTORY_CODE"]),
            "prodCatCode": safe_str(row["PRODCAT_CODE"]),
            "lastCost": safe_float(row["LAST_COST"]),
            "stockInd": safe_str(row["STOCK_IND"]),
            "styles": {
                "gender": safe_str(row.get("GENDER")),
                "material": safe_str(row.get("MATERIAL")),
                "style": safe_str(row.get("STYLE")),
                "colour": safe_str(row.get("COLOUR")),
                "branding": safe_str(row.get("BRANDING")),
                "qualProbs": safe_str(row.get("QUAL_PROBS"))
            }
        }
        docs.append(doc)

    db.products.insert_many(docs)