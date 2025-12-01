from app import mongo
from bson.objectid import ObjectId

class Book:
    @staticmethod
    def get_all():
        return list(mongo.db.books.find())
    
    @staticmethod
    def get_by_id(book_id):
        return mongo.db.books.find_one({'_id': ObjectId(book_id)})
    
    @staticmethod
    def create(data):
        return mongo.db.books.insert_one(data)
    
    @staticmethod
    def update(book_id, data):
        return mongo.db.books.update_one({'_id': ObjectId(book_id)}, {'$set': data})
    
    @staticmethod
    def delete(book_id):
        return mongo.db.books.delete_one({'_id': ObjectId(book_id)})
    
    @staticmethod
    def search(query):
        return list(mongo.db.books.find({
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'author': {'$regex': query, '$options': 'i'}}
            ]
        }))