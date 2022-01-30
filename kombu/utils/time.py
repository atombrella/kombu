"""Time Utilities."""
# flake8: noqa


__all__ = ('maybe_s_to_ms',)

from typing import Optional, Union


def maybe_s_to_ms(v: Optional[Union[int, float]]) -> int:
    """Convert seconds to milliseconds, but return None for None."""
    return int(float(v) * 1000.0) if v is not None else v
