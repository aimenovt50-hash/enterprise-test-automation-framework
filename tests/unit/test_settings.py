from src.config.settings import get_environment_config, get_global_settings


def test_global_settings_loads_retry_policy():
    settings = get_global_settings()
    assert settings.retry.max_attempts >= 1
    assert settings.timeout_ms > 0


def test_environment_config_resolves_staging():
    config = get_environment_config("staging")
    assert config.base_url.startswith("https://")
    assert "features" in config.model_dump()
