from pymongo import MongoClient, errors

# Create the initial db
client = MongoClient("mongodb://mongo")
db = client.wim


def index_db():
    """
    Returns a list of all the collections in the db
    """
    return db.list_collection_names()


def index_col(collection_name):
    """
    Returns all data of a specific collection
    """
    collection = db[collection_name]
    return collection.find({})


def add(collection_name, data):
    """
    Inserts the data into the collection
    """
    collection = db[collection_name]
    return collection.insert_one(data).inserted_id


def add_many(collection_name, data):
    """
    Inserts a list of data into the collection
    """
    collection = db[collection_name]
    return collection.insert_many(data)


def get(collection_name, _id):
    """
    Get an item based on the the id
    """
    collection = db[collection_name]
    return collection.find_one({"_id": _id})


def delete(collection_name, _id):
    """
    Delete an item based on the the id
    """
    result = db[collection_name].delete_one({"_id": _id}).deleted_count
    return result


def update(collection_name, _id, json_data):
    """
    Update an item based on the the id
    """
    collection = db[collection_name]
    return collection.replace_one({"_id": _id}, json_data).modified_count


def count(collection_name):
    """
    Count the items of a collection
    """
    collection = db[collection_name]
    return collection.count_documents({})


def find(collection_name, data={}):
    """
    Find an item based on specific data
    """
    collection = db[collection_name]
    return collection.find_one(data)


def find_all(collection_name, data={}):
    """
    Find all the items based on specific data
    """
    collection = db[collection_name]
    return collection.find(data)


def delete_all(collection_name, data={}):
    """
    Delete all items based on specific data
    """
    collection = db[collection_name]
    return collection.delete_many(data)


# Define exceptions
dub_error = errors.DuplicateKeyError
