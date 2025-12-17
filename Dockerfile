FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Flask runs on 5000
EXPOSE 5000

# Production-ish defaults
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

CMD ["python", "run.py"]
