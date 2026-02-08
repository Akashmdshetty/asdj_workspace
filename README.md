# SaaS Collaboration Platform

A real-time collaboration SaaS platform built with Django, Channels, and React.

## Project Structure

- `backend/`: Django project root.
- `frontend/`: React application (planned).
- `docker/`: Docker configuration.

## Setup

### Prerequisites
- Python 3.10+
- Redis (for Channels and Celery)

### Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r backend/requirements/base.txt
   ```

3. Configure environment:
   - Copy `.env.example` to `.env` (or create one based on `backend/config/settings/base.py`).

4. Run migrations:
   ```bash
   python backend/manage.py migrate
   ```

5. Run the server:
   ```bash
   python backend/manage.py runserver
   ```
