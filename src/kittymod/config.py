import toml
from typing import Any

CONFIG = None


def get_config() -> dict[str, Any]:
    global CONFIG

    if CONFIG is not None:
        return CONFIG

    CONFIG = toml.load("kittymod.toml")
    return CONFIG
