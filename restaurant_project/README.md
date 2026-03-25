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

### 1. Clone/Extract the Project

```bash
cd restaurant_project
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

Follow the prompts to create your admin account.

### 6. Create Static Files Directory

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

## 📊 Initial Data Setup

After logging into the admin panel:

1. **Restaurant Information**
   - Go to "Restaurant Information"
   - Add your restaurant details, contact info, hours, etc.

2. **Menu Categories**
   - Go to "Categories"
   - Add categories (e.g., Appetizers, Main Course, Desserts)

3. **Menu Items**
   - Go to "Menu Items"
   - Add items with images, prices, descriptions
   - Set dietary options (vegetarian, vegan, gluten-free)

## 🌐 Deployment

### Deploy to Render

1. **Create Render Account**: https://render.com

2. **Create PostgreSQL Database**:
   - New → PostgreSQL
   - Copy the "Internal Database URL"

3. **Create Web Service**:
   - New → Web Service
   - Connect your repository
   - Settings:
     - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
     - **Start Command**: `gunicorn restaurant.wsgi`
   
4. **Environment Variables**:
   ```
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app.onrender.com
   DATABASE_URL=<paste-internal-database-url>
   ```

5. **Deploy**: Click "Create Web Service"

### Deploy to Railway

1. **Create Railway Account**: https://railway.app

2. **New Project**:
   - Deploy from GitHub repo
   - Add PostgreSQL database (automatically configured)

3. **Environment Variables**:
   ```
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app
   ```

4. Railway automatically detects Django and deploys

### Deploy to DigitalOcean

1. **Create Droplet** (Ubuntu 22.04)

2. **SSH into server** and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Clone your project
git clone <your-repo-url>
cd restaurant_project

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure PostgreSQL
sudo -u postgres psql
CREATE DATABASE restaurant_db;
CREATE USER restaurant_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO restaurant_user;
\q

# Configure environment
cp .env.example .env
nano .env  # Edit with production values

# Run migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

# Setup Gunicorn
sudo nano /etc/systemd/system/gunicorn.service
```

Gunicorn service file:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/restaurant_project
ExecStart=/root/restaurant_project/venv/bin/gunicorn --workers 3 --bind unix:/root/restaurant_project/restaurant.sock restaurant.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Configure Nginx
sudo nano /etc/nginx/sites-available/restaurant
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /root/restaurant_project;
    }
    
    location /media/ {
        root /root/restaurant_project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/root/restaurant_project/restaurant.sock;
    }
}
```

```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/restaurant /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Deploy to PythonAnywhere

1. **Create PythonAnywhere Account**: https://www.pythonanywhere.com

2. **Upload Files**:
   - Upload project via Git or Files tab

3. **Setup Virtual Environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 restaurant-env
   pip install -r requirements.txt
   ```

4. **Configure Web App**:
   - Web tab → Add new web app
   - Manual configuration → Python 3.10
   - Set Source code directory
   - Set Virtual environment path
   - Configure WSGI file (edit to point to your wsgi.py)

5. **Static Files**:
   - URL: `/static/`
   - Directory: `/home/username/restaurant_project/staticfiles`

6. **Reload** your web app

## 🔒 Security Checklist (Production)

- [ ] Change `SECRET_KEY` to a unique value
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/SSL
- [ ] Change admin URL from default
- [ ] Set up email backend for contact forms
- [ ] Configure CORS if using API
- [ ] Regular backups of database
- [ ] Monitor error logs
- [ ] Keep dependencies updated

## 📱 Features Guide

### Online Ordering
1. Customers browse menu
2. Add items to cart
3. Fill delivery details
4. Submit order
5. Admin receives notification and manages order

### Table Booking
1. Customer selects date, time, guests
2. System validates availability
3. Booking submitted for approval
4. Admin confirms or rejects
5. Customer receives confirmation

### Reviews
1. Customer submits review with rating
2. Review pending admin approval
3. Admin approves/rejects
4. Approved reviews display on site

### Contact Form
1. Customer fills contact form
2. Message saved to database
3. Admin receives notification (if email configured)
4. Admin can mark as read/unread

## 🎨 Customization

### Colors & Branding
Edit `static/css/style.css` - CSS variables at the top:
```css
:root {
    --color-primary: #c9a962;
    --color-secondary: #2d3436;
    --color-accent: #e17055;
    /* ... */
}
```

### Restaurant Information
Update in Admin Panel → Restaurant Information

### Menu Categories & Items
Manage in Admin Panel → Categories & Menu Items

### Logo & Images
Place logo in `static/images/` and update templates

## 📞 Support Features

- **WhatsApp Integration**: Floating button for direct chat
- **Call Button**: One-click calling
- **Google Maps**: Embedded location map
- **Social Media**: Links to all platforms

## 🛠️ Tech Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL / SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Fonts**: Playfair Display, Karla (Google Fonts)
- **Icons**: Font Awesome 6
- **Deployment**: Gunicorn, WhiteNoise, Nginx

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

For support or queries, please use the contact form on the website or reach out via email.

---

**Built with ❤️ using Django and Modern Web Technologies**
