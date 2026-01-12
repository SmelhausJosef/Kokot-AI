# Tech Choice Documentation

## Goal
Pick a tech stack for a construction contracts web application that runs on Kubernetes and uses PostgreSQL. The focus is on reliable delivery, maintainability, and strong ecosystem support for typical business workflows.

## Summary
Chosen stack: Django (Python) + PostgreSQL, packaged in Docker and deployed to Kubernetes. This stack is widely supported in both Codex and Claude code generation, with strong ORM, migrations, admin tooling, and a large ecosystem.

## Why Django (Python)
- Mature batteries-included framework for CRUD-heavy business apps.
- Built-in admin, auth, migrations, and ORM reduce boilerplate.
- Strong Postgres support out of the box.
- Large public codebase and documentation footprint improves model performance for Codex + Claude.
- Easy to containerize and operate with Gunicorn in Kubernetes.

## Alternatives Considered
- FastAPI + SQLAlchemy: Excellent for APIs but requires more assembly for admin/auth/migrations.
- Next.js + Prisma: Great developer experience but a heavier frontend-first approach than needed for a data-centric internal app.
- NestJS + TypeORM: Strong TypeScript ecosystem but more boilerplate for the same outcomes.

## Kubernetes Fit
- Standard 12-factor config via environment variables.
- Stateless web tier with horizontal scaling.
- Supports readiness/liveness probes and run-once migration jobs.
- Compatible with managed Postgres services.

## PostgreSQL Fit
- ACID guarantees and strong relational integrity for contracts, changes, and financial tracking.
- Native support in Django ORM and migrations.
- Mature tooling for backups and observability.

## Project Structure (High-Level)
- Single Django app with modular apps as the domain grows.
- Server-rendered templates for initial delivery; API endpoints can be added later if needed.

## Future-Proofing
- If a richer frontend is required, add a separate API layer (Django REST Framework) and a JS client without replacing the backend.
- If multi-tenancy is required later, it can be added with database-level or schema-based strategies.
