from pymongo import MongoClient
uri = "mongodb+srv://thiagorodrigues:T7XOMsm2X3pRHtEu@unit-ml-instance.mf9cgqy.mongodb.net/?retryWrites=true&w=majority&appName=UNIT-ML-INSTANCE"
client = MongoClient(uri)
print(client.list_database_names())