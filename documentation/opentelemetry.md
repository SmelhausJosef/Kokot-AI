# OpenTelemetry Logging and Tracing

This project will use OpenTelemetry for distributed tracing and logging. The goal is to export traces and logs to an OpenTelemetry Collector via OTLP, with auto-instrumentation for Django and common libraries.

## References (official)
- Python zero-code instrumentation: https://opentelemetry.io/docs/zero-code/python/
- Python zero-code configuration: https://opentelemetry.io/docs/zero-code/python/configuration/
- Python logs auto-instrumentation example: https://opentelemetry.io/docs/zero-code/python/logs-example/
- Python distro: https://opentelemetry.io/docs/languages/python/distro/
- Python exporters: https://opentelemetry.io/docs/languages/python/exporters/
- SDK env configuration (general): https://opentelemetry.io/docs/languages/sdk-configuration/general/
- SDK env configuration (OTLP): https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/

## Approach
Use Python auto-instrumentation (OpenTelemetry distro) to capture traces and logs with minimal code changes.

### Packages
Install the distro and OTLP exporter (per official docs):

```sh
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install
```

Notes:
- The distro installs the API/SDK and the `opentelemetry-instrument` and `opentelemetry-bootstrap` tools.
- `opentelemetry-bootstrap -a install` scans installed packages and installs matching instrumentation libraries.

### Run the app with auto-instrumentation
Use `opentelemetry-instrument` to start the Django app (gunicorn example):

```sh
opentelemetry-instrument \
  gunicorn config.wsgi:application
```

Alternatively, configure via environment variables (example):

```sh
export OTEL_SERVICE_NAME=kokot-web
export OTEL_TRACES_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
opentelemetry-instrument \
  gunicorn config.wsgi:application
```

## Logging (OTel Logs Auto-Instrumentation)
OpenTelemetry logs auto-instrumentation attaches an OTLP handler to the Python root logger. Enable it with:

```sh
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
```

Optional log correlation and formatting controls (from the agent configuration doc):

```sh
export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_PYTHON_LOG_FORMAT="%(msg)s [span_id=%(span_id)s]"
export OTEL_PYTHON_LOG_LEVEL=info
```

## Django-Specific Controls
The agent supports Django auto-instrumentation. Useful options:

- Disable Django instrumentation if needed:
  `OTEL_PYTHON_DJANGO_INSTRUMENT=false`
- Add Django request attributes to spans:
  `OTEL_PYTHON_DJANGO_TRACED_REQUEST_ATTRS='path_info,content_type'`

## Excluding Health Checks
Exclude internal endpoints from instrumentation to reduce noise, e.g.:

```sh
export OTEL_PYTHON_EXCLUDED_URLS="healthz,healthcheck"
```

## Core OTEL Environment Variables
Common env variables used in Kubernetes manifests:

```sh
# Service identity
OTEL_SERVICE_NAME=kokot-web
OTEL_RESOURCE_ATTRIBUTES=service.version=0.1.0,deployment.environment=dev

# Exporter configuration
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
OTEL_EXPORTER_OTLP_HEADERS=api-key=example

# Signals
OTEL_TRACES_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp

# Sampling (optional)
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1
```

Refer to the SDK configuration docs for the complete list and behavior of these variables.

## Local Collector (for testing)
The distro documentation includes a minimal OpenTelemetry Collector config with an OTLP receiver and debug exporter. Use that config to validate that traces and logs are emitted before wiring to a production backend.

## Implementation Notes
- Use `Decimal` for monetary values; avoid logging sensitive data.
- Keep the health check path excluded from tracing/logging.
- Start with auto-instrumentation; add manual spans only if specific business operations need deeper visibility.
