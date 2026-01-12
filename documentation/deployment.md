# Deployment Notes

This document describes how to build and run the app in Docker and Kubernetes.

## Docker Image

Build:

```sh
docker build -t kokot-web:latest .
```

Run locally (expects a reachable Postgres):

```sh
docker run --rm -p 8000:8000 \
  -e DJANGO_SECRET_KEY=change-me \
  -e POSTGRES_HOST=host.docker.internal \
  -e POSTGRES_PASSWORD=kokot \
  kokot-web:latest
```

Static files are bundled with Vite and collected during the image build. The runtime uses WhiteNoise to serve `/static/` assets. The collect step does not require database access unless app imports touch the DB at startup.

## Kubernetes Manifests

Manifests live in `k8s/`:
- `k8s/configmap.yaml`: non-secret env vars including OpenTelemetry config.
- `k8s/secret.yaml`: secrets for DB password and Django secret key.
- `k8s/job-migrate.yaml`: migration job.
- `k8s/deployment.yaml`: web deployment with health probes.
- `k8s/service.yaml`: ClusterIP service.
- `k8s/ingress.yaml`: optional ingress.

Apply:

```sh
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/job-migrate.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Environment Variables

Required:
- `DJANGO_SECRET_KEY`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

Production settings:
- `DJANGO_DEBUG=0`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`

OpenTelemetry (optional but recommended):
- `OTEL_SERVICE_NAME`
- `OTEL_TRACES_EXPORTER`
- `OTEL_LOGS_EXPORTER`
- `OTEL_EXPORTER_OTLP_ENDPOINT`
- `OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED`
- `OTEL_PYTHON_LOG_CORRELATION`
- `OTEL_PYTHON_LOG_LEVEL`
- `OTEL_PYTHON_EXCLUDED_URLS`
