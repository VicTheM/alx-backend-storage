#!/usr/bin/env python3
"""
Defines a top_students function
"""


def top_students(mongo_collection):
    """Returns all students sorted by average score"""
    students = list(mongo_collection.find())

    for student in students:
        topics = student.get('topics', [])
        if topics:
            avg_score = sum(topic['score'] for topic in topics) / len(topics)
            student['averageScore'] = avg_score
        else:
            student['averageScore'] = 0

    sorted_students = sorted(
        students,
        key=lambda x: x['averageScore'],
        reverse=True)

    return sorted_students
