from opportunity import client

def connect(db_name):
	# create or connect to db
	db = client[db_name]

	return db