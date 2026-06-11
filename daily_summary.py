from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import os

# =====================================
# MongoDB Connection
# =====================================

client = MongoClient(
    "mongodb://localhost:27018/"
)

db = client["crowd_monitoring"]

# =====================================
# Today's Date
# =====================================

today = datetime.now().strftime(
    "%Y-%m-%d"
)

# =====================================
# Fetch Today's Summary Records
# =====================================

records = list(

    db["summary_data"].find(

        {
            "date": today
        },

        {
            "_id": 0
        }

    )

)

if len(records) == 0:

    print(
        "No Data Found"
    )

    exit()

# =====================================
# DataFrame
# =====================================

df = pd.DataFrame(records)

# =====================================
# Calculate Daily KPIs
# =====================================

daily_avg_occ = round(

    df[
        "average_occupancy"
    ].mean(),

    2

)

daily_peak_occ = max(

    df[
        "peak_occupancy"
    ]

)

daily_min_occ = min(

    df[
        "minimum_occupancy"
    ]

)

peak_row = df.loc[
    df[
        "peak_occupancy"
    ].idxmax()
]

most_crowded_slot = (

    peak_row["start_time"]

    +

    " - "

    +

    peak_row["end_time"]

)

# =====================================
# Create Summary DataFrame
# =====================================

summary_df = pd.DataFrame({

    "Metric": [

        "Daily Average Occupancy",
        "Daily Peak Occupancy",
        "Daily Minimum Occupancy",
        "Most Crowded Slot"

    ],

    "Value": [

        daily_avg_occ,
        daily_peak_occ,
        daily_min_occ,
        most_crowded_slot

    ]

})

# =====================================
# Create Reports Folder
# =====================================

os.makedirs(
    "reports",
    exist_ok=True
)

# =====================================
# Save Excel
# =====================================

file_name = os.path.join(

    "reports",

    f"daily_summary_{today}.xlsx"

)

summary_df.to_excel(

    file_name,

    index=False

)

# =====================================
# Success Message
# =====================================

print(

    f"Daily Summary Created Successfully: {file_name}"

)