# Test-Driven Development (TDD)

This project will follow TDD: write a failing test first, implement the smallest change to pass, then refactor.

## Core Loop (Red-Green-Refactor)
1) Red: Write a test for the next behavior. Run tests and confirm failure.
2) Green: Implement the minimal code to make the test pass.
3) Refactor: Clean up code and tests without changing behavior.

## Scope of Tests
- Models: validation, defaults, computed fields, constraints.
- Permissions: role-based access and org scoping.
- Views: HTTP status, template selection, redirects, messages.
- Workflows: invitation flow, period approvals, budget updates.

## Guidelines
- One behavior per test.
- Prefer Arrange-Act-Assert structure.
- Keep tests deterministic; avoid external services.
- Use factories/fixtures to reduce setup noise.
- Add integration tests for end-to-end paths that cross multiple layers.

## Django Notes
- Use Django's test runner or pytest-django (to be selected during setup).
- Store tests alongside apps in `tests/` modules.
- Use database transactions per test to isolate state.

## Example Flow
- Write test: "BudgetPeriod cannot be created when an open period exists." (fails)
- Implement check in model/service; make test pass.
- Refactor for clarity, keep tests green.
