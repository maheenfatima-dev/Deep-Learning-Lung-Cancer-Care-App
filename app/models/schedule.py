# models/schedule.py

from pymongo import MongoClient
from bson import ObjectId
from config.config import Config

class Schedule:
    @staticmethod
    def get_db():
        # Establish connection to MongoDB
        mongo_client = MongoClient(Config.MONGO_URI)
        return mongo_client[Config.DATABASE_NAME]
    def __init__(self, user_id, name, type, date, time, description=None):
        self.user_id = user_id
        self.name = name 
        self.type = type
        self.date = date
        self.time = time
        self.description = description

        # Establish connection to MongoDB
        self.mongo_client = MongoClient(Config.MONGO_URI)
        self.db = self.mongo_client[Config.DATABASE_NAME]

    def save(self):
        self.db.schedules.insert_one({
            "user_id": self.user_id,
            "name": self.name,
            "type": self.type,
            "date": self.date,
            "time": self.time,
            "description": self.description
        })
        self.mongo_client.close()

    @staticmethod
    def get_all(user_id, type=None):
    # Retrieve all schedules for a specific user and optionally filtered by type from the database
        mongo_client = MongoClient(Config.MONGO_URI)
        db =  mongo_client[Config.DATABASE_NAME]
        # db = Schedule.get_db()
        query = {'user_id': ObjectId(user_id)}
        if type:
            query['type'] = type
        listing = list(db.schedules.find(query))
        mongo_client.close()
        return listing

    @staticmethod
    def get_by_id(schedule_id, user_id):
        mongo_client = MongoClient(Config.MONGO_URI)
        db =  mongo_client[Config.DATABASE_NAME]
        # db = Schedule.get_db()
        # Retrieve a schedule by its ID for a specific user from the database

        listing = db.schedules.find_one({'_id': schedule_id,'user_id':user_id})
        mongo_client.close()
        return listing

    @staticmethod
    def update(schedule_id, user_id, **kwargs):
        mongo_client = MongoClient(Config.MONGO_URI)
        db =  mongo_client[Config.DATABASE_NAME]
        # db = Schedule.get_db()
        # Update a schedule by its ID for a specific user in the database
        data = db.schedules.update_one({'_id': ObjectId(schedule_id), 'user_id': ObjectId(user_id)}, {'$set': kwargs})
        mongo_client.close()
        return data

    @staticmethod
    def delete(schedule_id):
        # Delete a schedule by its ID for a specific user from the database
        mongo_client = MongoClient(Config.MONGO_URI)
        db =  mongo_client[Config.DATABASE_NAME]
        # db = Schedule.get_db()
        data = db.schedules.delete_one({'_id': ObjectId(schedule_id)})
        mongo_client.close()
        return data
