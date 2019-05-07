import pymongo


# Create the initial db
client = pymongo.MongoClient("mongodb://mongo")
wim_db = client.wim


def create_index(collection_name, index_list):
	"""
	Add more indexes to the collections
	"""
	collection = wim_db[collection_name]
	for new_index in index_list:
		collection.create_index([(new_index, pymongo.ASCENDING)], unique=True)
	return sorted(list(collection.index_information()))


def index_db():
	"""
	Returns a list of all the collections in the db
	"""
	return wim_db.list_collection_names()


def index_col(collection_name):
	"""
	Returns the data of a specific collection
	"""
	collection = wim_db[collection_name]
	return collection.find({})
	

def col_add(collection_name, data):
	"""
	Inserts the data into the collection
	"""
	collection = wim_db[collection_name]
	return collection.insert_one(data).inserted_id


def col_insert(collection_name, data):
	"""
	Inserts the data into the collection
	"""
	collection = wim_db[collection_name]
	return collection.insert_many(data)

