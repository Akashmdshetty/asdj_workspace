#!/usr/bin/env bash
set -o errexit

echo "Build script started"
pwd
ls -la

# Build frontend
echo "Building frontend..."
cd frontend
npm install
npm run build
echo "Frontend build complete."
echo "Checking dist folder:"
ls -la dist || echo "dist folder NOT FOUND in frontend"
cd ..

# Install backend dependencies
echo "Installing backend deps..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python backend/manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python backend/manage.py migrate

echo "Build script finished"
