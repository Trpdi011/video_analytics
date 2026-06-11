from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27018/"
)

db = client["crowd_monitoring"]

print(
    "minute_data:",
    db["minute_data"].count_documents({})
)

print(
    "summary_data:",
    db["summary_data"].count_documents({})
)