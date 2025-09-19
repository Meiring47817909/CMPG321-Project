from config.mongo_config import db
from loaders.base_loader import load_sheet
from utils.date_converter import excel_serial_to_iso
import pandas as pd

def load_sale_headers(file_path):
    # Load both sheets
    headers_df = load_sheet(file_path, "Sales_Header")
    lines_df = load_sheet(file_path, "Sales_Line")

    # Merge line items with header metadata
    merged_df = pd.merge(
        lines_df,
        headers_df,
        how="left",
        on="DOC_NUMBER",
        suffixes=("", "_header")
    )

    grouped = merged_df.groupby("DOC_NUMBER")

    docs = []
    for doc_number, group in grouped:
        sale_lines = []
        for _, row in group.iterrows():
            sale_lines.append({
                "inventoryCode": str(row["INVENTORY_CODE"]),
                "quantity": int(row["QUANTITY"]),
                "unitSellPrice": float(row["UNIT_SELL_PRICE"]),
                "totalLinePrice": float(row["TOTAL_LINE_PRICE"]),
                "lastCost": float(row["LAST_COST"])
            })

        # Use first row for header fields
        header_row = group.iloc[0]
        doc = {
            "_id": str(doc_number),
            "transtypeCode": str(header_row["TRANSTYPE_CODE"]),
            "repCode": str(header_row["REP_CODE"]),
            "customerNumber": str(header_row["CUSTOMER_NUMBER"]),
            "transDate": excel_serial_to_iso(header_row["TRANS_DATE"]),
            "finPeriod": str(header_row["FIN_PERIOD"]),
            "saleLines": sale_lines
        }
        docs.append(doc)

    db.saleHeaders.insert_many(docs)