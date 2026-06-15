# Beauty Salon

Beauty Salon is a Django-based beauty salon booking and service catalog application. It provides a user-facing service catalog, shopping cart, appointment checkout, user accounts, and Stripe test-mode payment integration.

## Project Overview

- Django 5.2 project with a custom `User` model for email-based authentication.
- `main` app manages procedures, categories, specialists, discounts, and public site pages.
- `cart` app stores selected procedures in a session-backed cart.
- `users` app handles registration, login, profile editing, and appointment history.
- `appointments` app creates appointment records, saves appointment items, and uses Stripe Checkout for payments.

## Features

- Home page and artists page.
- Service catalog with filtering by category, discount, specialist, and price range.
- Procedure detail pages with associated specialists and pricing.
- Cart add/remove/update flows with procedure quantity and specialist selection.
- Appointment creation for logged-in users.
- Stripe Checkout integration for payment sessions.
- PostgreSQL database configuration by default.
- Media uploads for procedure and specialist images.

## Requirements

- Python 3.x
- Django 5.2
- PostgreSQL
- `python-dotenv`
- `stripe`
- `psycopg2-binary`

## Setup

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install required packages:

```powershell
pip install django python-dotenv stripe psycopg2-binary
```

3. Create a `.env` file at the repository root with the following values:

```text
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=db01
STRIPE_TEST_PUBLIC_KEY=your_stripe_test_public_key
STRIPE_TEST_SECRET_KEY=your_stripe_test_secret_key
```

4. Apply database migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:

```powershell
python manage.py createsuperuser
```

6. Start the development server:

```powershell
python manage.py runserver
```

## Local URLs

- `/` — home page
- `/artists/` — artists page
- `/services/` — service catalog
- `/procedure/<slug>/` — procedure detail
- `/cart/` — cart overview
- `/users/register/` — user registration
- `/users/login/` — user login
- `/users/profile/` — profile and appointments
- `/appointments/create/` — appointment checkout

## Notes

- The project uses `AUTH_USER_MODEL = 'users.User'`.
- `ecom/settings.py` configures PostgreSQL by default. For a simple local setup, replace the `DATABASES` block with SQLite settings.
- Media files are stored under `media/` and served in development when `DEBUG=True`.
- Stripe payment links currently use `http://localhost:8000/appointments/completed` and `http://localhost:8000/appointments/create`.

## Project Structure

- `main/` — procedures, categories, specialists, discounts, catalog and detail views.
- `cart/` — shopping cart logic and cart-related views.
- `users/` — custom user model, authentication, registration, and profile.
- `appointments/` — appointment forms, models, Stripe checkout, success/failure templates.
- `ecom/` — Django project settings, URLs, WSGI/ASGI configuration.

## Further Improvements

- Add tests for cart, user auth, discounts, and appointment checkout.
- Add proper Stripe webhook handling for payment confirmations.
- Improve error handling for invalid cart items and Stripe failures.
- Add admin configuration for procedure images and service management.
