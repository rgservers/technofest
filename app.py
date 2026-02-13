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

col1 = mydb['mycollection']

app = flask.Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return flask.send_file('templates/index.html')

@app.route('/search', methods=['GET'])
def search():
    query = flask.request.args.get('query')
    # get the query embedding
    # search in elasticsearch
    # return the results
    col1.insert_one({"query": query, "timestamp":"hi" })
    return "inserted"

