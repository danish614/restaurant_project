# 🚀 Quick Start Guide

Get your restaurant website running in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- Git (optional, for version control)

## Option 1: Automated Setup (Recommended)

### For Linux/Mac:
```bash
cd restaurant_project
chmod +x setup.sh
./setup.sh
```

### For Windows:
```batch
cd restaurant_project
setup.bat
```

The script will:
1. Create virtual environment
2. Install dependencies
3. Setup database
4. Create superuser
5. Collect static files

## Option 2: Manual Setup

### Step 1: Create Virtual Environment
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings (optional for development)
```

### Step 4: Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Step 5: Run Server
```bash
python manage.py runserver
```

## Access Your Website

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## First Steps After Login

### 1. Add Restaurant Information
- Login to admin panel
- Go to "Restaurant Information"
- Fill in your details (name, address, phone, etc.)

### 2. Create Menu Categories
- Go to "Categories"
- Add categories (e.g., "Appetizers", "Main Course", "Desserts")

### 3. Add Menu Items
- Go to "Menu Items"
- Add items with:
  - Name, description, price
  - Category
  - Image (optional)
  - Dietary options

### 4. Test the Features
- Visit homepage to see featured items
- Browse menu
- Try online ordering
- Submit a test booking
- Leave a review
- Send a contact message

## Common Commands

```bash
# Run development server
python manage.py runserver

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run Django shell
python manage.py shell
```

## Project Structure

```
restaurant_project/
├── core/              # Main app
├── restaurant/        # Project settings
├── templates/         # HTML files
├── static/           # CSS, JS, images
├── media/            # Uploaded files
└── manage.py         # Django commands
```

## Key URLs

| Page | URL |
|------|-----|
| Home | `/` |
| Menu | `/menu/` |
| Order Online | `/order/` |
| Book Table | `/booking/` |
| Reviews | `/reviews/` |
| Contact | `/contact/` |
| Admin | `/admin/` |

## Need Help?

1. Check `README.md` for detailed documentation
2. Check `DEPLOYMENT.md` for deployment guides
3. Check `PROJECT_STRUCTURE.md` for technical details

## Next Steps

1. ✅ Setup complete
2. 📝 Add restaurant information
3. 🍽️ Create menu
4. 🎨 Customize design (edit `static/css/style.css`)
5. 🚀 Deploy to production (see DEPLOYMENT.md)

## Troubleshooting

**Port already in use:**
```bash
python manage.py runserver 8080
```

**Static files not loading:**
```bash
python manage.py collectstatic --clear
```

**Database errors:**
```bash
python manage.py migrate --run-syncdb
```

**Permission denied (Linux/Mac):**
```bash
chmod +x manage.py
```

## Production Deployment

For production deployment, see `DEPLOYMENT.md` for:
- Render
- Railway
- DigitalOcean
- PythonAnywhere

## Support

This is a complete, production-ready Django application with:
- ✅ Responsive design
- ✅ Admin panel
- ✅ Online ordering
- ✅ Table booking
- ✅ Reviews system
- ✅ Contact form
- ✅ Security features
- ✅ Deployment ready

Happy building! 🎉
