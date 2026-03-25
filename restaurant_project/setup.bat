@echo off
REM Quick Setup Script for Restaurant Website (Windows)
REM This script sets up the development environment

echo ==============================================
echo    Restaurant Website - Quick Setup
echo ==============================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env file with your configuration
    echo.
)

REM Create necessary directories
echo Creating directories...
if not exist media mkdir media
if not exist staticfiles mkdir staticfiles
echo.

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput
echo.

REM Create superuser
echo ==============================================
echo    Create Superuser Account
echo ==============================================
python manage.py createsuperuser
echo.

echo ==============================================
echo    Setup Complete!
echo ==============================================
echo.
echo Next steps:
echo 1. Edit .env file with your settings
echo 2. Run: python manage.py runserver
echo 3. Visit: http://127.0.0.1:8000
echo 4. Admin: http://127.0.0.1:8000/admin/
echo.
echo Happy coding!
echo.
pause
