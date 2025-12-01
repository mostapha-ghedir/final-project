# Book Library

A simple Flask web application for managing a book library using MongoDB and Jinja2 templates.

## Features
- View a list of books
- View book details
- Add new books
- Edit existing books
- Delete books
- Search books by title or author

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up MongoDB (local or cloud).
3. Update `.env` with your MongoDB URI.
4. Run: `python run.py`

## Project Structure
- `app/`: Flask application
- `models/`: Data models
- `routes/`: URL routes
- `templates/`: Jinja2 HTML templates
- `static/`: CSS and JS files