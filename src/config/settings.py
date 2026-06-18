from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
ENVIRONMENTS_DIR = CONFIG_DIR / "environments"


class RetryConfig(BaseModel):
    max_attempts: int = 3
    delay_seconds: float = 1.0


class ReportingConfig(BaseModel):
    screenshots_on_failure: bool = True
    video_on_failure: bool = False
    trace_on_failure: bool = False


class GlobalSettings(BaseModel):
    name: str = "enterprise-saas"
    timeout_ms: int = 15000
    retry: RetryConfig = Field(default_factory=RetryConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)


class EnvironmentCredentials(BaseModel):
    admin_email: str = ""
    admin_password: str = ""


class EnvironmentConfig(BaseModel):
    name: str
    base_url: str
    api_url: str = ""
    credentials: EnvironmentCredentials = Field(default_factory=EnvironmentCredentials)
    features: dict[str, bool] = Field(default_factory=dict)


class RuntimeSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: str = Field(default="staging", alias="ENV")
    base_url: str | None = Field(default=None, alias="BASE_URL")
    headless: bool = Field(default=True, alias="HEADLESS")
    browser: str = Field(default="chromium", alias="BROWSER")
    slow_mo: int = Field(default=0, alias="SLOW_MO")
    default_timeout: int = Field(default=15000, alias="DEFAULT_TIMEOUT")


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


@lru_cache
def get_global_settings() -> GlobalSettings:
    load_dotenv(PROJECT_ROOT / ".env")
    data = _load_yaml(CONFIG_DIR / "settings.yaml")
    return GlobalSettings.model_validate(data)


@lru_cache
def get_environment_config(env_name: str | None = None) -> EnvironmentConfig:
    load_dotenv(PROJECT_ROOT / ".env")
    runtime = RuntimeSettings()
    selected_env = env_name or runtime.env
    env_path = ENVIRONMENTS_DIR / f"{selected_env}.yaml"

    if not env_path.exists():
        available = sorted(p.stem for p in ENVIRONMENTS_DIR.glob("*.yaml"))
        raise FileNotFoundError(
            f"Environment '{selected_env}' not found. Available: {', '.join(available)}"
        )

    data = _load_yaml(env_path)
    config = EnvironmentConfig.model_validate(data)

    if runtime.base_url:
        config.base_url = runtime.base_url.rstrip("/")

    return config


@lru_cache
def get_runtime_settings() -> RuntimeSettings:
    load_dotenv(PROJECT_ROOT / ".env")
    return RuntimeSettings()
