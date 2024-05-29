# Vendor Management System

## Overview
A Django and Django REST Framework based Vendor Management System that handles vendor profiles, tracks purchase orders, and calculates vendor performance metrics.

## Features
- Vendor Profile Management
- Purchase Order Tracking
- Vendor Performance Evaluation

## Requirements
- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+

## Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/bhosalemayuri812/vendor-management-system.git
    cd vendor-management-system
    ```

2. **Apply migrations**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Create a superuser**
    ```sh
    python manage.py createsuperuser
    ```

4. **Run the development server**
    ```sh
    python manage.py runserver
    ```

## API Endpoints

### Vendor Endpoints
- **Create a new vendor**: `POST /api/vendors/`
- **List all vendors**: `GET /api/vendors/`
- **Retrieve a specific vendor**: `GET /api/vendors/{vendor_id}/`
- **Update a vendor's details**: `PUT /api/vendors/{vendor_id}/`
- **Delete a vendor**: `DELETE /api/vendors/{vendor_id}/`

### Purchase Order Endpoints
- **Create a purchase order**: `POST /api/purchase_orders/`
- **List all purchase orders**: `GET /api/purchase_orders/`
- **Retrieve a specific purchase order**: `GET /api/purchase_orders/{po_id}/`
- **Update a purchase order**: `PUT /api/purchase_orders/{po_id}/`
- **Delete a purchase order**: `DELETE /api/purchase_orders/{po_id}/`

### Vendor Performance Endpoint
- **Retrieve a vendor's performance metrics**: `GET /api/vendors/{vendor_id}/performance`

## Running Tests
To run the test suite:
```sh
python manage.py test
