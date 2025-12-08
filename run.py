from app import create_app
from app.models.user import User

app = create_app()

if __name__ == '__main__':
    # Create super admin on startup (delete and recreate if exists)
    with app.app_context():
        existing_admin = User.get_by_username('admin')
        if existing_admin:
            User.delete(existing_admin.id)
            print("⚠ Existing admin user deleted")
        
        User.create(
            username='admin',
            email='admin@booklibrary.com',
            password='admin123',
            role='super_admin'
        )
        print("✓ Super admin created: admin / admin123")
    
    app.run(host='0.0.0.0', port=5001)