import pymongo # import pymongo for database connection
from gridfs import GridFS # import GridFS for file storage
from config import MONGODB_URI

# Create database connections
client = pymongo.MongoClient(MONGODB_URI) # create a client
gamificationdb = client.get_database('Gamificationdatabase') # get the database

#gamification_collection = gamificationdb.gamificationcollection # get the collection for gamification
users_collection = gamificationdb.users # get the collection for users

# Test connection
client.server_info()