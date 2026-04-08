# AutomationPro — Industrial E-Commerce Platform

A full-featured Django e-commerce web application for selling industrial automation equipment and scheduling professional maintenance services.

## Features

- **Product Catalog** — Category-based browsing, search, filters (price, brand, condition)
- **User Authentication** — Registration, login, profile management
- **Shopping Cart** — Session-based cart for guests, persistent cart for logged-in users
- **Order Management** — Checkout, order history, order detail view
- **Maintenance Services** — Service type catalog, service request submission, maintenance scheduling
- **REST API** — Full API for products, orders, and service requests (DRF)
- **Admin Dashboard** — Django admin for products, orders, services
- **Responsive UI** — Bootstrap 5 with custom CSS

## Project Structure

```
├── automation_ecommerce/     # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── catalog/              # Products and categories
│   ├── accounts/             # User authentication & profiles
│   ├── cart/                 # Shopping cart
│   ├── orders/               # Order management & checkout
│   ├── services/             # Maintenance scheduling
│   └── api/                  # REST API endpoints
├── templates/                # HTML templates (Bootstrap 5)
├── static/                   # CSS, JavaScript
├── manage.py
├── requirements.txt
└── .env.example
```

## Requirements

- Python 3.10+
- MariaDB / MySQL 8.0+
- pip

## Setup

### 1. Clone and create virtual environment

```bash
git clone <repo-url>
cd Automation-ecommerce
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `mysqlclient` requires system libraries. On Ubuntu/Debian:
> ```bash
> sudo apt-get install libmariadb-dev
> ```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your values:

```
SECRET_KEY=your-very-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=automation_ecommerce
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 4. Create the database

```sql
CREATE DATABASE automation_ecommerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Collect static files (production)

```bash
python manage.py collectstatic
```

### 8. Start the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000

## URLs

| Path | Description |
|------|-------------|
| `/` | Home page |
| `/products/` | Product catalog |
| `/products/<slug>/` | Product detail |
| `/accounts/register/` | User registration |
| `/accounts/login/` | Login |
| `/accounts/profile/` | User profile |
| `/cart/` | Shopping cart |
| `/orders/checkout/` | Checkout |
| `/orders/` | Order history |
| `/services/` | Service types |
| `/services/request/` | Submit service request |
| `/services/my-requests/` | My service requests |
| `/services/maintenance/` | Maintenance schedules |
| `/api/` | REST API root |
| `/admin/` | Admin dashboard |

## REST API Endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/categories/` | GET | List categories |
| `/api/products/` | GET | List products (search, ordering) |
| `/api/products/<slug>/` | GET | Product detail |
| `/api/products/featured/` | GET | Featured products |
| `/api/orders/` | GET | User's orders (auth required) |
| `/api/service-types/` | GET | Service type catalog |
| `/api/service-requests/` | GET, POST | User's service requests (auth required) |

## Technology Stack

- **Backend:** Django 4.2, Django REST Framework 3.15
- **Database:** MariaDB / MySQL (via mysqlclient)
- **Frontend:** Bootstrap 5 (CDN), Bootstrap Icons, Custom CSS/JS
- **Forms:** django-crispy-forms + crispy-bootstrap5
- **Config:** django-environ
- **Images:** Pillow
