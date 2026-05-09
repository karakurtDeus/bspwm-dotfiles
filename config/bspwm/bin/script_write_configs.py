#!/usr/bin/env python3

from pathlib import Path
import re

from config_templates import (
    kitty_config,
    polybar_config,
)

DEFAULT_MAIN = "#329DA4"


def ensure_color_file() -> Path:
    conf_dir = Path.home() / ".config/bspwm/conf"
    conf_dir.mkdir(parents=True, exist_ok=True)

    color_file = conf_dir / "color.conf"

    if not color_file.exists():
        color_file.write_text(
            """# MAIN:
# main accent color
# example: MAIN=#329DA4
MAIN=#329DA4
"""
        )

    return color_file


def get_main_color() -> str:
    path = ensure_color_file()

    for line in path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)

        if key.strip() == "MAIN":
            color = value.strip()

            if re.match(r"^#[0-9a-fA-F]{6}$", color):
                return color

    return DEFAULT_MAIN


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


def write_polybar(main: str) -> bool:
    path = Path.home() / ".config/polybar/config.ini"

    config = polybar_config()
    config = config.replace(
        "primary = ${env:MAIN_COLOR:#329DA4}",
        f"primary = {main}",
    )

    return write_file(path, config)


def main() -> None:
    main_color = get_main_color()

    if write_kitty():
        print("OK: write kitty config")
    else:
        print("FAILED: write kitty config")

    if write_polybar(main_color):
        print("OK: write polybar config")
    else:
        print("FAILED: write polybar config")


if __name__ == "__main__":
    main()
