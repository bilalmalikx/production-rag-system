# ============================================
# STAGE 1: Backend Setup
# ============================================
FROM python:3.11-slim AS backend

WORKDIR /backend

# Install system dependencies (including libgomp1 for fastembed)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app/ ./app/
COPY data/ ./data/
COPY .env .

# Create necessary directories
RUN mkdir -p /backend/data/vector_store /backend/data/uploads /backend/logs

EXPOSE 8000


# ============================================
# STAGE 2: Frontend Setup (Build)
# ============================================
FROM node:20-slim AS frontend-builder

WORKDIR /frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Build Angular app
RUN npm run build -- --configuration production


# ============================================
# STAGE 3: Final Runtime (Nginx + Backend Python)
# ============================================
FROM python:3.11-slim

# Install nginx, supervisor, AND system dependencies (CRITICAL for fastembed/onnxruntime)
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    curl \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directories
WORKDIR /app

# Copy backend from stage 1 (including site-packages and binaries)
COPY --from=backend /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend /usr/local/bin /usr/local/bin
COPY --from=backend /backend /app

# Copy frontend build from stage 2
COPY --from=frontend-builder /frontend/dist/frontend/browser /var/www/html

# ============================================
# Configure Nginx for Angular + API Proxy
# ============================================
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /var/www/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
    location /api/ { \
        proxy_pass http://127.0.0.1:8000/; \
        proxy_http_version 1.1; \
        proxy_set_header Upgrade $http_upgrade; \
        proxy_set_header Connection "upgrade"; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
    } \
}' > /etc/nginx/sites-available/default

# ============================================
# Configure Supervisor (Run both services)
# ============================================
RUN echo '[supervisord]\n\
nodaemon=true\n\
\n\
[program:backend]\n\
command=uvicorn app.main:app --host 0.0.0.0 --port 8000\n\
directory=/app\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/backend.err.log\n\
stdout_logfile=/var/log/backend.out.log\n\
\n\
[program:nginx]\n\
command=nginx -g "daemon off;"\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/nginx.err.log\n\
stdout_logfile=/var/log/nginx.out.log\n\
' > /etc/supervisor/conf.d/app.conf

# Expose ports
EXPOSE 80 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start supervisor
CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]