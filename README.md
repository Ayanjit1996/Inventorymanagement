# Inventory Management System

## Overview
It is a web-based application designed to manage products, suppliers, stock movements, and sales orders. It enables users to track inventory levels, monitor sales performance, and streamline inventory operations efficiently.

---

## Features
- **Product Management**: Add, update, and view product details.
- **Supplier Management**: Manage supplier information.
- **Stock Movement**: Record stock additions and reductions.
- **Sales Order Management**: Create and track sales orders with status updates.
- **Sorting Functionality**: Sort sales orders by category or status directly from the interface.
- **User-Friendly Interface**: Responsive design with styled tables and buttons for easy navigation.

---

## Technologies Used

### Backend
- **Python**
- **Django**
- **MongoDB**

### Frontend
- **HTML5 & CSS3**
- **JavaScript**

### Others
- **Bootstrap**
- **Virtual Environment**

---

## Installation and Setup

### Prerequisites
- Python 3.10+
- Virtual environment tool (`venv`)
- Django (latest stable version)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Ayanjit1996/Inventorymanagement.git
   cd Inventorymanagement
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application in your browser:
   ```
   http://127.0.0.1:8000/
   ```

---

## Key Functionalities

### 1. Product Management
- **Fields**: Name, Description, Category, Price, Stock Quantity, Supplier.
- **Features**: CRUD operations to manage product inventory.

### 2. Supplier Management
- **Fields**: Name, Email, Phone, Address.
- **Features**: CRUD operations for suppliers.

### 3. Stock Movement
- **Fields**: Product, Quantity, Movement Type (IN/OUT), Date.
- **Features**: Record stock adjustments and update inventory levels.

### 4. Sales Order Management
- **Fields**: Product, Quantity, Total Amount, Sale Date, Notes, Status (PENDING/COMPLETED/CANCELLED).
- **Features**: Create and update sales orders with automatic total amount calculation.

### 5. Sorting
- **Fields**: Sort by Category and Status.
- **Features**: Interactive sorting buttons using JavaScript for seamless UX.

---
