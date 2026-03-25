#!/bin/bash
# Quick Setup Script for Restaurant Website
# This script sets up the development environment

echo "🍽️  Restaurant Website - Quick Setup"
echo "===================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✓ Please edit .env file with your configuration"
fi

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p media
mkdir -p staticfiles

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo ""
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser
echo ""
echo "👤 Create superuser account"
echo "============================="
python manage.py createsuperuser

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your settings"
echo "2. Run: python manage.py runserver"
echo "3. Visit: http://127.0.0.1:8000"
echo "4. Admin: http://127.0.0.1:8000/admin/"
echo ""
echo "Happy coding! 🚀"
