import pymongo
import json
from bson.json_util import dumps
from keys import *

client = pymongo.MongoClient(os.getenv('MONGO', None))

db = client.fb

def add(idVal, string):
	db.posts.insert_one({"id": idVal, "string": string})

def read():
	for post in db.posts.find():
		print(post)

def get_entry(idVal):
	return db.posts.find_one({"id": idVal})['string']


def update():
	myquery = { "blog": "sample_airbnb" }
	newvalues = { "$set": { "blog": "updated_sample_airbnb" } }

	db.posts.update_one(myquery, newvalues)

if __name__ == '__main__':
	add('chris', 'subway', 'palo alto', '12345')

	print("\n\nOLD\n\n")
	read()
	print("\n\nNEW\n\n")
	read()
	print get_user('asdfadsfasdfchris')