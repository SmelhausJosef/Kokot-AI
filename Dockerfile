FROM node:20-slim AS frontend

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY frontend ./frontend
COPY vite.config.js ./
RUN npm run build

FROM python:3.12-slim AS backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=frontend /app/static/dist /app/static/dist

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["opentelemetry-instrument", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
