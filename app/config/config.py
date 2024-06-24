class Config:
    # MongoDB configuration
    MONGO_URI = 'mongodb://localhost:27017/'
    DATABASE_NAME = 'fyp'
    MONGO_OPTIONS = {
        # Add additional options here if needed
        # For example:
        'connectTimeoutMS': 2000,
        'socketTimeoutMS': 2000,
    }