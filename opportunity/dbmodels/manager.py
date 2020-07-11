from pymongo import MongoClient

# mongo client
client = MongoClient()
# connect to local host
client = MongoClient('localhost', 27017)

def connect(db_name):
	db = client[db_name]