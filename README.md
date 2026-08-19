# Restaurant DRF API

A learning backend project for managing restaurants, menu categories, and menu
items through a REST API. The project is built with Django REST Framework,
stores data in PostgreSQL, uses token authentication for protected operations,
and includes automated API tests.

## Features

- CRUD endpoints for restaurants, categories, and menu items
- Public read access
- Token-protected create, update, and delete operations
- Foreign-key validation for related objects
- Positive-price validation for menu items
- PostgreSQL persistence
- Automated tests for CRUD, validation, permissions, and token authentication
- Interactive Swagger UI and an OpenAPI schema

## Tech stack

- Python 3.12
- Django 6.1
- Django REST Framework 3.18
- drf-spectacular 0.30
- PostgreSQL 18
- Psycopg 3
- python-dotenv

## Data model

Each model has its own automatically generated `id` primary key.

- `Restaurant`: `name`, `city`
- `Category`: `name`, `restaurant`
- `MenuItem`: `name`, `price`, `category`

Relationships:

```text
Restaurant 1 ─── * Category 1 ─── * MenuItem
```

A category belongs to one restaurant, and a menu item belongs to one category.
Deleting a restaurant also deletes its categories and their menu items. Deleting
a category also deletes its menu items.

## API endpoints

The local base URL is `http://127.0.0.1:8000`.

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/restaurants/` | Public | List restaurants |
| `POST` | `/restaurants/` | Token required | Create a restaurant |
| `GET` | `/restaurants/<id>/` | Public | Retrieve a restaurant |
| `PUT` | `/restaurants/<id>/` | Token required | Fully update a restaurant |
| `PATCH` | `/restaurants/<id>/` | Token required | Partially update a restaurant |
| `DELETE` | `/restaurants/<id>/` | Token required | Delete a restaurant |
| `GET` | `/categories/` | Public | List categories |
| `POST` | `/categories/` | Token required | Create a category |
| `GET` | `/categories/<id>/` | Public | Retrieve a category |
| `PUT` | `/categories/<id>/` | Token required | Fully update a category |
| `PATCH` | `/categories/<id>/` | Token required | Partially update a category |
| `DELETE` | `/categories/<id>/` | Token required | Delete a category |
| `GET` | `/menu-items/` | Public | List menu items |
| `POST` | `/menu-items/` | Token required | Create a menu item |
| `GET` | `/menu-items/<id>/` | Public | Retrieve a menu item |
| `PUT` | `/menu-items/<id>/` | Token required | Fully update a menu item |
| `PATCH` | `/menu-items/<id>/` | Token required | Partially update a menu item |
| `DELETE` | `/menu-items/<id>/` | Token required | Delete a menu item |
| `POST` | `/api/token/` | Public | Exchange credentials for a token |
| `GET` | `/admin/` | Staff only | Open the Django admin site |

## API documentation

After starting the development server, open:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

Swagger UI lists all available endpoints and request fields. To try a protected
request, click **Authorize** and enter the token in this format:

```text
Token your-token-key
```

## Request data

Create a restaurant:

```json
{
  "name": "Dodo Pizza",
  "city": "Astana"
}
```

Create a category using an existing restaurant ID:

```json
{
  "name": "Pizza",
  "restaurant": 1
}
```

Create a menu item using an existing category ID:

```json
{
  "name": "Pepperoni",
  "price": 2500,
  "category": 1
}
```

`price` must be an integer greater than zero. Category responses also include
the read-only `restaurant_name` field, and menu-item responses include the
read-only `category_name` field.

## Authentication

Create a user locally before requesting a token:

```console
python manage.py createsuperuser
```

Send the username and password to the token endpoint:

```http
POST /api/token/
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

A successful response contains a token:

```json
{
  "token": "your-token-key"
}
```

Include it in every protected request:

```http
Authorization: Token your-token-key
```

Do not commit usernames, passwords, or tokens to the repository.

## Local setup

### 1. Clone the repository

```console
git clone https://github.com/arsenrinatuly/restaurant-drf.git
cd restaurant-drf
```

### 2. Create and activate a virtual environment

```console
python -m venv env
```

Windows CMD:

```console
env\Scripts\activate
```

Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

macOS or Linux:

```console
source env/bin/activate
```

### 3. Install dependencies

```console
python -m pip install -r requirements.txt
```

### 4. Create a PostgreSQL database

Open `psql` as a PostgreSQL administrator and run:

```sql
CREATE USER restaurant_user WITH PASSWORD 'choose-a-secure-password';
CREATE DATABASE restaurant_db OWNER restaurant_user;
```

The Django test runner creates a temporary database. For local development,
grant this role permission to create it:

```sql
ALTER ROLE restaurant_user CREATEDB;
```

Production application roles should not normally keep the `CREATEDB`
privilege.

### 5. Configure environment variables

Copy `.env.example` to `.env`, then replace the placeholder values:

```env
DJANGO_SECRET_KEY=replace-with-a-local-secret-key
DB_NAME=restaurant_db
DB_USER=restaurant_user
DB_PASSWORD=replace-with-your-database-password
DB_HOST=localhost
DB_PORT=5432
```

The `.env` file is ignored by Git and must never be committed.

### 6. Apply migrations

```console
python manage.py migrate
```

### 7. Start the development server

```console
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## Tests

Run the complete test suite:

```console
python manage.py test restaurants
```

The tests cover public and protected requests, valid and invalid creation,
detail retrieval, full and partial updates, deletion, missing resources, price
validation, token issuance, and using a real token on a protected endpoint.

The configured PostgreSQL user needs the local `CREATEDB` privilege because
Django creates and destroys a separate test database for each test run.

## Project structure

```text
config/                 Django project settings and root URLs
restaurants/            Models, serializers, views, URLs, migrations, and tests
.env.example            Environment variable template
manage.py               Django management entry point
requirements.txt        Pinned Python dependencies
```
