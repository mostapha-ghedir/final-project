# 📚 Book Library Application - Technical Overview

## 🏗️ **Architecture & Design Pattern**

### **Application Structure (MVC-ish Pattern)**
```
Flask App (Factory Pattern)
├── Models (Data Layer) - MongoDB ODM
├── Routes (Controllers) - Blueprint-based routing
├── Templates (Views) - Jinja2 templating
└── Static Assets - CSS/JS/Images
```

### **Core Components:**

**1. Application Factory (`app/__init__.py`)**
- Uses **Factory Pattern** to create Flask app instances
- Initializes extensions (PyMongo, Flask-Login)
- Registers blueprints (modular routing)
- Health check endpoint for monitoring
- MongoDB connection validation on startup

**2. Authentication & Authorization**
- **Flask-Login** for session management
- **Werkzeug** for password hashing (bcrypt)
- **Role-based access control (RBAC):**
  - `super_admin` → Full system access
  - `admin` → Manage books & clients
  - `client` → View books, manage favorites

**3. Database Layer (MongoDB)**
- **NoSQL document store** for flexibility
- **Collections:**
  - `users` → Authentication & roles
  - `books` → Library catalog
  - User favorites stored as arrays in user documents

**4. Blueprint Architecture (Modular Routing)**
```python
/auth     → Login, Register, Logout
/admin    → User management, Dashboard, Profile
/client   → Client dashboard, Favorites, Profile
/books    → CRUD operations, Search
/favorites → Add/Remove favorites
```

---

## 🐳 **Docker Architecture**

### **Multi-Container Setup (docker-compose.yml)**

```
┌─────────────────────────────────────┐
│   Host Machine (Port 5001)          │
└──────────────┬──────────────────────┘
               │
    ┌──────────▼──────────┐
    │  Docker Network     │
    │  (app-network)      │
    └──────────┬──────────┘
               │
       ┌───────┴────────┐
       │                │
   ┌───▼────┐      ┌───▼────┐
   │  web   │◄────►│ mongo  │
   │ Flask  │      │MongoDB │
   │ :5000  │      │ :27017 │
   └────────┘      └────────┘
```

### **Dockerfile Breakdown (Multi-Stage Build)**

**Stage 1: Base Image**
```dockerfile
FROM python:3.11-slim
```
- Minimal Python image (~150MB vs 1GB full image)
- Security: Fewer attack surfaces

**Stage 2: Dependencies**
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
- Layer caching optimization
- Rebuilds only if requirements change

**Stage 3: Application Code**
```dockerfile
COPY run.py .
COPY app ./app
```
- Separate layer for code changes
- Faster rebuilds during development

**Stage 4: Security Hardening**
```dockerfile
RUN adduser --disabled-password appuser
USER appuser
```
- **Non-root user** prevents privilege escalation
- Container runs with minimal permissions

**Stage 5: Runtime**
```dockerfile
CMD ["python", "run.py"]
```
- Direct Python execution (not gunicorn in dev)
- Port 5000 internally, mapped to 5001 externally

### **Docker Networking**
- **Bridge network** (`app-network`) isolates containers
- Service discovery: Flask connects to `mongodb://mongo:27017`
- DNS resolution: Docker resolves `mongo` hostname automatically

### **Volume Persistence**
```yaml
volumes:
  - mongo_data:/data/db  # MongoDB data persists across restarts
  - ./app/static/uploads:/app/app/static/uploads  # File uploads
```

### **Container Communication Flow**
```
1. docker-compose up
   ↓
2. Creates app-network bridge
   ↓
3. Starts mongo container (waits for health check)
   ↓
4. Starts web container (depends_on: mongo)
   ↓
5. Flask app connects to mongodb://mongo:27017
   ↓
6. Docker DNS resolves 'mongo' to container IP
   ↓
7. Health check: GET /health → {"status": "healthy"}
```

---

## 🔄 **CI/CD Pipeline (GitHub Actions)**

### **Pipeline Stages (Sequential)**

```
Push/PR → Lint → Security → Test → Docker Build → Docker Scan → Integration Test
```

### **Stage Breakdown:**

**1. Linting (Code Quality)**
```yaml
- flake8 .  # PEP 8 compliance
```
- Catches syntax errors, style violations
- Fails fast if code doesn't meet standards
- Enforces consistent code style across team

**2. Security Scanning**
```yaml
- pip-audit    # Dependency vulnerabilities (CVEs)
- bandit -r app  # SAST (SQL injection, XSS, etc.)
```
- **pip-audit**: Checks for known vulnerabilities in packages
  - Scans requirements.txt against CVE database
  - Fails if critical vulnerabilities found
- **bandit**: Static analysis for security issues in code
  - Detects hardcoded passwords
  - Identifies SQL injection risks
  - Checks for insecure cryptography

**3. Testing**
```yaml
services:
  mongodb:
    image: mongo:7.0
    ports: [27017:27017]
```
- Spins up **MongoDB service container**
- Runs pytest with real database
- Tests authentication, CRUD operations, role permissions
- Validates business logic

**4. Docker Build**
```yaml
- docker build -t library-app .
```
- Validates Dockerfile syntax
- Ensures image builds successfully
- Tests layer caching efficiency

**5. Docker Security Scan (Trivy)**
```yaml
- trivy image library-app
```
- Scans for OS vulnerabilities
- Checks Python package CVEs
- Fails if critical vulnerabilities found
- Generates vulnerability report

**6. Integration Test (Docker Compose)**
```yaml
- docker compose up -d
- sleep 10  # Wait for services
- docker compose ps  # Verify running
```
- Tests full stack deployment
- Validates container networking
- Ensures MongoDB connectivity
- Simulates production environment

### **CI/CD Flow Logic:**
```yaml
needs: [lint, security]  # Test runs only if lint & security pass
needs: test              # Docker build only if tests pass
needs: docker-build      # Scan only if build succeeds
```
- **Fail-fast**: Stops pipeline on first failure
- **Dependency chain**: Each stage depends on previous success
- **Parallel execution**: Lint and security run simultaneously
- **Resource optimization**: Caches Python dependencies

### **Branch Strategy**
```
main                 → Production-ready code
backend-core         → Core backend features
api-routes           → API endpoint development
frontend-templates   → UI/UX development
```
- CI runs on all branches
- Only main branch triggers deployment (if configured)

---

## 🔐 **Security Implementation**

### **1. Authentication**
- Passwords hashed with **bcrypt** (cost factor 12)
- Session-based auth with **Flask-Login**
- CSRF protection via Flask forms
- Secure session cookies (httponly, secure flags)

### **2. Authorization (Decorator Pattern)**
```python
@admin_required
def delete_user():
    if target_user.is_admin() and not current_user.is_super_admin():
        flash('Only super admin can delete admins')
```
- **Decorator-based access control**
- Role hierarchy enforcement
- Prevents privilege escalation

### **3. Input Validation**
- **Werkzeug secure_filename()** for file uploads
- File extension whitelist (`.png`, `.jpg`, `.jpeg`, `.gif`)
- MongoDB ObjectId validation
- Form data sanitization

### **4. Docker Security**
- Non-root user in container
- Minimal base image (slim)
- No hardcoded secrets (environment variables)
- Read-only filesystem where possible
- Security scanning in CI/CD

### **5. Database Security**
- MongoDB connection string in environment variables
- No default credentials
- Network isolation via Docker networks

---

## 📊 **Data Flow Examples**

### **User Registration Flow**
```
1. User submits registration form
   ↓
2. POST /auth/register
   ↓
3. Validate input (username unique, password match)
   ↓
4. Hash password with bcrypt
   ↓
5. MongoDB: db.users.insert_one({username, email, password_hash, role})
   ↓
6. Flask-Login: login_user(user)
   ↓
7. Redirect based on role (admin → dashboard, client → client dashboard)
```

### **Book Search Flow**
```
1. User enters search query
   ↓
2. GET /books?search=python
   ↓
3. Book.search(query) → MongoDB regex search
   ↓
4. db.books.find({$or: [{title: /python/i}, {author: /python/i}]})
   ↓
5. Render book_list.html with results
   ↓
6. Display books with favorite status (if authenticated)
```

### **Delete User Flow (with Super Admin Check)**
```
1. Admin clicks delete button
   ↓
2. JavaScript shows custom modal (no Bootstrap backdrop)
   ↓
3. User confirms → POST /admin/users/{id}/delete
   ↓
4. @admin_required decorator checks authentication
   ↓
5. Check if user_id == current_user.id (prevent self-delete)
   ↓
6. Get target_user from MongoDB
   ↓
7. Check if target_user.is_admin() AND NOT current_user.is_super_admin()
   ↓
8. If check fails → Flash error, redirect
   ↓
9. MongoDB: db.users.delete_one({'_id': ObjectId(id)})
   ↓
10. Flash success message → Redirect to manage_users
   ↓
11. Template renders updated user list
```

### **File Upload Flow**
```
1. Admin uploads book cover image
   ↓
2. POST /books/add with multipart/form-data
   ↓
3. Validate file extension (.png, .jpg, .jpeg, .gif)
   ↓
4. secure_filename() sanitizes filename
   ↓
5. Save to app/static/uploads/
   ↓
6. Store filename in MongoDB book document
   ↓
7. Render book detail with image URL
```

---

## 🚀 **Deployment Flow**

### **Local Development:**
```bash
# Start services
docker-compose up --build

# Access application
http://localhost:5001

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### **Production (Hypothetical):**
```bash
# Build versioned image
docker build -t library-app:v1.0 .

# Push to container registry
docker push registry/library-app:v1.0

# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml

# Or deploy to AWS ECS
aws ecs update-service --cluster prod --service library-app --force-new-deployment
```

---

## 🔧 **Key Technical Decisions**

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| **MongoDB** | Flexible schema for book metadata, easy horizontal scaling | No ACID transactions (not needed for this use case) |
| **Flask Blueprints** | Modular code, team can work on separate routes | Slight overhead vs monolithic routing |
| **Docker Compose** | Simple multi-container orchestration for dev/test | Not suitable for production at scale |
| **Non-root container** | Security best practice, limits blast radius | Requires proper file permissions setup |
| **Custom modal** | Avoid Bootstrap z-index conflicts, better UX control | More code to maintain vs Bootstrap modal |
| **Super admin role** | Prevents accidental admin deletion, clear hierarchy | Adds complexity to authorization logic |
| **Session-based auth** | Simple, works well with server-side rendering | Not suitable for mobile apps (use JWT instead) |
| **Bcrypt hashing** | Industry standard, resistant to rainbow tables | Slower than SHA256 (intentional for security) |

---

## 🐛 **Common Issues & Solutions**

### **Issue 1: Flask not accessible from host**
**Symptom:** `curl localhost:5001` fails, but Flask logs show "Running on http://127.0.0.1:5000"

**Root Cause:** Binding to `127.0.0.1` (localhost only) inside container

**Fix:**
```python
app.run(host='0.0.0.0', port=5000)
```
- `0.0.0.0` binds to all network interfaces
- Allows external connections from host machine

---

### **Issue 2: MongoDB connection refused**
**Symptom:** `pymongo.errors.ServerSelectionTimeoutError`

**Root Cause:** Containers not on same network

**Fix:**
```yaml
networks:
  - app-network

networks:
  app-network:
    driver: bridge
```
- Explicit network ensures DNS resolution
- Flask can resolve `mongo` hostname

---

### **Issue 3: Modal backdrop blocks buttons**
**Symptom:** Black overlay prevents clicking modal buttons

**Root Cause:** Bootstrap z-index stacking context

**Fix:**
```css
.modal-backdrop {
    display: none !important;
}
```
- Custom modal with controlled z-index
- Avoids Bootstrap's automatic backdrop

---

### **Issue 4: File uploads fail in Docker**
**Symptom:** `PermissionError: [Errno 13] Permission denied`

**Root Cause:** Non-root user can't write to uploads directory

**Fix:**
```dockerfile
RUN mkdir -p app/static/uploads && \
    chown -R appuser:appuser app/static/uploads
```
- Create directory before switching to non-root user
- Set proper ownership

---

### **Issue 5: CI/CD fails on docker-compose test**
**Symptom:** `docker compose: command not found`

**Root Cause:** Old Docker Compose v1 vs v2 syntax

**Fix:**
```yaml
- name: Install Docker Compose Plugin
  run: sudo apt-get install -y docker-compose-plugin
```
- Use `docker compose` (v2) instead of `docker-compose` (v1)

---

## 📈 **Performance Considerations**

### **Database Indexing**
```javascript
// Recommended indexes for MongoDB
db.users.createIndex({ username: 1 }, { unique: true })
db.users.createIndex({ email: 1 })
db.books.createIndex({ title: "text", author: "text" })  // Full-text search
db.books.createIndex({ genre: 1 })
```

### **Docker Layer Caching**
```dockerfile
# ✅ Good: Dependencies change less frequently
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app ./app

# ❌ Bad: Invalidates cache on every code change
COPY . .
RUN pip install -r requirements.txt
```

### **Flask Session Management**
- Sessions stored server-side (default)
- Consider Redis for production (horizontal scaling)

---

## 🧪 **Testing Strategy**

### **Unit Tests**
```python
# Test user model
def test_user_creation():
    user = User.create('test', 'test@example.com', 'password123')
    assert user.username == 'test'
    assert user.check_password('password123')
```

### **Integration Tests**
```python
# Test authentication flow
def test_login_flow(client):
    response = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 302  # Redirect
    assert '/admin/dashboard' in response.location
```

### **End-to-End Tests (Docker Compose)**
```bash
# Start services
docker-compose up -d

# Wait for health check
curl http://localhost:5001/health

# Run E2E tests
pytest tests/e2e/

# Cleanup
docker-compose down
```

---

## 🔮 **Future Enhancements**

### **Scalability**
- Add Redis for session storage
- Implement MongoDB replica set
- Use Nginx as reverse proxy
- Add load balancer for multiple Flask instances

### **Features**
- Book recommendations (ML-based)
- User reviews and ratings
- Email notifications
- API endpoints (REST/GraphQL)
- Mobile app (React Native + JWT auth)

### **DevOps**
- Kubernetes deployment
- Prometheus + Grafana monitoring
- ELK stack for logging
- Automated backups
- Blue-green deployments

---

## 📚 **Technology Stack Summary**

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Flask 2.3.3 | Web framework |
| **Database** | MongoDB 7.0 | NoSQL document store |
| **Auth** | Flask-Login 0.6.3 | Session management |
| **Password** | Bcrypt 4.0.1 | Password hashing |
| **Frontend** | Jinja2 + Bootstrap 5 | Server-side rendering |
| **Containerization** | Docker + Docker Compose | Application packaging |
| **CI/CD** | GitHub Actions | Automated testing & deployment |
| **Security** | Bandit, Trivy, pip-audit | Vulnerability scanning |
| **Testing** | Pytest | Unit & integration tests |

---

## 🎯 **Quick Reference Commands**

### **Development**
```bash
# Run locally (without Docker)
python run.py

# Run with Docker
docker-compose up --build

# View logs
docker-compose logs -f web

# Access MongoDB shell
docker exec -it <mongo-container-id> mongosh

# Create super admin
python init_admin.py
```

### **Testing**
```bash
# Run all tests
pytest -vv

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/
```

### **Docker**
```bash
# Build image
docker build -t library-app .

# Run container
docker run -p 5001:5000 -e MONGO_URI=mongodb://host.docker.internal:27017/book_library library-app

# Clean up
docker system prune -a
```

---

## 📞 **Support & Troubleshooting**

### **Health Check Endpoint**
```bash
curl http://localhost:5001/health
# Response: {"status": "healthy", "database": "connected"}
```

### **Debug Mode**
```python
# run.py
app.run(host='0.0.0.0', port=5001, debug=True)
```
- Enables auto-reload on code changes
- Shows detailed error pages
- **Never use in production!**

### **Logs**
```bash
# Flask logs
docker-compose logs web

# MongoDB logs
docker-compose logs mongo

# Follow logs in real-time
docker-compose logs -f
```

---

**Last Updated:** 2024
**Version:** 1.0
**Maintainers:** Development Team
