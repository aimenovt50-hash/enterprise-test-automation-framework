# Enterprise Test Automation Framework

Universal UI test framework for company SaaS products. Built as a **production-ready scaffold** with layered architecture, environment configuration, observability, and a smoke → regression CI strategy.

## Principles (senior-level)

| Principle | Implementation |
|-----------|----------------|
| **Separation of concerns** | Locators → Pages → Flows → Tests |
| **Config as code** | YAML env + `.env` overrides + feature flags |
| **Observable failures** | Allure steps, screenshots, optional trace/video |
| **Retry as policy** | `@retry` reads defaults from `config/settings.yaml` |
| **Fast feedback** | Smoke on PR, regression on main |

## Architecture

```
tests/                 # scenarios and fixtures
src/flows/             # business flows (AuthFlow)
src/pages/             # Page Object Model
src/pages/locators/    # selectors (UI map)
src/data/factories/    # test data generation
src/config/            # environments and runtime settings
docs/ARCHITECTURE.md   # design decisions
```

## Stack

Playwright (sync) · pytest · Allure · pytest-xdist · pytest-rerunfailures · Pydantic · Faker

## Quick start

```powershell
cd d:\QA\enterprise-test-automation-framework
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
copy .env.example .env
```

## Running tests

```powershell
pytest -m smoke --env=staging          # PR gate
pytest -m regression --env=staging     # full suite
pytest -m auth --env=staging           # domain filter
pytest -m negative --env=staging       # negative scenarios
pytest -n auto -m regression --env=staging
python scripts/run_tests.py --env staging --markers regression --parallel
```

## Markers

- `smoke` — critical path (< 2 min)
- `regression` — full UI regression
- `e2e` — end-to-end scenarios
- `auth` / `dashboard` — domain filters
- `negative` — validation and error-path checks

## Configuration

```env
ENV=staging
HEADLESS=true
BROWSER=chromium
DEFAULT_TIMEOUT=15000
```

Feature flags in `config/environments/*.yaml`:

```yaml
features:
  new_dashboard: true
```

Usage in tests: `require_feature(env_config, "new_dashboard")`.

## CI/CD

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | smoke (PR) + regression (main), parallel, Allure |
| `lint.yml` | ruff on `src`, `tests` |

## Extending for your product

1. Add locators and page objects per product area.
2. Create flows for key user journeys.
3. Add env YAML with `base_url`, `features`, and credentials via CI secrets.
4. Wire API setup for preconditions when needed.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.
