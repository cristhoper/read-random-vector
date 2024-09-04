import os
from pymongo import MongoClient
from flask_restful import Resource
from flask import request
from datetime import datetime
import ast

import bson.json_util as dbson

class DatabaseServices(object):

    # credential information
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
    MONGODB_HOST = os.environ.get('MONGODB_HOST')

    URI = f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}'
    DATABASE = None

    def connect():
        client = MongoClient(DatabaseServices.URI)
        DatabaseServices.DATABASE = client.rng_data

    def find():
        '''
        method to find document
        '''
        DatabaseServices.connect()
        print(DatabaseServices.DATABASE.sensors)

        return DatabaseServices.DATABASE.sensors.find({}, {'_id': False})

    def insert(item: dict):
        DatabaseServices.connect()
        return DatabaseServices.DATABASE.sensors.insert_one(item)



class DatabaseHandler(Resource):
    def get(self):

        data = DatabaseServices.find()

        result = dbson.dumps(data)
        result = dbson.loads(result)
        if len(result) > 0:
            return result

        return f'NO DATA YET'

    def post(self):
        data = request.get_data().decode('utf-8')
        data_dict = ast.literal_eval(data)
        result = datetime.now()
        data_dict['timestamp'] = result.timestamp()
        print(data_dict)
        DatabaseServices.insert(data_dict)
