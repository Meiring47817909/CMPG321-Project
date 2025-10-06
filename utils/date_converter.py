import pandas as pd
from datetime import datetime, timedelta

def excel_serial_to_iso(serial):
    if pd.isna(serial):
        return None
    if isinstance(serial, (pd.Timestamp, datetime)):
        return serial.isoformat()
    return (datetime(1899, 12, 30) + timedelta(days=int(serial))).isoformat()