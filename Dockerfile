# -----------------------------
# 1. Base Image (slim + security)
# -----------------------------
FROM python:3.11-slim AS base

# -----------------------------
# 2. Security Updates & Minimal Packages
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
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
COPY run.py .

COPY app ./app

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
