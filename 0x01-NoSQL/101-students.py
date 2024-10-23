#!/usr/bin/env python3
"""
    top students  by average
"""

def top_students(mongo_collection):
    """
    Returns all students sorted by their average score.

    Args:
        mongo_collection (pymongo.collection.Collection): MongoDB collection containing students.

    Returns:
        list: Sorted list of students with their average score added as 'averageScore'.
    """
    # Pipeline to calculate average score and sort by it
    pipeline = [
        {
            '$project': {
                'name': 1,
                'topics': 1,
                'averageScore': { '$avg': '$topics.score' }  # Calculate average score
            }
        },
        {
            '$sort': { 'averageScore': -1 }  # Sort by averageScore in descending order
        }
    ]
    
    return list(mongo_collection.aggregate(pipeline))

