import pymongo 
from sentence_transformers import SentenceTransformer, util

def find_relevant(data):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['VadaPavFashion']
    col1 = mydb['fashion_items']

    vector_data = []

    projection = {
        "id": 1, 
        "vector": 1, 
        "_id": 0
    }
    results = col1.find({}, projection)
    for doc in results:
        product_id = doc.get("id")
        vector_data = doc.get("vector")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embed_1 = model.encode('text')
    result = {}

    for key, value in vector_data:
        embed_2 = data
        result['key'] = (util.cos_sim(embed_1, embed_2))

    return {k: v for k, v in sorted(result.items())}


myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['VadaPavFashion']
col1 = mydb['fashion_items']
projection = {
    "id": 1, 
    "vector": 1, 
    "_id": 0
}
results = col1.find({}, projection)
for doc in results:
    product_id = doc.get("id")
    vector_data = doc.get("vector")

result = find_relevant("Stylish men's shirt")
print(result)


