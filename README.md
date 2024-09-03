# Online Shopping application
This project demonstrates a Django REST Framework application connected to a PostgreSQL database. It features CRUD operations, Postman documentation for API exploration, and is prepared for deployment with Gunicorn.

## Table of Contents
- Prerequisites
- Installation
- Configuration
- Deployment

### Prerequisites
- Python 3.9+
- PostgreSQL

### Installation
Install the required packages with under command:
```
pip install -r requirements.txt
```

### Configuration
#### Manage environment variables:
Copy the .env.example file to create your own .env file:
```
cp .env_example .env

```
Edit the .env file to set up your database credentials and any other environment-specific variables.
#### Manage DB:
Apply migrations to set up the database schema:
```
python manage.py migrate
```
#### Manage staticfiles:
Run the under command to generate static files in `STATIC_ROOT` path
```
python manage.py collectstatic --noinput
```
#### Manage superuser:
Run the under command to create a new superuser for access to `Django-admin-panel`
```
python manage.py createsuperuser --username "admin" --email "admin@exmple.com"
```

### Deployment (gunicorn)
Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model, which means the master process forks multiple worker processes to handle requests. This section outlines how to configure and use Gunicorn with your Django project.
#### Configuration File
Gunicorn allows you to specify configurations via a configuration file. Create a `gunicorn.conf.py` file in your project root directory with the following content:
```
workers = 4  # Number of worker processes
threads_per_worker = 2  # Threads per worker
loglevel = 'info'  # Log level
bind = '0.0.0.0:8000'  # IP and port to bind to
```
#### Running Gunicorn
To start your Django application with Gunicorn, execute the following command in your terminal:
```
gunicorn configs.wsgi:application --config gunicorn.conf.py
```
