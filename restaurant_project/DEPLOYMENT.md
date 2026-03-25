# 🚀 Deployment Guide

Comprehensive guide for deploying the Restaurant Website to various platforms.

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Render Deployment](#render-deployment)
3. [Railway Deployment](#railway-deployment)
4. [DigitalOcean Deployment](#digitalocean-deployment)
5. [PythonAnywhere Deployment](#pythonanywhere-deployment)
6. [Custom Domain Setup](#custom-domain-setup)
7. [SSL Certificate Setup](#ssl-certificate-setup)
8. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All sensitive data in `.env` file (not in code)
- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` is strong and unique
- [ ] `ALLOWED_HOSTS` configured with your domain
- [ ] Database configured (PostgreSQL recommended)
- [ ] Static files configured with WhiteNoise
- [ ] requirements.txt is up to date
- [ ] All migrations are created and tested
- [ ] Admin account created
- [ ] Restaurant information added

---

## Render Deployment

### Step 1: Prepare Your Code

1. Ensure your code is in a Git repository (GitHub, GitLab, etc.)

2. Verify `requirements.txt`:
```txt
Django==4.2.7
Pillow==10.1.0
whitenoise==6.6.0
gunicorn==21.2.0
dj-database-url==2.1.0
psycopg2-binary==2.9.9
python-decouple==3.8
```

3. Verify `Procfile`:
```
web: gunicorn restaurant.wsgi --log-file -
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub/GitLab
3. Authorize Render to access your repositories

### Step 3: Create PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Configure:
   - Name: `restaurant-db`
   - Database: `restaurant`
   - User: `restaurant_user`
   - Region: Choose closest to your users
   - Instance Type: Free tier for testing
3. Click "Create Database"
4. **Copy the "Internal Database URL"** (you'll need this)

### Step 4: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure:
   - **Name**: `restaurant-website`
   - **Region**: Same as database
   - **Branch**: `main` or `master`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**:
     ```bash
     gunicorn restaurant.wsgi
     ```
   - **Instance Type**: Free tier for testing

### Step 5: Environment Variables

Add these in the "Environment" section:

```
SECRET_KEY=your-super-secret-key-change-this-to-something-random
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=<paste-the-internal-database-url-from-step-3>
ADMIN_URL=secure-admin-123/
```

To generate a secret key:
```python
import secrets
print(secrets.token_urlsafe(50))
```

### Step 6: Deploy

1. Click "Create Web Service"
2. Wait for build (5-10 minutes)
3. Monitor logs for any errors

### Step 7: Create Superuser

1. Go to your Render dashboard
2. Click on your web service
3. Go to "Shell" tab
4. Run:
   ```bash
   python manage.py createsuperuser
   ```

### Step 8: Access Your Site

- Frontend: `https://your-app-name.onrender.com`
- Admin: `https://your-app-name.onrender.com/secure-admin-123/`

---

## Railway Deployment

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway automatically detects Django

### Step 3: Add PostgreSQL

1. In your project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically creates and links it

### Step 4: Configure Environment

1. Go to your web service
2. Click "Variables"
3. Add:
   ```
   SECRET_KEY=<generate-random-key>
   DEBUG=False
   ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}}
   ADMIN_URL=secure-admin/
   ```

### Step 5: Configure Build

1. Go to "Settings"
2. Add Custom Start Command:
   ```
   python manage.py migrate && python manage.py collectstatic --noinput && gunicorn restaurant.wsgi
   ```

### Step 6: Deploy

Railway automatically deploys on push to main branch.

### Step 7: Generate Domain

1. Go to "Settings"
2. Click "Generate Domain"
3. Your site will be at `your-app.railway.app`

---

## DigitalOcean Deployment

### Step 1: Create Droplet

1. Log into DigitalOcean
2. Create Droplet:
   - Ubuntu 22.04 LTS
   - Basic plan ($6/month minimum)
   - Choose datacenter region
   - Add SSH key

### Step 2: Initial Server Setup

SSH into your droplet:
```bash
ssh root@your-droplet-ip
```

Update system:
```bash
apt update && apt upgrade -y
```

Install dependencies:
```bash
apt install python3-pip python3-venv nginx postgresql postgresql-contrib git -y
```

### Step 3: Configure PostgreSQL

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE restaurant_db;
CREATE USER restaurant_user WITH PASSWORD 'strong-password-here';
ALTER ROLE restaurant_user SET client_encoding TO 'utf8';
ALTER ROLE restaurant_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE restaurant_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO restaurant_user;
\q
```

### Step 4: Clone Project

```bash
cd /var/www
git clone https://github.com/yourusername/restaurant-project.git
cd restaurant-project
```

### Step 5: Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 6: Configure Environment

```bash
cp .env.example .env
nano .env
```

Edit:
```
SECRET_KEY=<generate-unique-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-droplet-ip
DATABASE_URL=postgresql://restaurant_user:strong-password-here@localhost:5432/restaurant_db
```

### Step 7: Setup Django

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### Step 8: Configure Gunicorn

Create systemd service:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=gunicorn daemon for restaurant website
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/restaurant-project
Environment="PATH=/var/www/restaurant-project/venv/bin"
ExecStart=/var/www/restaurant-project/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/restaurant-project/restaurant.sock \
    restaurant.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

### Step 9: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/restaurant
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias /var/www/restaurant-project/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/restaurant-project/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/restaurant-project/restaurant.sock;
    }
}
```

Enable and test:
```bash
sudo ln -s /etc/nginx/sites-available/restaurant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 10: Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Follow prompts and choose to redirect HTTP to HTTPS.

---

## PythonAnywhere Deployment

### Step 1: Create Account

1. Go to https://www.pythonanywhere.com
2. Create account (free tier available)

### Step 2: Upload Code

Option A - Git:
```bash
cd ~
git clone https://github.com/yourusername/restaurant-project.git
```

Option B - Upload via Files tab

### Step 3: Create Virtual Environment

Go to Bash console:
```bash
mkvirtualenv --python=/usr/bin/python3.10 restaurant-env
cd restaurant-project
pip install -r requirements.txt
```

### Step 4: Setup Database

For free tier (SQLite):
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

For paid tier (MySQL):
1. Create MySQL database in Databases tab
2. Update DATABASE_URL in .env

### Step 5: Configure Web App

1. Go to Web tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Python 3.10

Configure:
- **Source code**: `/home/username/restaurant-project`
- **Working directory**: `/home/username/restaurant-project`
- **Virtualenv**: `/home/username/.virtualenvs/restaurant-env`

### Step 6: Edit WSGI File

Click "WSGI configuration file" link and replace content:

```python
import os
import sys

path = '/home/username/restaurant-project'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'restaurant.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 7: Configure Static Files

In Web tab, add:
- URL: `/static/`
- Directory: `/home/username/restaurant-project/staticfiles`

- URL: `/media/`
- Directory: `/home/username/restaurant-project/media`

### Step 8: Reload

Click "Reload" button in Web tab.

---

## Custom Domain Setup

### For Render:
1. Go to your service → Settings
2. Click "Add Custom Domain"
3. Add your domain
4. Update DNS records at your domain provider:
   - Type: CNAME
   - Name: www (or @)
   - Value: provided by Render

### For Railway:
1. Go to Settings → Domains
2. Click "Add Domain"
3. Update DNS:
   - Type: CNAME
   - Name: www
   - Value: provided by Railway

### For DigitalOcean:
1. Point your domain's A record to droplet IP
2. Update `ALLOWED_HOSTS` in settings
3. Run certbot again with new domain

---

## SSL Certificate Setup

### Automatic (Render/Railway)
SSL is automatic - just use custom domain.

### Manual (DigitalOcean)
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Auto-renewal:
```bash
sudo certbot renew --dry-run
```

---

## Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

Verify `STATIC_ROOT` and `STATICFILES_STORAGE` in settings.

### Database Connection Error
- Check `DATABASE_URL` format
- Verify database credentials
- Ensure database service is running

### 500 Internal Server Error
- Check logs: `heroku logs --tail` or server logs
- Verify `DEBUG=False` and `ALLOWED_HOSTS`
- Check migrations: `python manage.py migrate`

### Admin CSS Not Loading
- Run `collectstatic`
- Check WhiteNoise configuration
- Verify `STATIC_URL` and `STATIC_ROOT`

### Port Already in Use
```bash
# Kill process on port
sudo lsof -t -i:8000 | xargs kill -9
```

### Permission Denied Errors
```bash
# DigitalOcean
sudo chown -R www-data:www-data /var/www/restaurant-project
sudo chmod -R 755 /var/www/restaurant-project
```

---

## Monitoring & Maintenance

### Regular Tasks:
- Monitor error logs
- Backup database regularly
- Update dependencies monthly
- Check disk space
- Monitor performance
- Review security updates

### Backup Database:
```bash
# PostgreSQL
pg_dump restaurant_db > backup_$(date +%Y%m%d).sql

# Django
python manage.py dumpdata > backup.json
```

---

**Need Help?** Check Django deployment docs or platform-specific documentation.
