<!-- Copilot instructions for AI coding agents working on this repo -->
# Quick Start for AI Coding Agents

This project is a small Django REST application with two main apps: `api` (public REST endpoints) and `adminpanel` (staff/admin related endpoints). Follow these concise, actionable rules when making changes or suggesting code.

## Big-picture architecture
- Web framework: Django (project root: `manage.py`, settings: `assetlab/assetlab/settings.py`).
- Two primary apps: `api/` (user-facing API endpoints, see `api/views.py`, `api/models.py`, `api/serializers.py`) and `adminpanel/` (staff-facing logic, see `adminpanel/views.py`, `adminpanel/models.py`).
- Persistence: configured in `assetlab/assetlab/settings.py` to use MySQL (look at `DATABASES`). Migrations live under each app's `migrations/` directory (e.g. `api/migrations/`).
- Authentication: mixed patterns — `api` uses a custom `User` model defined in `api/models.py`, while `adminpanel` often queries Django's built-in `auth.User` for staff users.

## Key conventions & patterns (project-specific)
- Keep REST views simple and explicit: current handlers are function-based (`@api_view`) in `api/views.py` and class-based `APIView` in `adminpanel/views.py`.
- Serializers tend to be ModelSerializers that expose `fields = "__all__"` (see `api/serializers.py`). Be conservative when adding fields; migrations history includes asset-related schema changes — inspect `api/migrations/` first.
- Passwords are currently stored as plain text in custom models (e.g. `api.models.User`, `adminpanel.models.AdminUser`). Any change to authentication or password storage must consider backward compatibility and existing migrations/data.

## Developer workflows (what to run locally)
- Activate the repository's Python environment (there is a `venv/` in the workspace if present). Then run Django management commands from the repo root:

```bash
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Run the dev server
python manage.py migrate
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Run tests (if/when tests exist)
python manage.py test
```

Note: `settings.py` currently has `DEBUG = False` and hard-coded MySQL credentials; when running locally you may set `DEBUG = True` or use environment-specific settings.

## Editing rules for AI agents
- Always search `api/migrations/` and `adminpanel/migrations/` before editing models. The repo has an extensive migration history — altering models blindly can break DB state.
- When changing authentication/password handling, preserve compatibility: prefer adding a migration and a small data-migration script to upgrade stored passwords, and document the change.
- Prefer small, focused PRs. Update or add unit tests where behavior changes are introduced.
- Avoid committing secret credentials; if you modify `settings.py`, prefer using environment variables.

## Debugging & common hotspots
- Authentication/login: `api/views.login`, `adminpanel/views.AdminLoginView.post`. These are common change targets. Tests or manual curl/Postman requests against those endpoints help validate changes.
- Database surprises: if migrations and models diverge, inspect `api/migrations/` files (e.g. `0003_...`, `0007_...`) to understand past schema changes.
- Static/media: media files are served from `media/` (see `MEDIA_ROOT` in `settings.py`).

## Files to inspect for context (examples)
- `assetlab/assetlab/settings.py` — DB, installed apps, REST config
- `api/views.py`, `api/models.py`, `api/serializers.py` — public API logic
- `api/migrations/` — history of schema changes
- `adminpanel/views.py`, `adminpanel/models.py` — admin flows
- `manage.py` — standard entrypoint for management commands

## When merging existing instruction files
If a repo already contains a `.github/copilot-instructions.md`, merge by preserving any repository-specific rules. If in doubt, prefer concrete examples and explicit file references.

---
If anything here is unclear or you want more detail (example endpoints, representative tests, or recommended local settings), tell me which area to expand. 
