# AGENTS.md

You are operating in the `kokot` project workspace.

## Primary Stack
- Backend: Django (Python)
- Frontend: Django SSR + Material Web (M3) components bundled with Vite
- Database: PostgreSQL
- Deployment: Kubernetes (stateless web tier)
- Observability: OpenTelemetry for tracing and logging

## Product Constraints
- Invitation-only registration for all non-CEO users.
- CEO creates the Organization during public registration.
- Roles: CEO, AccountManager, BudgetManager, ConstructionManager.
- Roles prefixed with "Sub" (e.g., SubCEO) are equivalent to their base roles but scoped to a subcontractor organization.
- UI copy is Czech-only for initial release, but must be i18n-ready for future languages.

## Domain Requirements
- Organization owns Constructions; Constructions own Orders.
- Orders have assigned ConstructionManagers and a ContractForWork.
- Budgets belong to Orders and store the original Excel file.
- BudgetHeaders form a tree; BudgetItems live under headers.
- Budget approval workflow uses Periods as documented in `documentation/workflows.md`.

## Excel Import
- Follow `documentation/import-excel.md` for the Zakazka sheet parsing rules.
- Do not implement Excel import without aligning with the documented mapping.

## Observability
- Follow `documentation/opentelemetry.md` for OpenTelemetry setup and configuration.

## Frontend UI
- Follow `documentation/frontend-style.md` for Material Web setup and UI conventions.

## Engineering Guidelines
- Use Django migrations for schema changes.
- Use Decimal for money and quantities; avoid float for persisted values.
- Keep frontend styling aligned with Material Web (M3) theme tokens.
- Keep documentation in `documentation/` updated when workflows or data assumptions change.
- Continuously update `documentation/` with live implementation status; record changes in `documentation/implementation-status.md`.
- Avoid adding extra infrastructure components unless requested.
- Do not push directly to `main`; open a PR from a feature branch.
- Implement features using TDD (write failing tests first, then implement).
- Before opening a PR, run backend checks, frontend build, and tests.
- Before opening a PR, merge the latest `main` into the current branch.
