import pymongo
from sentence_transformers import SentenceTransformer, util
import json
import logging
import os
import contextlib
import heapq

os.environ["TQDM_DISABLE"] = "1"
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

def find_relevant(query_text, limit=100):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['VadaPavFashion']
    col1 = mydb['fashion_items']

    vector_data = []

    projection = {
        "id": 1,
        "combined_vector": 1,
        "_id": 0
    }
    results = col1.find({}, projection).limit(limit) 
    for doc in results:
        product_id = doc.get("id")
        vector = doc.get("combined_vector")
        if product_id and vector:
            vector_data.append((product_id, vector))

    if not vector_data:
        return {}

    with contextlib.redirect_stdout(open(os.devnull, 'w')), contextlib.redirect_stderr(open(os.devnull, 'w')):
        model = SentenceTransformer("all-MiniLM-L6-v2")

    embed_1 = model.encode(query_text)
    similarities = {}

    for product_id, embed_2 in vector_data:
        similarity = util.cos_sim(embed_1, embed_2).item()
        similarities[product_id] = similarity

    return  heapq.nlargest(100, similarities.items(), key=lambda item: item[1])


if __name__ == "__main__":
    result = find_relevant("Stylish men's shirt")
    print(json.dumps(result))


