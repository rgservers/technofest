import pymongo
import elasticsearch

mainclient = pymongo.MongoClient("mongodb://localhost:27017/")
maindb = mainclient["VadaPavFassion"]

collection1 = maindb.create_collection["sureshites"]