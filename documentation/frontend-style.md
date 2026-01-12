# Frontend Style and UI System

## Decision
Use Material Design 3 via Material Web components (`@material/web`) with Django SSR. Components are bundled with Vite and served as static assets.

## Rationale
- Modern, consistent Material UI without moving to a React frontend.
- Works with server-rendered templates and minimal JavaScript.
- Theme tokens provide a single source of truth for color, typography, and spacing.

## Build Approach
- Use Vite to bundle a small entry file that imports only needed Material Web components.
- Ship the compiled JS/CSS as Django static files.
- Keep JS usage minimal and component driven (dialogs, menus, text fields, buttons).

## Theming
- Define Material tokens once (colors, typography, shape, elevations).
- Keep tokens in a single file and reuse across templates.
- Ensure dark mode is optional; default to light mode.

## Component Baseline
Expected first-phase components:
- Buttons, text fields, select, checkbox, switch
- Dialog, menu, tabs
- Card, list, table, chips

## Constraints
- UI copy is Czech only for initial release.
- Templates must be i18n-ready (translation keys and structured strings).
