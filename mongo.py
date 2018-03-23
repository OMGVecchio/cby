from pymongo import MongoClient

class CbyMongo(object):

    def __init__(self, host='localhost', port=27017, dbName='cby'):
        client = MongoClient(host, port)
        self.db = client[dbName]

    def getTable(self, table):
        return self.db[table]
        