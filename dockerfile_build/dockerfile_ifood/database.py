import pymongo
# import __main__ as main

class Database:

    __client = None
    __database = None
    __collection = None

    @staticmethod
    def setConnectionWithMongo(name='food', **kwargs):

        Database.__client = pymongo.MongoClient(**kwargs)
        Database.__database = Database.__client['raw_food_data']
        Database.__collection = Database.__database[name]
        # Database.__collection = Database.__database[main.__file__]

    @staticmethod
    def getConnectionWithMongo():
        return Database.__collection


