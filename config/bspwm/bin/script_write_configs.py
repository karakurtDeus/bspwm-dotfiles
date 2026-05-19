#!/usr/bin/env python3

from pathlib import Path

from config_templates import polybar_config, kitty_config


def write_file_if_missing(path: Path, content: str) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            print(f"SKIP exists: {path}")
            return True

        path.write_text(content, encoding="utf-8")
        return True

    except Exception as e:
        print(f"FAILED write {path}: {e}")
        return False


def ensure_color_file() -> bool:
    path = Path.home() / ".config/bspwm/conf/color.conf"

    return write_file_if_missing(
        path,
        """# MAIN:
# main accent color
# example: MAIN=#329DA4
MAIN=#329DA4
""",
    )


def ensure_font_file() -> bool:
    path = Path.home() / ".config/bspwm/conf/font.conf"

    return write_file_if_missing(
        path,
        """# FONT_SIZE_GLOBAL:
# if set, overrides kitty, polybar, dunst and rofi values
FONT_SIZE_GLOBAL=

# FONT_SIZE_KITTY:
FONT_SIZE_KITTY=10.5

# FONT_SIZE_POLYBAR:
FONT_SIZE_POLYBAR=10;3

# FONT_SIZE_DUNST:
FONT_SIZE_DUNST=10

# FONT_SIZE_ROFI:
FONT_SIZE_ROFI=10.5
""",
    )


def write_kitty() -> bool:
    path = Path.home() / ".config/kitty/kitty.conf"
    return write_file_if_missing(path, kitty_config())


def write_polybar() -> bool:
    path = Path.home() / ".config/polybar/config.ini"
    return write_file_if_missing(path, polybar_config())


def main() -> None:
    if ensure_color_file():
        print("OK: ensure color.conf")

    if ensure_font_file():
        print("OK: ensure font.conf")

    if write_kitty():
        print("OK: ensure kitty.conf")

    if write_polybar():
        print("OK: ensure polybar config")


if __name__ == "__main__":
    main()