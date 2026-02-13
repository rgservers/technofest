import pymongo
import elasticsearch
import flask
import numpy as np

mainclient = pymongo.MongoClient("mongodb://localhost:27017/")
maindb = mainclient["VadaPavFassion"]

collection1 = maindb.create_collection["sureshites"]