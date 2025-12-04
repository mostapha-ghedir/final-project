from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app import mongo

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.password_hash = user_data['password_hash']
        self.role = user_data.get('role', 'client')
        self.is_active_user = user_data.get('is_active', True)
    
    def is_active(self):
        return self.is_active_user
    
    def is_admin(self):
        return self.role in ['admin', 'super_admin']
    
    def is_super_admin(self):
        return self.role == 'super_admin'
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def create(username, email, password, role='client'):
        password_hash = generate_password_hash(password)
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'role': role,
            'is_active': True
        }
        result = mongo.db.users.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return User(user_data)
    
    @staticmethod
    def get_by_username(username):
        user_data = mongo.db.users.find_one({'username': username})
        return User(user_data) if user_data else None
    
    @staticmethod
    def get_by_id(user_id):
        try:
            user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            return User(user_data) if user_data else None
        except:
            return None
    
    @staticmethod
    def get_all():
        users = mongo.db.users.find()
        return [User(user) for user in users]
    
    @staticmethod
    def update_role(user_id, role):
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'role': role}}
        )
    
    @staticmethod
    def delete(user_id):
        mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    
    def add_favorite(self, book_id):
        mongo.db.users.update_one(
            {'_id': ObjectId(self.id)},
            {'$addToSet': {'favorites': str(book_id)}}
        )
    
    def remove_favorite(self, book_id):
        mongo.db.users.update_one(
            {'_id': ObjectId(self.id)},
            {'$pull': {'favorites': str(book_id)}}
        )
    
    def get_favorites(self):
        user_data = mongo.db.users.find_one({'_id': ObjectId(self.id)})
        return user_data.get('favorites', [])
    
    def is_favorite(self, book_id):
        return str(book_id) in self.get_favorites()
    
    def update_password(self, new_password):
        password_hash = generate_password_hash(new_password)
        mongo.db.users.update_one(
            {'_id': ObjectId(self.id)},
            {'$set': {'password_hash': password_hash}}
        )
        self.password_hash = password_hash
    
    def update_profile(self, username=None, email=None):
        update_data = {}
        if username:
            update_data['username'] = username
            self.username = username
        if email:
            update_data['email'] = email
            self.email = email
        
        if update_data:
            mongo.db.users.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': update_data}
            )