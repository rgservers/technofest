import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["VadaPavFashion"]
mycol = mydb["fashion_items"]

projection = {
    "id": 1, 
    "vector": 1, 
    "_id": 0
}

results = mycol.find({}, projection)
print(f"Estimated document count: {results}")

for doc in results:
    product_id = doc.get("id")
    vector_data = doc.get("vector")
    print(f"ID: {product_id} | Vector Length: {vector_data}")

    
