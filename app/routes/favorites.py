from flask import Blueprint, request, redirect, url_for, flash, jsonify, render_template
from flask_login import login_required, current_user
from app.models.book import Book

bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@bp.route('/add/<book_id>', methods=['POST'])
@login_required
def add_favorite(book_id):
    book = Book.get_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('client.browse_books'))
    
    current_user.add_favorite(book_id)
    flash(f'"{book["title"]}" added to favorites!', 'success')
    return redirect(request.referrer or url_for('client.book_detail', book_id=book_id))

@bp.route('/remove/<book_id>', methods=['POST'])
@login_required
def remove_favorite(book_id):
    book = Book.get_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('client.browse_books'))
    
    current_user.remove_favorite(book_id)
    flash(f'"{book["title"]}" removed from favorites!', 'info')
    return redirect(request.referrer or url_for('client.book_detail', book_id=book_id))

@bp.route('/toggle/<book_id>', methods=['POST'])
@login_required
def toggle_favorite(book_id):
    book = Book.get_by_id(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    is_favorite = current_user.is_favorite(book_id)
    
    if is_favorite:
        current_user.remove_favorite(book_id)
        message = f'"{book["title"]}" removed from favorites'
        action = 'removed'
    else:
        current_user.add_favorite(book_id)
        message = f'"{book["title"]}" added to favorites'
        action = 'added'
    
    return jsonify({
        'success': True,
        'message': message,
        'action': action,
        'is_favorite': not is_favorite
    })

@bp.route('/list')
@login_required
def list_favorites():
    favorite_ids = current_user.get_favorites()
    favorite_books = []
    
    for book_id in favorite_ids:
        book = Book.get_by_id(book_id)
        if book:
            favorite_books.append(book)
    
    return render_template('favorites_list.html', books=favorite_books)