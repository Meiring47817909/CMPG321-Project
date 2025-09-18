from config.mongo_config import db
from loaders.base_loader import load_sheet
import pandas as pd

def load_age_analysis(file_path):
    df = load_sheet(file_path, "Age_Analysis")

    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    docs = []
    for _, row in df.iterrows():
        doc = {
            "_id": {
                "customerNumber": str(row["CUSTOMER_NUMBER"]),
                "finPeriod": str(row["FIN_PERIOD"])
            },
            "totalDue": safe_float(row.get("TOTAL_DUE")),
            "amtCurrent": safe_float(row.get("AMT_CURRENT")),
            "amt30Days": safe_float(row.get("AMT_30_DAYS")),
            "amt60Days": safe_float(row.get("AMT_60_DAYS")),
            "amt90Days": safe_float(row.get("AMT_90_DAYS")),
            "amt120Days": safe_float(row.get("AMT_120_DAYS")),
            "amt150Days": safe_float(row.get("AMT_150_DAYS")),
            "amt180Days": safe_float(row.get("AMT_180_DAYS")),
            "amt210Days": safe_float(row.get("AMT_210_DAYS")),
            "amt240Days": safe_float(row.get("AMT_240_DAYS")),
            "amt270Days": safe_float(row.get("AMT_270_DAYS")),
            "amt300Days": safe_float(row.get("AMT_300_DAYS")),
            "amt330Days": safe_float(row.get("AMT_330_DAYS")),
            "amt360Days": safe_float(row.get("AMT_360_DAYS"))
        }
        docs.append(doc)

    db.ageAnalysis.insert_many(docs)