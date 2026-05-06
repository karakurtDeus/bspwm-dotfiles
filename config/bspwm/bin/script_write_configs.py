#!/usr/bin/env python

from pathlib import Path

from config_templates import (
    kitty_config,
    polybar_config,
)


def write_file(path: Path, content: str) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return True
    except Exception as e:
        print(f"FAILED write {path}: {e}")
        return False


def write_kitty() -> bool:
    path = Path.home() / ".config/kitty/kitty.conf"
    return write_file(path, kitty_config())


def write_polybar() -> bool:
    path = Path.home() / ".config/polybar/config.ini"
    return write_file(path, polybar_config())


def main() -> None:
    if write_kitty():
        print("OK: write kitty config")
    else:
        print("FAILED: write kitty config")

    if write_polybar():
        print("OK: write polybar config")
    else:
        print("FAILED: write polybar config")


if __name__ == "__main__":
    main()
