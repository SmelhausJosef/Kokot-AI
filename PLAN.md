# Implementation Plan

This plan is phased to build the system safely from foundations to delivery. Each phase can be delivered and verified independently.

## Phase 0 - Project Bootstrap
- Initialize Django project structure and settings for Postgres.
- Set up Vite asset pipeline for Material Web (M3) components and static builds.
- Add environment configuration, secrets handling, and local run scripts.
- Select the test framework (pytest-django vs Django test runner) and wire it up.
- Define basic CI checks (lint, test placeholders).

## Phase 1 - Authentication and Organization Core
- Implement invitation-only registration flow.
- Create Organization and Role models with scoped membership.
- Support CEO public signup to create the first Organization.

## Phase 2 - Core Domain Models
- Implement Construction, Order, ContractForWork, Residual.
- Add admin screens and minimal CRUD views.
- Enforce organization scoping for all queries.

## Phase 3 - Budget Structures
- Implement Budget, BudgetHeader (tree), BudgetItem.
- Store original Excel file with the Budget.
- Add BudgetPeriod model and states aligned with workflow docs.

## Phase 4 - Budget Approval Workflow
- Implement Period lifecycle: open, submit, accept/decline, close.
- Validate BudgetItem amount against current and previous periods.
- Capture decline metadata (payment, penalty, fee).

## Phase 5 - UI and Localization
- Implement server-rendered pages for core workflows.
- Apply Material Web (M3) components and theme tokens for consistent styling.
- Provide Czech UI strings and i18n-ready templates.
- Add role-based navigation and permission checks.

## Phase 6 - Excel Import
- Build parser based on `documentation/import-excel.md`.
- Map headers and items into BudgetHeader/BudgetItem.
- Store measurement notes or skip them per final decision.

## Phase 7 - Deployment Readiness
- Create Dockerfile and Kubernetes manifests.
- Add health checks and migration job template.
- Add OpenTelemetry configuration (env vars, exporter endpoint, log correlation).
- Document deployment steps and required environment variables.

## Phase 8 - Hardening and Tests
- Add unit tests for critical workflows (invitation, budgets, periods).
- Add import validation tests for Excel parsing.
- Review performance, indexing, and audit logging needs.
