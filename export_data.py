from pymongo import MongoClient
import pandas as pd
import os

# =====================================
# MongoDB Connection
# =====================================

client = MongoClient(
    "mongodb://localhost:27018/"
)

db = client["crowd_monitoring"]

# =====================================
# Get Summary Data
# =====================================

data = list(

    db["summary_data"].find(
        {},
        {"_id": 0}
    )

)

if len(data) == 0:

    print(
        "No Summary Data Found"
    )

    exit()

# =====================================
# Convert to DataFrame
# =====================================

df = pd.DataFrame(data)

# =====================================
# Create Reports Folder
# =====================================

os.makedirs(
    "reports",
    exist_ok=True
)

# =====================================
# Save Excel File
# =====================================

from datetime import datetime

report_date = datetime.now().strftime(
    "%Y-%m-%d"
)

file_name = os.path.join(

    "reports",

    f"crowd_summary_report_{report_date}.xlsx"

)

# =====================================
# Success Message
# =====================================

print(
    f"Excel Created Successfully: {file_name}"
)