import app
import pymongo

@app.route("/matcher")
def match():
    client = pymongo.MongoClient('mongodb://testjkerwdkjrds')
    db = pymongo.database.Database(client, 'db')
    users = db['users']

