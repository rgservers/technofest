import pymongo
import elasticsearch
import flask
import numpy as np

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["VadaPavFassion"]
mongo_collection = mongo_db["sureshites"]

app = flask.Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return "Welcome to VadaPavFassion API"
