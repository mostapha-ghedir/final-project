from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user
from app.models.book import Book
import os
from werkzeug.utils import secure_filename

bp = Blueprint('books', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/books')
def book_list():
    search_query = request.args.get('search', '')
    genre_filter = request.args.get('genre', '')
    
    if search_query:
        books = Book.search(search_query)
    else:
        books = Book.get_all()
    
    # Filter by genre if specified
    if genre_filter:
        books = [book for book in books if book.get('genre', '').lower() == genre_filter.lower()]
    
    return render_template('book_list.html', books=books)

@bp.route('/books/<book_id>')
def book_detail(book_id):
    book = Book.get_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('books.book_list'))
    
    is_favorite = False
    if current_user.is_authenticated:
        is_favorite = current_user.is_favorite(book_id)
    
    return render_template('book_detail.html', book=book, is_favorite=is_favorite)

@bp.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        image_filename = None
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            if file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))
        
        data = {
            'title': request.form['title'],
            'author': request.form['author'],
            'genre': request.form['genre'],
            'year': int(request.form['year']),
            'description': request.form['description'],
            'image': image_filename
        }
        Book.create(data)
        flash('Book added successfully', 'success')
        return redirect(url_for('books.book_list'))
    return render_template('add_edit_book.html', book=None, action='Add')

@bp.route('/books/<book_id>/edit', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.get_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('books.book_list'))
    if request.method == 'POST':
        image_filename = book.get('image')
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            if file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))
        
        data = {
            'title': request.form['title'],
            'author': request.form['author'],
            'genre': request.form['genre'],
            'year': int(request.form['year']),
            'description': request.form['description'],
            'image': image_filename
        }
        Book.update(book_id, data)
        flash('Book updated successfully', 'success')
        return redirect(url_for('books.book_detail', book_id=book_id))
    return render_template('add_edit_book.html', book=book, action='Edit')

@bp.route('/books/<book_id>/delete', methods=['POST'])
def delete_book(book_id):
    Book.delete(book_id)
    flash('Book deleted successfully', 'success')
    return redirect(url_for('books.book_list'))

@bp.route('/search', methods=['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        query = request.form['query']
        books = Book.search(query)
        return render_template('search.html', books=books, query=query)
    return render_template('search.html', books=None, query='')