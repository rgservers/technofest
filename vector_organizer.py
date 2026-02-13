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

logger = logging.getLogger(__name__)

def find_relevant(query_text, limit=1000):
    logger.info(f"find_relevant called with query: {query_text}, limit: {limit}")
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['VadaPavFashion']
    col1 = mydb['fashion_items']
    logger.debug("Connected to MongoDB for vector search")

    vector_data = []

    projection = {
        "id": 1,
        "combined_vector": 1,
        "_id": 0
    }
    results = col1.find({}, projection)  # Fetch all items with vectors
    for doc in results:
        product_id = doc.get("id")
        vector = doc.get("combined_vector")
        if product_id and vector:
            vector_data.append((product_id, vector))
    logger.info(f"Loaded {len(vector_data)} items with vectors")

    if not vector_data:
        logger.warning("No vector data found")
        return {}

    with contextlib.redirect_stdout(open(os.devnull, 'w')), contextlib.redirect_stderr(open(os.devnull, 'w')):
        model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.debug("Model loaded")

    embed_1 = model.encode(query_text)
    logger.debug(f"Query encoded to vector of shape: {embed_1.shape}")
    similarities = {}

    for product_id, embed_2 in vector_data:
        similarity = util.cos_sim(embed_1, embed_2).item()
        similarities[product_id] = similarity

    # Return top 10 most similar items
    return [[k, v] for k, v in heapq.nlargest(10, similarities.items(), key=lambda item: item[1])]
if __name__ == "__main__":
    result = find_relevant("Stylish men's shirt")
    print(json.dumps(result))


