from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.book import Book

bp = Blueprint('client', __name__, url_prefix='/client')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's favorite books or recent activity
    recent_books = Book.get_all()[:6]  # Show 6 recent books
    return render_template('client_dashboard.html', books=recent_books)

@bp.route('/books')
@login_required
def browse_books():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    genre_filter = request.args.get('genre', '')
    
    if search_query:
        books = Book.search(search_query)
    else:
        books = Book.get_all()
    
    # Filter by genre if specified
    if genre_filter:
        books = [book for book in books if book.get('genre', '').lower() == genre_filter.lower()]
    
    # Get unique genres for filter dropdown
    all_books = Book.get_all()
    genres = list(set(book.get('genre', '') for book in all_books if book.get('genre')))
    genres.sort()
    
    return render_template('book_list.html', 
                         books=books, 
                         genres=genres,
                         current_search=search_query,
                         current_genre=genre_filter)

@bp.route('/books/<book_id>')
@login_required
def book_detail(book_id):
    book = Book.get_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('client.browse_books'))
    return render_template('book_detail.html', book=book, is_favorite=current_user.is_favorite(book_id) if current_user.is_authenticated else False)

@bp.route('/profile')
@login_required
def profile():
    return render_template('client_profile.html', user=current_user)

@bp.route('/favorites')
@login_required
def favorites():
    favorite_ids = current_user.get_favorites()
    favorite_books = []
    
    for book_id in favorite_ids:
        book = Book.get_by_id(book_id)
        if book:
            favorite_books.append(book)
    
    return render_template('client_favorites.html', books=favorite_books)