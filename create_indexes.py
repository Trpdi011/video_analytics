from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27018/")
db = client["crowd_monitoring"]

db["minute_data"].create_index(
    "timestamp",
    expireAfterSeconds=2592000
)

print("TTL Index Created")