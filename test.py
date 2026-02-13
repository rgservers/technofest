import pymongo

# 1. Establish connection and select collection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["VadaPavFashion"]
mycol = mydb["fashion_items"]

# 2. Use find() with projection to get only the 'name' field
# {} is the query (empty means all documents)
# {"name": 1, "_id": 0} is the projection (include 'name', exclude '_id')
projection = {
    "id": 1, 
    "vector": 1, 
    "_id": 0
}

# 2. Execute the find
results = mycol.find({}, projection)
# 3. Print the count of documents
print(f"Estimated document count: {results}")

for doc in results:
    product_id = doc.get("id")
    vector_data = doc.get("vector")
    print(f"ID: {product_id} | Vector Length: {vector_data}")
