# Smart Document Management System

A complete production-style Django web application for managing documents with role-based access control, department-based organization, and comprehensive permission management.

## Features

### User Management
- **Role-Based Access Control (RBAC)** with three roles:
  - Super Admin: Full system access
  - Department Admin: Department-level management
  - Employee: View and download authorized documents
- Custom User model with role and department fields
- Profile management with profile pictures
- Password change functionality

### Department Management
- Create, edit, and delete departments
- Track users and documents per department
- Department-based document organization

### Role Management
- Define custom roles with granular permissions
- Configure permissions for:
  - User management
  - Department management
  - Document management
  - System administration

### Document Management
- Upload documents (PDF, DOCX, XLSX, TXT)
- Document versioning with history tracking
- Soft delete with restore functionality
- File preview for PDF documents
- Advanced search and filtering
- Drag and drop upload support
- File validation (type and size)

### Permission System
- Role-based permissions
- Department-based permissions
- User-specific permissions
- Granular access control (view, download, edit, delete)

### Activity Logging
- Track all user actions
- Log login/logout events
- Document upload/download tracking
- Permission change logging
- IP address tracking

### REST API
- JWT authentication
- Complete CRUD operations for all entities
- Pagination, filtering, and search
- Secure endpoint access

## Technology Stack

### Backend
- Django 5+
- Django REST Framework
- SQLite (development) / PostgreSQL (production)
- Django Simple JWT

### Frontend
- Django Templates
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Authentication
- Django Authentication System
- Custom User Model
- JWT Tokens (API)

## Project Structure

```
smart_dms/
├── accounts/              # User management app
├── departments/          # Department management app
├── roles/                # Role management app
├── documents/            # Document management app
├── permissions_app/      # Permission management app
├── activity_logs/        # Activity logging app
├── api/                  # REST API app
├── templates/            # HTML templates
├── static/               # Static files (CSS, JS)
├── media/                # Uploaded files
├── smart_dms/            # Project settings
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── seed_data.py          # Database seeding script
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
cd c:\Users\NIKHITHA\OneDrive\Desktop\DjangoFrameworkSample
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables (Optional)
```bash
cp .env.example .env
```

Edit `.env` file with your configuration (optional for SQLite):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email configuration (optional, for password reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@smartdms.com
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Seed Database (Optional)
```bash
python seed_data.py
```

This will create sample departments, roles, users, and documents.

### Step 8: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Default Login Credentials (After Seeding)

| Role | Username | Password |
|------|----------|----------|
| Super Admin | admin | admin123 |
| HR Admin | hr_admin | hr123 |
| Finance Admin | finance_admin | finance123 |
| Engineer | engineer1 | engineer123 |

## Usage

### Super Admin
1. Login with super admin credentials
2. Access dashboard to view system statistics
3. Manage departments (Create/Edit/Delete)
4. Manage roles and permissions
5. Upload and manage documents
6. View activity logs
7. Access Django Admin panel at `/admin/`

### Department Admin
1. Login with department admin credentials
2. View department-specific dashboard
3. Upload documents for department
4. Manage department documents
5. View department activity logs
6. Cannot access other departments

### Employee
1. Login with employee credentials
2. View accessible documents
3. Search and filter documents
4. Download authorized documents
5. View document details
6. Cannot upload or delete documents

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List users
- `POST /api/users/` - Create user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Departments
- `GET /api/departments/` - List departments
- `POST /api/departments/` - Create department
- `GET /api/departments/{id}/` - Get department details
- `PUT /api/departments/{id}/` - Update department
- `DELETE /api/departments/{id}/` - Delete department

### Documents
- `GET /api/documents/` - List documents
- `POST /api/documents/` - Upload document
- `GET /api/documents/{id}/` - Get document details
- `PUT /api/documents/{id}/` - Update document
- `DELETE /api/documents/{id}/` - Delete document
- `POST /api/documents/{id}/download/` - Download document
- `POST /api/documents/{id}/restore/` - Restore document

### Permissions
- `GET /api/permissions/` - List permissions
- `POST /api/permissions/` - Create permission
- `GET /api/permissions/{id}/` - Get permission details
- `DELETE /api/permissions/{id}/` - Delete permission

### Activity Logs
- `GET /api/activity-logs/` - List activity logs

## Security Features

- CSRF protection
- File upload validation (type and size)
- Role-based route protection
- Secure media access
- Login required decorators
- Permission checks
- Input validation
- JWT authentication for API
- Password hashing

## File Upload Limits

- Maximum file size: 10MB
- Allowed file types: PDF, DOCX, XLSX, TXT

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Custom Management Commands
```bash
python manage.py startapp custom_app
```

### Accessing Django Admin
Navigate to `http://localhost:8000/admin/` and login with super admin credentials.

## Production Deployment

### Quick Deployment Commands

```bash
# 1. Clone the repository
git clone https://github.com/Nikhitha-spec/DocVault.git
cd DocVault

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your production settings

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Create superuser
python manage.py createsuperuser

# 8. Seed database (optional)
python seed_data.py
```

### Deployment Platforms

#### Option 1: PythonAnywhere (Recommended for Django)

```bash
# On PythonAnywhere dashboard:
# 1. Create a new web app
# 2. Choose "Manual Configuration" with Python 3.9+
# 3. Go to the virtual environment tab and run:
pip install -r requirements.txt

# 4. In the Files tab, upload your project
# 5. In the Web tab, set the working directory to your project folder
# 6. Set the WSGI configuration file to: smart_dms/wsgi.py
# 7. Add static files mapping: /static/ -> /path/to/staticfiles
# 8. Set environment variables in the Web tab
# 9. Reload the web app
```

**PythonAnywhere WSGI Configuration:**
```python
import os
import sys

path = '/home/yourusername/DocVault'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_dms.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### Option 2: Render.com

```bash
# Create a render.com account
# Create a new Web Service
# Connect your GitHub repository
# Build Command:
pip install -r requirements.txt
python manage.py collectstatic --noinput

# Start Command:
gunicorn smart_dms.wsgi:application

# Environment Variables (add in Render dashboard):
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=postgresql://...
```

**Create `render.yaml` in project root:**
```yaml
services:
  - type: web
    name: docvault
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput
    startCommand: gunicorn smart_dms.wsgi:application
    envVars:
      - key: DEBUG
        value: False
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: docvault-db
          property: connectionString
databases:
  - name: docvault-db
    databaseName: docvault
    user: docvault_user
```

#### Option 3: Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Heroku app
heroku create docvault

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set ALLOWED_HOSTS=docvault.herokuapp.com

# Push to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Seed database
heroku run python manage.py shell
# Then run: exec(open('seed_data.py').read())
```

**Create `Procfile` in project root:**
```
web: gunicorn smart_dms.wsgi:application
```

**Create `runtime.txt` in project root:**
```
python-3.9.16
```

### Settings to Update for Production

1. **Set DEBUG = False** in `smart_dms/settings.py`
2. **Update ALLOWED_HOSTS** with your domain:
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```
3. **Use strong SECRET_KEY** (generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
4. **Configure production database** (PostgreSQL recommended)
5. **Set up static file serving** (Whitenoise recommended)
   ```bash
   pip install whitenoise
   ```
   Add to `settings.py`:
   ```python
   MIDDLEWARE = [
       'whitenoise.middleware.WhiteNoiseMiddleware',
       # ... other middleware
   ]
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   ```
6. **Configure email backend** for password reset (optional)
7. **Enable HTTPS** (required for production)
8. **Set CSRF_COOKIE_SECURE = True**
9. **Set SESSION_COOKIE_SECURE = True**
10. **Set SECURE_SSL_REDIRECT = True**
11. **Set SECURE_HSTS_SECONDS = 31536000**

### Using Gunicorn (Production Server)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn smart_dms.wsgi:application

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:8000 smart_dms.wsgi:application

# Run with Gunicorn and systemd (Linux)
# Create /etc/systemd/system/docvault.service:
[Unit]
Description=DocVault Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/DocVault
ExecStart=/path/to/DocVault/venv/bin/gunicorn --workers 3 --bind unix:/path/to/DocVault/docvault.sock smart_dms.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx Configuration (Linux)

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /path/to/DocVault/staticfiles/;
    }

    location /media/ {
        alias /path/to/DocVault/media/;
    }

    location / {
        proxy_pass http://unix:/path/to/DocVault/docvault.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Database Setup for Production

**PostgreSQL:**
```bash
# Install PostgreSQL
# Create database
createdb docvault

# Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'docvault',
        'USER': 'docvault_user',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Install psycopg2-binary
pip install psycopg2-binary
```

### Static Files

```bash
# Collect static files for production
python manage.py collectstatic --noinput

# Use Whitenoise for static file serving
pip install whitenoise
```

### SSL/HTTPS Setup

**Using Let's Encrypt with Certbot:**
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
```

### Monitoring and Logging

```bash
# Enable Django logging in settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/path/to/DocVault/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

### Migration Issues
```bash
python manage.py makemigrations --empty
python manage.py migrate --fake-initial
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Permission Denied Errors
- Check user role and permissions
- Verify document permissions are set correctly
- Ensure user is assigned to correct department

## License

This project is for educational and demonstration purposes.

## Support

For issues and questions, please refer to the Django documentation:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Contributing

This is a sample project for demonstration purposes. Feel free to extend and modify as needed.
