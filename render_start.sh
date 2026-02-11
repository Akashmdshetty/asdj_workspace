#!/usr/bin/env bash
set -o errexit

echo "Running migrations..."
python backend/manage.py migrate

echo "Starting Daphne..."
daphne -b 0.0.0.0 -p $PORT config.asgi:application
