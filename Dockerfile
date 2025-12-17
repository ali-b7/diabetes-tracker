FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Flask runs on 5000
EXPOSE 5000

# Ensure Flask binds correctly inside container
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV PYTHONUNBUFFERED=1


CMD ["python", "run.py"]
