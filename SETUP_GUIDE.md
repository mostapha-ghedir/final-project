# Book Library Setup Guide

## Quick Start with Authentication

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file:
```env
MONGO_URI=mongodb://localhost:27017/book_library
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=development
DEBUG=True
```

### 3. Start MongoDB
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Or use MongoDB Atlas (cloud)
# Update MONGO_URI in .env with your Atlas connection string
```

### 4. Initialize Admin User
```bash
python init_admin.py
```

### 5. Run the Application
```bash
python run.py
```

## User Roles and Access

### Admin Users
- **Login**: `admin` / `admin123` (change after first login)
- **Access**: Full system access
- **Features**:
  - Admin Dashboard with statistics
  - User management (create, edit, delete users)
  - Book management (add, edit, delete books)
  - View all system data

### Client Users
- **Registration**: Open registration available
- **Access**: Limited to browsing and viewing
- **Features**:
  - Client Dashboard with recent books
  - Browse books by genre
  - Search functionality
  - View book details
  - Personal profile management

## Application Structure

### Authentication System
- **Login/Register**: `/auth/login`, `/auth/register`
- **Session Management**: Flask-Login with secure sessions
- **Password Security**: Bcrypt hashing
- **Role-based Access**: Admin vs Client permissions

### Admin Panel (`/admin/`)
- **Dashboard**: `/admin/dashboard` - System overview and statistics
- **User Management**: `/admin/users` - Manage all users
- **Book Management**: `/admin/books` - Full book CRUD operations
- **API Endpoints**: `/admin/api/stats` - JSON statistics

### Client Interface (`/client/`)
- **Dashboard**: `/client/dashboard` - Personal library view
- **Browse Books**: `/client/books` - Browse with filters
- **Book Details**: `/client/books/<id>` - Individual book view
- **Profile**: `/client/profile` - User account management

### Public Routes
- **Home**: `/` - Landing page
- **Book List**: `/books` - Public book listing
- **Search**: `/search` - Public search functionality

## Docker Deployment

### Development
```bash
# Start all services
docker-compose up --build

# Initialize admin user (in container)
docker-compose exec web python init_admin.py
```

### Production
```bash
# Use production docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

## Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId,
  "username": String,
  "email": String,
  "password_hash": String,
  "role": String, // "admin" or "client"
  "is_active": Boolean
}
```

### Books Collection
```javascript
{
  "_id": ObjectId,
  "title": String,
  "author": String,
  "genre": String,
  "year": Number,
  "description": String,
  "image": String // filename
}
```

## Security Features

### Authentication
- Secure password hashing with bcrypt
- Session-based authentication
- Login required decorators
- Role-based access control

### Authorization
- Admin-only routes protected
- User role validation
- CSRF protection (Flask-WTF recommended for production)
- Input validation and sanitization

### Data Protection
- Environment variables for sensitive data
- Secure session cookies
- Password complexity (implement as needed)
- Rate limiting (implement for production)

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/logout` - User logout

### Admin API
- `GET /admin/api/stats` - System statistics (JSON)
- `POST /admin/users/<id>/role` - Update user role
- `POST /admin/users/<id>/delete` - Delete user

### Books API (existing)
- `GET /books` - List all books
- `POST /books/add` - Add new book (admin only)
- `GET /books/<id>` - Book details
- `POST /books/<id>/edit` - Edit book (admin only)
- `POST /books/<id>/delete` - Delete book (admin only)

## Development Workflow

### For Team Collaboration

1. **Backend Developer**: Focus on models, authentication, API endpoints
2. **Frontend Developer**: Work on templates, styling, user experience
3. **Admin Features**: Implement admin dashboard and management tools
4. **Client Features**: Build user-friendly browsing and search

### Testing Users

Create test users for development:
```python
# Admin user
python init_admin.py

# Test client user
# Register through /auth/register or create via admin panel
```

## Production Considerations

### Security Hardening
- Change default admin password
- Use strong SECRET_KEY
- Enable HTTPS
- Implement rate limiting
- Add CSRF protection
- Validate all inputs

### Performance
- Add database indexing
- Implement caching
- Optimize image uploads
- Add pagination for large datasets

### Monitoring
- Add logging
- Implement health checks
- Monitor user activity
- Track system performance

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Check MongoDB is running
   - Verify MONGO_URI in .env
   - Check network connectivity

2. **Admin User Not Created**
   - Run `python init_admin.py`
   - Check database connection
   - Verify no existing admin user

3. **Template Not Found**
   - Check template file paths
   - Verify blueprint registrations
   - Check route template references

4. **Permission Denied**
   - Verify user role in database
   - Check login status
   - Validate admin decorators

### Debug Mode
```bash
export FLASK_ENV=development
export DEBUG=True
python run.py
```

## Next Steps

1. **Customize Styling**: Update CSS in `app/static/css/style.css`
2. **Add Features**: Implement favorites, reviews, ratings
3. **Enhance Security**: Add 2FA, password reset, email verification
4. **Improve UX**: Add search filters, sorting, advanced pagination
5. **Add Analytics**: Track user behavior, popular books, usage statistics

---

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`
- **⚠️ Change immediately after first login!**