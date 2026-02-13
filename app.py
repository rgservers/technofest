import pymongo
import elasticsearch
import flask
import numpy as np

mainclient = pymongo.MongoClient("mongodb://localhost:27017/")
maindb = mainclient["VadaPavFassion"]

# get each image
# get the model
# store image embeddings