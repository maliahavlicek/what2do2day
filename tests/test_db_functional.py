"""
This file (tes_db_functionality.py) contains the functional tests for the blueprint routing.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the event, places and reviews blueprints.
"""

import pymongo
from pymongo import MongoClient

myclient = MongoClient("mongodb://localhost:27017/")

mydb = myclient["test"]


def test_home_page():
    pass
