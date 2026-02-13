import pymongo 
from sentence_transformers import SentenceTransformer, util
import json

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['VadaPavFashion']
col1 = mydb['fashion_items']

def find_relevant():
    users_collection = mydb['users']

    vec1 = col1.find()

    data = json.loads(str(vec1))
    model = SentenceTransformer("all-MiniLM-L6-v2")

    embed_1 = model.encode('text')
    result = []

    for key, value in data.items():
        embed_2 = []
        result.append(util.cos_sim(embed_1, embed_2))

    result.sort(reverse=True)

