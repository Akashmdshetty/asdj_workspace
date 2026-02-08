#!/usr/bin/env bash
set -o errexit

# Build frontend
cd frontend
npm install
npm run build
cd ..

# Install backend dependencies
pip install -r requirements.txt

# Collect static files (including frontend build)
python backend/manage.py collectstatic --noinput

# Run migrations
python backend/manage.py migrate
