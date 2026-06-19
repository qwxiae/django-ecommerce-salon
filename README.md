🌍 Languages: [🇬🇧 English](README.md) | [🇷🇺 Русский](README.ru.md)

# Beauty Salon (Mini E-Commerce Project)

Application for booking appointments at a beauty salon and browsing a
service catalog, developed with Django. It provides a service catalog
for users, a shopping cart, appointment booking for procedures, user
accounts, and integration with the Stripe payment system in test mode.

## Project Overview

-   Django 5.2 project with a custom `User` model for email-based
    authentication.
-   The `main` application manages procedures, categories, specialists,
    discounts, and public website pages.
-   The `cart` application stores selected procedures in a session-based
    shopping cart.
-   The `users` application handles registration, login, profile editing,
    and appointment history.
-   The `appointments` application creates appointments, stores selected
    services, and uses Stripe Checkout for payment processing.

## Features

-   Home page and specialists page.
-   Service catalog with filtering by categories, discounts,
    specialists, and price range.
-   Detailed procedure pages with assigned specialists and pricing.
-   Add, remove, and update services in the cart with procedure quantity
    and specialist selection.
-   Appointment booking for authenticated users.
-   Stripe Checkout integration for creating payment sessions.
-   PostgreSQL database configuration by default.
-   Uploading images for procedures and specialists.

## Requirements

-   Python 3.x
-   Django 5.2
-   PostgreSQL
-   python-dotenv
-   stripe
-   psycopg2-binary

## Installation

1.  Create and activate a virtual environment:
```sh
    python -m venv .venv
    .\.venv\Scripts\Activate
```
2.  Install the required packages:
```sh
    pip install django python-dotenv stripe psycopg2-binary
```
3.  Create a .env file in the project root directory with the following
    values:
```
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=db01
    STRIPE_TEST_PUBLIC_KEY=your_stripe_test_public_key
    STRIPE_TEST_SECRET_KEY=your_stripe_test_secret_key
```
4.  Apply database migrations:
```sh
    python manage.py makemigrations
    python manage.py migrate
```
5.  Create a superuser:
```sh
    python manage.py createsuperuser
```
6.  Start the development server:
```sh
    python manage.py runserver
```
## Local URLs

-   `/` — home page
-   `/artists/` — specialists page
-   `/services/` — service catalog
-   `/procedure/<slug>/` — procedure page
-   `/cart/` — view cart
-   `/users/register/` — user registration
-   `/users/login/` — user login
-   `/users/profile/` — profile and appointment list
-   `/appointments/create/` — appointment booking

## Notes

-   The project uses `AUTH_USER_MODEL = 'users.User'`.
-   PostgreSQL is configured by default in `ecom/settings.py`. For simple
    local development, you can replace the `DATABASES` configuration with
    SQLite settings.
-   Media files are stored in the `media/` directory and served during
    development when `DEBUG=True`.
-   Stripe success and failure payment URLs currently use
    `http://localhost:8000/appointments/completed` and
    `http://localhost:8000/appointments/create`.

## Project Structure

-   `main/` — procedures, categories, specialists, discounts, catalog, and
    detail pages.
-   `cart/` — cart logic and related views.
-   `users/` — custom user model, authentication, registration, and
    profile.
-   `appointments/` — appointment forms and models, Stripe Checkout,
    successful and failed payment templates.
-   `ecom/` — Django project settings, URL routing, WSGI/ASGI
    configuration.

## Possible Improvements

-   Add tests for the cart, user authentication, discounts, and
    appointment booking.
-   Implement full Stripe Webhook handling for payment confirmation.
-   Improve error handling for invalid cart data and Stripe failures.
-   Add advanced admin panel customization for procedure images and
    service management.
