#!/usr/bin/env python3
"""
script to list all docs in a collection
"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """
    function to list all documents in a collection
    """
    docs = list(mongo_collection.find({}))
    return docs
