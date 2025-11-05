# Django PostgreSQL Docker Template

A Django project template with Docker and PostgreSQL setup, created using django-admin startproject.

## Features

- Django 4.2.26 (created with django-admin startproject)
- PostgreSQL 15
- Docker & Docker Compose
- Whitenoise for static files
- Environment variables configuration with python-decouple
- Ready-to-use templates
- All Django code organized in `/app` directory

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

### 1. Clone and Configure Environment

```bash
# Copy environment variables
cp .env.example .env

# Edit .env file and update the SECRET_KEY and other settings as needed
```

### 2. Build and Run with Docker

```bash
# Build and start containers
docker-compose up --build

# The application will be available at http://localhost:8000
```

### 3. Run Migrations

```bash
# In a new terminal, run migrations
docker-compose exec web python manage.py migrate

# Create a superuser for admin access
docker-compose exec web python manage.py createsuperuser
```

## Common Commands

```bash
# Start containers
docker-compose up

# Start containers in detached mode
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f web

# Run Django commands
docker-compose exec web python manage.py <command>

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic

# Access Django shell
docker-compose exec web python manage.py shell

# Access PostgreSQL
docker-compose exec db psql -U django_user -d django_db
```

## Project Structure

```
.
├── app/                    # Django application directory
│   ├── config/            # Django configuration (created by startproject)
│   │   ├── __init__.py
│   │   ├── settings.py   # Django settings (configured for PostgreSQL)
│   │   ├── urls.py       # URL configuration
│   │   ├── wsgi.py       # WSGI configuration
│   │   └── asgi.py       # ASGI configuration
│   ├── templates/         # HTML templates
│   │   └── home.html
│   ├── static/            # Static files (CSS, JS, images)
│   └── manage.py          # Django management script
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Development

The project uses volume mounting, so any changes you make to the code will be reflected immediately without rebuilding the container.

## Admin Panel

Access the admin panel at http://localhost:8000/admin after creating a superuser.

## Environment Variables

Key environment variables (see `.env.example`):

- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port

## Creating New Django Apps

To create a new Django app within the project:

```bash
# Enter the Django container
docker-compose exec web bash

# Create a new app (this will create it in /code directory inside container)
python manage.py startapp myapp

# Exit the container
exit
```

The new app will be created in the `app/` directory. Remember to add it to `INSTALLED_APPS` in `app/config/settings.py`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp",  # Add your new app here
]
```

## Production Deployment

For production:

1. Set `DEBUG=False` in .env
2. Update `SECRET_KEY` with a secure random key
3. Configure `ALLOWED_HOSTS` properly
4. Use a production-grade WSGI server (gunicorn is included)
5. Set up proper static file serving
6. Configure database backups
7. Use environment-specific docker-compose files

## License

MIT
