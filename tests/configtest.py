import unittest
import os

from what2do2day import app

from mockupdb import MockupDB, go, Command
from pymongo import MongoClient
from mockupdb._bson import ObjectId as mockup_oid
from json import dumps


class GetDataSourceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.server = MockupDB(auto_ismaster=True, verbose=True)
        self.server.run()
        # create mongo connection to mock server

        app.testing = True
        app.config['MONGO_URI'] = self.server.uri
        self.app = app.test_client()

    @classmethod
    def tearDownClass(self):
        self.server.stop()
