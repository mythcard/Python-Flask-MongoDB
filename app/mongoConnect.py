import pymongo

# establish a connection to the database
#connection = pymongo.MongoClient("mongodb://localhost:27017")
connection = pymongo.MongoClient('mongodb://mongodb:27017')

db = connection.checkOut
#productCatalog = db.productCatalog


