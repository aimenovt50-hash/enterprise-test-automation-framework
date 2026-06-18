from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

import allure

from src.config.settings import get_global_settings

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    max_attempts: int | None = None,
    delay_seconds: float | None = None,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry decorator aligned with global framework policy."""

    settings = get_global_settings()
    attempts = max_attempts or settings.retry.max_attempts
    delay = delay_seconds if delay_seconds is not None else settings.retry.delay_seconds

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error: BaseException | None = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    last_error = error
                    if attempt == attempts:
                        break
                    allure.attach(
                        f"Attempt {attempt}/{attempts} failed: {error}",
                        name="retry",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    time.sleep(delay)
            assert last_error is not None
            raise last_error

        return wrapper

    return decorator
