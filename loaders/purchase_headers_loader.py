from config.mongo_config import db
from loaders.base_loader import load_sheet
from utils.date_converter import excel_serial_to_iso
import pandas as pd

def load_purchase_headers(file_path):
    # Load both sheets
    headers_df = load_sheet(file_path, "Purchases_Headers")
    lines_df = load_sheet(file_path, "Purchases_Lines")

    # Merge line items with header metadata
    merged_df = pd.merge(
        lines_df,
        headers_df,
        how="left",
        on="PURCH_DOC_NO",
        suffixes=("", "_header")
    )

    grouped = merged_df.groupby("PURCH_DOC_NO")

    docs = []
    for doc_no, group in grouped:
        purchase_lines = []
        for _, row in group.iterrows():
            purchase_lines.append({
                "inventoryCode": str(row["INVENTORY_CODE"]),
                "quantity": int(row["QUANTITY"]),
                "unitCostPrice": float(row["UNIT_COST_PRICE"]),
                "totalLineCost": float(row["TOTAL_LINE_COST"])
            })

        header_row = group.iloc[0]
        doc = {
            "_id": str(doc_no),
            "supplierCode": str(header_row["SUPPLIER_CODE"]),
            "purchaseDate": excel_serial_to_iso(header_row["PURCH_DATE"]),
            "purchaseLines": purchase_lines
        }
        docs.append(doc)

    db.purchaseHeaders.insert_many(docs)