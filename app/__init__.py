from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from .config import Config

mongo = PyMongo()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mongo.init_app(app)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.get_by_id(user_id)
    
    # Register blueprints
    from .routes import books, auth, admin, client, favorites
    app.register_blueprint(books.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(client.bp)
    app.register_blueprint(favorites.bp)
    
    return app