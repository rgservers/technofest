import pymongo
import elasticsearch
import flask
import numpy as np

elasticsearch_client = elasticsearch.Elasticsearch("http://localhost:9200")

mainclient = pymongo.MongoClient("mongodb://localhost:27017/")
maindb = mainclient["VadaPavFassion"]

# get each image
# get the model
# store image embeddings

myclient = pymongo.MongoClient('mongodb://localhost:27017/')

mydb = myclient['mydatabase']

app = flask.Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return flask.send_file('templates/index.html')
