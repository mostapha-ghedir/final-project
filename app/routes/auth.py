from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('client.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.get_by_username(username)
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            
            # Redirect based on role
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('client.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('client.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form.get('role', 'client')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if User.get_by_username(username):
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        # Create new user with role
        user = User.create(username, email, password, role)
        login_user(user)
        flash('Registration successful!', 'success')
        
        if user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('client.dashboard'))
    
    return render_template('register.html')

@bp.route('/register-admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        admin_code = request.form['admin_code']
        
        # Check admin code
        if admin_code != 'ADMIN2024':
            flash('Invalid admin code', 'error')
            return render_template('register_admin.html')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register_admin.html')
        
        if User.get_by_username(username):
            flash('Username already exists', 'error')
            return render_template('register_admin.html')
        
        # Create admin user
        user = User.create(username, email, password, 'admin')
        login_user(user)
        flash('Admin registration successful!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('register_admin.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('books.index'))