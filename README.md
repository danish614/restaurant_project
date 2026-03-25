# Restaurant Website - Production-Ready Django Application

A complete, modern, and responsive restaurant website built with Django, featuring online ordering, table booking, reviews, and admin management.

## 🌟 Features

### Frontend
- **Modern, Responsive Design**: Mobile-first approach with beautiful UI/UX
- **6 Main Pages**: Home, Menu, Online Order, Table Booking, Reviews, Contact
- **Interactive Elements**:
  - Shopping cart with live updates
  - Floating WhatsApp & Call buttons
  - Smooth animations and transitions
  - Google Maps integration
- **Accessibility**: Semantic HTML, ARIA labels, keyboard navigation

### Backend (Django)
- **User Management**: Secure authentication system
- **Dynamic Menu**: Category-based menu with dietary filters
- **Order System**: Complete online ordering with cart management
- **Booking System**: Table reservation with validation
- **Review System**: Customer reviews with admin approval
- **Contact Form**: Message handling with email notifications

### Admin Panel
- **Dashboard**: Overview of orders, bookings, and messages
- **Menu Management**: Add/edit/delete items and categories
- **Order Management**: View and update order status
- **Booking Management**: Approve/reject table reservations
- **Review Moderation**: Approve customer reviews
- **Settings**: Update restaurant information

### Security Features
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure password hashing
- Input validation and sanitization
- HTTPS enforcement (production)
- Secure headers and cookies

## 📋 Requirements

- Python 3.11+
- PostgreSQL (recommended for production) or SQLite (development)
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone the Project

```bash
git clone https://github.com/danish614/restaurant_project.git
cd restaurant_project/restaurant_project
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
SECRET_KEY=your-unique-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

### 8. Access Admin Panel

Visit: http://127.0.0.1:8000/admin/

Login with your superuser credentials.

## 🛠️ Tech Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL / SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Fonts**: Playfair Display, Karla (Google Fonts)
- **Icons**: Font Awesome 6
- **Deployment**: Gunicorn, WhiteNoise, Nginx

## 🌐 Deployment

Deployment guides available for:
- **Render** (Recommended for beginners)
- **Railway** (Easiest)
- **DigitalOcean**
- **PythonAnywhere**
- **Heroku**
- **AWS / GCP / Azure**

See [DEPLOYMENT.md](restaurant_project/DEPLOYMENT.md) for detailed instructions.

## 📝 License

This project is open source and available for personal and commercial use.

---

**Built with ❤️ using Django and Modern Web Technologies**
