# Project Structure

```
restaurant_project/
│
├── restaurant/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py            # Django settings (security, database, apps)
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration for deployment
│
├── core/                      # Main application
│   ├── migrations/            # Database migrations
│   ├── __init__.py
│   ├── admin.py              # Admin panel configuration
│   ├── apps.py               # App configuration
│   ├── forms.py              # Forms (Order, Booking, Review, Contact)
│   ├── models.py             # Database models
│   ├── urls.py               # App URL patterns
│   └── views.py              # View functions
│
├── templates/                 # HTML templates
│   ├── base.html             # Base template with navigation
│   └── core/
│       ├── home.html         # Homepage
│       ├── menu.html         # Menu page
│       ├── order.html        # Online ordering
│       ├── booking.html      # Table booking
│       ├── reviews.html      # Customer reviews
│       └── contact.html      # Contact page
│
├── static/                    # Static files
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   ├── js/
│   │   └── main.js           # JavaScript functionality
│   └── images/               # Image assets
│
├── media/                     # User uploads (created automatically)
│   └── menu_items/           # Menu item images
│
├── staticfiles/              # Collected static files (production)
│
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment configuration (Heroku/Render)
├── runtime.txt              # Python version specification
├── setup.sh                 # Quick setup script (Linux/Mac)
├── setup.bat                # Quick setup script (Windows)
├── README.md                # Project documentation
├── DEPLOYMENT.md            # Deployment guide
└── PROJECT_STRUCTURE.md     # This file
```

## Key Files Explained

### Configuration Files

**settings.py**
- Django settings
- Database configuration
- Security settings (CSRF, XSS protection)
- Static/Media file handling
- Email configuration

**urls.py**
- URL routing
- Admin panel URL
- App URL includes

**wsgi.py**
- WSGI application entry point
- Production server interface

### Application Files

**models.py**
Contains all database models:
- `Category` - Menu categories
- `MenuItem` - Menu items with prices, images
- `Order` - Customer orders
- `OrderItem` - Individual items in orders
- `TableBooking` - Table reservations
- `Review` - Customer reviews
- `ContactMessage` - Contact form submissions
- `RestaurantInfo` - Restaurant details (singleton)

**views.py**
View functions for all pages:
- `home()` - Homepage with featured items
- `menu()` - Full menu display
- `order_online()` - Online ordering page
- `create_order()` - AJAX order creation
- `table_booking()` - Booking form
- `reviews()` - Reviews page
- `contact()` - Contact form

**forms.py**
Django forms with validation:
- `OrderForm` - Online order form
- `TableBookingForm` - Reservation form with date/time validation
- `ReviewForm` - Review submission
- `ContactForm` - Contact message form

**admin.py**
Admin panel customization:
- Custom list displays
- Filters and search
- Inline editing
- Image previews
- Status management

### Template Files

**base.html**
- Master template
- Navigation bar
- Footer
- Floating action buttons
- Message display

**Page Templates**
- `home.html` - Hero section, featured items, reviews
- `menu.html` - Categorized menu display
- `order.html` - Shopping cart, checkout
- `booking.html` - Reservation form
- `reviews.html` - Review list and submission
- `contact.html` - Contact form, map, info

### Static Files

**style.css**
- Modern design system with CSS variables
- Responsive grid layouts
- Custom animations
- Mobile-first approach
- Sophisticated color palette

**main.js**
- Mobile menu toggle
- Smooth scrolling
- Form validation
- Alert/message handling
- Scroll animations

## Database Schema

### Tables

1. **Category**
   - id, name, description, order, created_at

2. **MenuItem**
   - id, category_id, name, description, price, image
   - is_available, is_vegetarian, is_vegan, is_gluten_free
   - spice_level, preparation_time
   - created_at, updated_at

3. **Order**
   - id, customer_name, customer_email, customer_phone
   - customer_address, status, total_amount, notes
   - created_at, updated_at

4. **OrderItem**
   - id, order_id, menu_item_id, quantity, price, notes

5. **TableBooking**
   - id, customer_name, customer_email, customer_phone
   - number_of_guests, booking_date, booking_time
   - status, special_requests
   - created_at, updated_at

6. **Review**
   - id, customer_name, customer_email, rating
   - review_text, is_approved, created_at

7. **ContactMessage**
   - id, name, email, phone, subject, message
   - is_read, created_at

8. **RestaurantInfo** (Singleton)
   - id, name, tagline, description
   - phone, email, address, whatsapp_number
   - google_maps_link, social media URLs
   - opening_hours
   - created_at, updated_at

## URL Structure

```
/                           → Home page
/menu/                      → Menu page
/order/                     → Online ordering
/order/create/              → Create order (AJAX)
/booking/                   → Table booking
/reviews/                   → Reviews page
/contact/                   → Contact page
/admin/                     → Admin panel (customizable URL)
/api/menu-item/<id>/       → Get menu item details (AJAX)
```

## Admin Panel Features

### Dashboard Sections
- Categories management
- Menu items (with image preview)
- Orders (status updates)
- Table bookings (approve/reject)
- Reviews (approve/reject)
- Contact messages (mark as read)
- Restaurant information

### Permissions
- Only superusers can access admin panel
- Staff users can have limited permissions
- Custom permissions per model

## Security Features

1. **CSRF Protection** - All forms protected
2. **XSS Protection** - Input sanitization
3. **SQL Injection Prevention** - Django ORM
4. **Secure Headers** - Production settings
5. **HTTPS Enforcement** - SSL/TLS required
6. **Password Hashing** - PBKDF2 algorithm
7. **Secure Cookies** - HTTPOnly, Secure flags
8. **Input Validation** - Form validation
9. **Custom Admin URL** - Security through obscurity
10. **Rate Limiting** - Can be added with middleware

## Deployment Platforms Supported

1. **Render** - Recommended for beginners
2. **Railway** - Easiest deployment
3. **DigitalOcean** - Full control
4. **PythonAnywhere** - Beginner-friendly
5. **Heroku** - Traditional choice
6. **AWS/GCP/Azure** - Enterprise scale

## Environment Variables

Required for production:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (False in production)
- `ALLOWED_HOSTS` - Comma-separated domains
- `DATABASE_URL` - PostgreSQL connection string
- `EMAIL_HOST` - SMTP server
- `EMAIL_HOST_USER` - Email username
- `EMAIL_HOST_PASSWORD` - Email password
- `ADMIN_URL` - Custom admin URL

## Feature Checklist

✅ Responsive design (mobile, tablet, desktop)
✅ Dynamic menu from database
✅ Online ordering with cart
✅ Table booking system
✅ Customer reviews with moderation
✅ Contact form
✅ Admin panel
✅ WhatsApp integration
✅ Google Maps integration
✅ Email notifications (configurable)
✅ Image uploads
✅ Form validation
✅ CSRF protection
✅ Production-ready
✅ Deployment guides
✅ Documentation

## Future Enhancements

Possible additions:
- Payment gateway integration
- Multi-language support
- Email confirmation for orders/bookings
- SMS notifications
- Loyalty program
- Online payment
- Inventory management
- Analytics dashboard
- Mobile app (Django REST API)
- Real-time order tracking
