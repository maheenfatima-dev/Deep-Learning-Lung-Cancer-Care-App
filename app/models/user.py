# models/user.py

from pymongo import MongoClient
from config.config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    @staticmethod
    def get_db():
        # Establish connection to MongoDB
        mongo_client = MongoClient(Config.MONGO_URI)
        return mongo_client[Config.DATABASE_NAME]
    def __init__(self, name, email, password, gender, age, address):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)  # Hash the password before saving
        self.gender = gender
        self.age = age
        self.address = address

        # Establish connection to MongoDB
        self.mongo_client = MongoClient(Config.MONGO_URI)
        self.db = self.mongo_client[Config.DATABASE_NAME]

    def save(self):
        # Insert user into the database
        self.db.users.insert_one({
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "gender": self.gender,
            "age": self.age,
            "address": self.address
        })
        self.mongo_client.close()

    @staticmethod
    def get_by_email(email):
        # Retrieve a user by email
        mongo_client = MongoClient(Config.MONGO_URI)
        db = mongo_client[Config.DATABASE_NAME]
        # db = User.get_db()
        data = db.users.find_one({'email': email}, {'_id': 0})
        mongo_client.close()
        return data
    
    @staticmethod
    def get_id_by_email(email):
        # db = User.get_db()
        mongo_client = MongoClient(Config.MONGO_URI)
        db = mongo_client[Config.DATABASE_NAME]
        data = db.users.find_one({'email':email})
        mongo_client.close()

        return data

    @staticmethod
    def login(email, password):
        # Check if email exists
        mongo_client = MongoClient(Config.MONGO_URI)
        db = mongo_client[Config.DATABASE_NAME]

        # db = User.get_db()
    
    # Check if email exists
        user = db.users.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
        # Login successful
            mongo_client.close()
            return True
        else:
            # Login failed
            mongo_client.close()
            return False

    @staticmethod
    def delete(email):
        # Delete a user by email
        mongo_client = MongoClient(Config.MONGO_URI)
        db = mongo_client[Config.DATABASE_NAME]
        # db = User.get_db()

    # Delete a user by email
        result = db.users.delete_one({'email': email})
        mongo_client.close()
        return result.deleted_count > 0

    def log_in(self):
        # Log in user
        mongo_client = MongoClient(Config.MONGO_URI)
        db = mongo_client[Config.DATABASE_NAME]
        # db = User.get_db()
        db.user_logs.insert_one({
            "user_email": self.email,
            "login_time": datetime.now()
        })
        mongo_client.close()

    def log_out(self):
        # Log out user
        mongo_client = MongoClient(Config.MONGO_URI)
        db = mongo_client[Config.DATABASE_NAME]
        
        db = User.get_db()
        result = db.user_logs.insert_one({
            "user_email": self.email,
            "logout_time": datetime.now()
        })
        mongo_client.close()
        return result
