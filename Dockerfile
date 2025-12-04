# -----------------------------
# 1. Base Image (slim + security)
# -----------------------------
FROM python:3.11-slim AS base

# -----------------------------
# 2. Security Updates & Packages
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 3. Create App Directory
# -----------------------------
WORKDIR /app

# -----------------------------
# 4. Install Python Dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------
# 5. Copy Application Code
# -----------------------------
# نسخ run.py أولًا لأنه خارج app
COPY run.py .
# نسخ مجلد app كامل
COPY app ./app

# Ensure uploads directory exists
RUN mkdir -p app/static/uploads

# -----------------------------
# 6. Set Environment Variables
# -----------------------------
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production \
    PYTHONPATH=/app \
    PORT=5001

# -----------------------------
# 7. Non-root User (Security)
# -----------------------------
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# -----------------------------
# 8. Expose Port
# -----------------------------
EXPOSE 5001

# -----------------------------
# 9. Run the Application
# -----------------------------
CMD ["python", "run.py"]
