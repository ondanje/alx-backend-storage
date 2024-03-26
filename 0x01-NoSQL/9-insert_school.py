#!/usr/bin/env python3
"""
function that inserts a new document in a collection based on kwargs
and returns the id
"""


def insert_school(mongo_collection, **kwargs):
    """
    function that inserts a new document in a collection based on kwargs:
    """
    new_doc = mongo_collection.insert_one(kwargs)

    return new_doc.inserted_id
