# Workflow Documentation

This document captures the current workflow and domain behavior for the construction contracts system. It is a working specification and will be refined later.

## Organization and Roles
- Organization is the primary tenant.
- Roles within an organization:
  - CEO
  - AccountManager
  - BudgetManager
  - ConstructionManager
- Permissions are scoped by organization membership.
- Roles prefixed with "Sub" (e.g., SubCEO, SubConstructionManager) are equivalent to their base roles but scoped to a subcontractor organization in relation to the main organization.

## Frontend Language
- UI text will be provided in Czech only for the initial release.
- The frontend must be prepared for future multilingual support (i18n-ready).

### Subcontractor Organizations
- An organization can invite a subcontractor.
- Inviting a subcontractor creates a Sub Organization with role "SUBCEO".
- SUBCEO manages the Sub Organization similarly to CEO in the main organization.
- Permissions are scoped based on whether the user belongs to the main organization or a subcontractor.

## Authentication and Invitation Workflow
- CEO registers publicly and creates the Organization.
- CEO can send invitation links via email.
- Users can register only through invitation links.
- Invitation links are required for all non-CEO users.

## Construction and Orders
- Organization owns Constructions.
- Construction contains Orders.
- Orders have assigned ConstructionManagers.

## Contract For Work
Each Order has a ContractForWork with the following fields:
- ContractNumber (string, required)
- ContractorShare (double)
- ContractSigned (DateTime)
- DayAfterDue (int)
- EndContract (DateTime)
- IsSocialHouse (bool)
- StartContract (DateTime)
- TaxReverseCharge (bool)
- WarrantyPeriod (int)
- Residuals (List<Residual>)

### Residual
- ContractForWork (navigation property)
- ContractForWorkId (int)
- EndDate (DateTime)
- Percentage (int)

## Budgets
- Orders contain Budgets.
- Budget can include an Appendix (to be added later).
- ExcelFile must be stored with the Budget.
- Excel import is deferred and will be handled later.

### Budget Approval Workflow
- BudgetManager creates a Budget.
- SubConstructionManager/ConstructionManager creates a Period.
- When a Period is open, a new Period cannot be created.
- SubConstructionManager can add an Amount and save it for a single Period.
- BudgetItem Amount is the source of truth and must be validated against current and previous periods.
- SubConstructionManager submits the Period for review.
- ConstructionManager can Accept or Decline the Period.
- If Declined, the Period returns to unsubmitted status.
- When Declining, ConstructionManager adds a payment, penalty, or fee.
- If Accepted, SubContractor can close the Period.

### Budget Structure
- Budget has BudgetHeaders.
- BudgetHeader can have ChildHeaders (tree structure).
- BudgetHeader has BudgetItems.

### BudgetItem
- Code (string)
- Describe (string)
- MeasureUnit (string)
- PriceForUnit (float/double)
