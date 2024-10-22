#!/usr/bin/env python3
"""
This script provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":

    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_collection = client.logs.nginx
    print("{} logs".format(nginx_collection.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print("\tmethod {}: {}".format(
            method,
            len(list(nginx_collection.find({"method": method}))))
            )
    print("{} status check".format(
        len(list(nginx_collection.find({
            "method": "GET",
            "path": "/status"
            })))))
