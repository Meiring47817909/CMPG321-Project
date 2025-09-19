from config.mongo_config import db
from loaders.base_loader import load_sheet

def load_suppliers(file_path):
    df = load_sheet(file_path, "Suppliers")
    records = df.to_dict(orient="records")
    for r in records:
        r["_id"] = str(r["SUPPLIER_CODE"]).zfill(3)
        r["supplierDesc"] = r["SUPPLIER_DESC"]
        r["exclsv"] = r["EXCLSV"]
        r["normalPayterms"] = int(r["NORMAL_PAYTERMS"])
        r["creditLimit"] = float(r["CREDIT_LIMIT"])
    db.suppliers.insert_many(records)