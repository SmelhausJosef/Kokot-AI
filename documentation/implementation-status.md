# Implementation Status

This file tracks delivered functionality in the repository.

## Completed in main
- Phase 0: Django project, Postgres config, Vite build, env scripts, pytest setup.
- Phase 1: Organization + roles + invitation registration; CEO public signup.
- Phase 2: Construction, Order, ContractForWork, Residual models with org scoping.
- Phase 3: Budgets, headers, items, periods; Excel file storage on Budget.
- Phase 4: Budget period workflow with validation (open -> submitted -> accepted/declined -> closed).
- Phase 5: SSR UI with Material Web, Czech i18n-ready templates, role-aware navigation; budget list/detail/create.
- Phase 6: Excel import for Zakazka sheet via openpyxl; Budget create auto-imports headers/items; import errors roll back and remove file; tests added.
- Phase 7: Docker build, Kubernetes manifests, WhiteNoise static serving, and OpenTelemetry configuration.

## In progress (current branch)
- Phase 8: Hardening tests for budget scoping and import sheet validation; deployment env fix (DJANGO_SETTINGS_MODULE).

## Pending
- None.
