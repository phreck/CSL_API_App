# CSL API Application 🌐🔍

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)](https://www.django-rest-framework.org/)

A modern Django application for interacting with the U.S. Government's Consolidated Screening List (CSL) API. This application provides both a RESTful API and an intuitive web interface for searching and managing CSL data.

## 📋 Overview

The Consolidated Screening List (CSL) is a collection of parties for which the United States Government maintains restrictions on certain exports, reexports, or transfers of items. This application enables users to:

- Search entities in the CSL database with advanced filtering
- Query the live CSL API from trade.gov in real-time
- Store and cache results in a local PostgreSQL database
- View detailed information about restricted entities
- Access data programmatically via a comprehensive REST API
- Browse entities through a user-friendly web interface

## 🏗️ Project Structure

The application follows a clean separation of concerns with the following components:

- `api/` - Django REST Framework API for accessing CSL data
- `core/` - Core business logic and services for interacting with the external CSL API
- `web/` - Web frontend with user interface templates
- `csl_api_project/` - Django project configuration

## ✅ Requirements

- Python 3.12+
- PostgreSQL (or Docker for containerized setup)
- Redis (optional, for caching)
- UV for dependency management

## 🚀 Installation

### Option 1: Local Development Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/CSL_API_App.git
cd CSL_API_App
```

2. **Install dependencies using UV**

```bash
pip install uv
uv pip install -e .
```

For development dependencies:
```bash
uv pip install -e ".[dev]"
```

3. **Configure environment variables**

Create a `.env` file in the project root based on the provided `example.env`:

```
# Django settings
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
USE_SQLITE=False
DB_NAME=csl_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# CSL API settings
CSL_API_URL=https://data.trade.gov/consolidated_screening_list/v1/search
CSL_SUBSCRIPTION_KEY=your_subscription_key_here

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

4. **Set up the PostgreSQL database**

```bash
createdb csl_db
```

5. **Apply migrations**

```bash
python manage.py migrate
```

6. **Create a superuser**

```bash
python manage.py createsuperuser
```

7. **Run the development server**

```bash
python manage.py runserver
```

The application will be available at http://localhost:8000/

### Option 2: Docker Setup

For a containerized setup using Docker:

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/CSL_API_App.git
cd CSL_API_App
```

2. **Start the PostgreSQL container**

```bash
docker-compose -f csl_postgres_dev_docker-compose.yml up -d
```

3. **Configure environment variables**

Create a `.env` file as above, but set:
```
DB_HOST=postgres
DB_PASSWORD=postgres
```

4. **Install dependencies, run migrations and start the application**

```bash
pip install uv
uv pip install -e .
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | None (Required) |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `USE_SQLITE` | Use SQLite instead of PostgreSQL | `False` |
| `DB_NAME` | Database name | `csl_db` |
| `DB_USER` | Database username | `postgres` |
| `DB_PASSWORD` | Database password | None (Required) |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `CSL_API_URL` | CSL API URL | `https://data.trade.gov/consolidated_screening_list/v1/search` |
| `CSL_SUBSCRIPTION_KEY` | CSL API subscription key | None (Required) |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000,http://localhost:8000` |

## 📊 Data Models

The application uses the following core models:

- **ScreeningEntity**: Main model representing entities from the CSL
- **Address**: Stores addresses associated with screening entities
- **EntityID**: Stores identification documents associated with entities
- **SearchQuery**: Logs search queries made to the application

## 🔍 Usage

### Web Interface

The web interface provides the following pages:

- **Home**: `/` - Landing page with search form and statistics
- **Search**: `/search/` - Advanced search with filters
- **Entity Detail**: `/entity/{id}/` - Detailed information about an entity
- **About**: `/about/` - Information about the application and the CSL

### API Endpoints

The application provides the following REST API endpoints:

#### Entity Endpoints

- `GET /api/v1/entities/` - List all entities (paginated)
- `GET /api/v1/entities/{id}/` - Retrieve a specific entity
- `GET /api/v1/entities/search/` - Search entities in the local database
- `GET /api/v1/entities/external_search/` - Search entities using the external CSL API
- `GET /api/v1/entities/source_lists/` - Get all source lists

#### Address Endpoints

- `GET /api/v1/addresses/` - List all addresses
- `GET /api/v1/addresses/countries/` - Get all countries

#### Search History Endpoints

- `GET /api/v1/search-history/` - View search history

For complete API documentation, visit http://localhost:8000/api/v1/ when the server is running.

### API Examples

**Search for entities containing "smith":**
```bash
curl -X GET "http://localhost:8000/api/v1/entities/search/?q=smith"
```

**Filter entities by country:**
```bash
curl -X GET "http://localhost:8000/api/v1/entities/search/?country=IR"
```

**Search external CSL API:**
```bash
curl -X GET "http://localhost:8000/api/v1/entities/external_search/?q=smith"
```

## 🧪 Testing

Run tests using pytest:

```bash
pytest
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

Project Link: [https://github.com/yourusername/CSL_API_App](https://github.com/yourusername/CSL_API_App)