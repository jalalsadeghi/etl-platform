# Python slim image for app in staging/prod
FROM python:3.12-slim

# Always set a working directory
WORKDIR /app

# System deps (add build-essential, libpq-dev later if needed)
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements and install
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app source
COPY backend/app /app/app

# Expose the internal app port (container) — Nginx will proxy to it
EXPOSE 8000

# Default command: start uvicorn (prod settings will be tuned later)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
