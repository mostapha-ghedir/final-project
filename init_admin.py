#!/usr/bin/env python3
"""
Initialize the database with an admin user.
Run this script once to create the first admin user.
"""

from app import create_app
from app.models.user import User

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.get_by_username('admin')
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin_user = User.create(
            username='admin',
            email='admin@booklibrary.com',
            password='admin123',  # Change this password!
            role='admin'
        )
        
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@booklibrary.com")
        print("\n⚠️  IMPORTANT: Change the default password after first login!")

if __name__ == '__main__':
    create_admin_user()