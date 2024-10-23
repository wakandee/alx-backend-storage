#!/usr/bin/env python3
""" 102. Log stats with top 10 IPs
"""

from pymongo import MongoClient


def log_stats():
    """ Log stats for Nginx logs stored in MongoDB. """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    
    # Count total logs
    total_logs = logs_collection.count_documents({})
    
    # Count different HTTP methods
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    method_counts = {method: logs_collection.count_documents({'method': method}) for method in methods}
    
    # Count status check paths (GET /status)
    status_check = logs_collection.count_documents({"method": "GET", "path": "/status"})
    
    # Print basic log statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check} status check")
    
    # Top 10 most present IPs
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},  # Group by IP and count occurrences
        {"$sort": {"count": -1}},  # Sort by count in descending order
        {"$limit": 10}  # Limit to top 10 IPs
    ]
    top_ips = logs_collection.aggregate(pipeline)
    
    # Display top 10 IPs
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()

