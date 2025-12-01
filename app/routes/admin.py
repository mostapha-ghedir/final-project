from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app.models.book import Book
from app.models.user import User

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_books = len(Book.get_all())
    total_users = len(User.get_all())
    recent_books = Book.get_all()[:5]  # Get 5 most recent books
    
    stats = {
        'total_books': total_books,
        'total_users': total_users,
        'recent_books': recent_books
    }
    
    return render_template('admin_dashboard.html', stats=stats)

@bp.route('/books')
@login_required
@admin_required
def manage_books():
    books = Book.get_all()
    return render_template('book_list.html', books=books)

@bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.get_all()
    return render_template('manage_users.html', users=users)

@bp.route('/users/<user_id>/role', methods=['POST'])
@login_required
@admin_required
def update_user_role(user_id):
    new_role = request.form['role']
    if new_role in ['admin', 'client']:
        User.update_role(user_id, new_role)
        flash('User role updated successfully', 'success')
    else:
        flash('Invalid role specified', 'error')
    return redirect(url_for('admin.manage_users'))

@bp.route('/users/<user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash('Cannot delete your own account', 'error')
    else:
        User.delete(user_id)
        flash('User deleted successfully', 'success')
    return redirect(url_for('admin.manage_users'))

@bp.route('/api/stats')
@login_required
@admin_required
def api_stats():
    books = Book.get_all()
    users = User.get_all()
    
    # Genre distribution
    genres = {}
    for book in books:
        genre = book.get('genre', 'Unknown')
        genres[genre] = genres.get(genre, 0) + 1
    
    # User role distribution
    roles = {'admin': 0, 'client': 0}
    for user in users:
        roles[user.role] = roles.get(user.role, 0) + 1
    
    return jsonify({
        'total_books': len(books),
        'total_users': len(users),
        'genres': genres,
        'user_roles': roles
    })

@bp.route('/profile')
@login_required
@admin_required
def profile():
    return render_template('admin_profile.html')

@bp.route('/profile/update', methods=['POST'])
@login_required
@admin_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    
    # Check if username already exists (excluding current user)
    if username and username != current_user.username:
        existing_user = User.get_by_username(username)
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('admin.profile'))
    
    current_user.update_profile(username, email)
    flash('Profile updated successfully', 'success')
    return redirect(url_for('admin.profile'))

@bp.route('/profile/change-password', methods=['POST'])
@login_required
@admin_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not current_user.check_password(current_password):
        flash('Current password is incorrect', 'error')
        return redirect(url_for('admin.profile'))
    
    if new_password != confirm_password:
        flash('New passwords do not match', 'error')
        return redirect(url_for('admin.profile'))
    
    if len(new_password) < 6:
        flash('Password must be at least 6 characters long', 'error')
        return redirect(url_for('admin.profile'))
    
    current_user.update_password(new_password)
    flash('Password changed successfully', 'success')
    return redirect(url_for('admin.profile'))