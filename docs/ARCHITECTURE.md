# Architecture

## Layers

```
tests/          → scenarios, markers, fixtures
src/flows/      → multi-step business flows
src/pages/      → Page Object Model (behavior)
src/pages/locators/ → selectors (UI map)
src/data/       → test data factories
src/config/     → environment + runtime settings
src/utils/      → cross-cutting utilities (retry)
```

## Design principles

1. **Locators separated from behavior** — selectors live in `locators/`, pages expose intent-based methods.
2. **Flows over fat tests** — reusable journeys (`AuthFlow`) keep tests declarative.
3. **Config-driven execution** — YAML environments, `.env` overrides, feature flags via `require_feature()`.
4. **Observable failures** — Allure steps, screenshots, optional Playwright trace/video on failure.
5. **Retry as policy** — `@retry` reads defaults from `config/settings.yaml`.

## Fixture lifecycle

| Fixture | Scope | Responsibility |
|---------|-------|----------------|
| `browser` | session | Single browser process per run |
| `context` | function | Isolated cookies/storage; trace/video |
| `page` | function | Active tab with env timeout |
| `registered_user` | function | Registers user via UI flow |

## CI strategy

- **PR / push**: smoke (`-m smoke`) — fast gate
- **Main branch**: regression (`-m regression`) — full suite in parallel
- **Manual**: optional prod via `workflow_dispatch` with approval

## Extending for company SaaS

1. Add locators + page objects per product area.
2. Add environment YAML under `config/environments/`.
3. Gate experimental UI behind `features` in env YAML.
4. Prefer API setup (future `src/api/`) for long-running auth/data prep.
