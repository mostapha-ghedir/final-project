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
    
    # Test MongoDB connection (non-blocking)
    with app.app_context():
        try:
            mongo.db.command('ping')
            print(f"✓ Connected to MongoDB: {app.config['MONGO_URI']}")
        except Exception as e:
            print(f"⚠ MongoDB connection failed (will retry): {e}")
            print(f"MongoDB URI: {app.config['MONGO_URI']}")
            # Don't fail, let the app start and retry connections later
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.get_by_id(user_id)
    
    # Health check route
    @app.route('/health')
    def health_check():
        try:
            mongo.db.command('ping')
            return {'status': 'healthy', 'database': 'connected'}, 200
        except Exception as e:
            return {'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}, 500
    
    # Register blueprints
    from .routes import books, auth, admin, client, favorites
    app.register_blueprint(books.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(client.bp)
    app.register_blueprint(favorites.bp)
    
    return app