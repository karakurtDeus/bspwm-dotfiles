#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess

from config_templates import polybar_config, kitty_config

DEFAULT_MAIN = "#329DA4"


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


def ensure_font_file() -> Path:
    conf_dir = Path.home() / ".config/bspwm/conf"
    conf_dir.mkdir(parents=True, exist_ok=True)

    font_file = conf_dir / "font.conf"

    if not font_file.exists():
        font_file.write_text(
            """# FONT_SIZE_GLOBAL:
# if set, overrides kitty, polybar, dunst and rofi values
FONT_SIZE_GLOBAL=

# FONT_SIZE_KITTY:
FONT_SIZE_KITTY=10.5

# FONT_SIZE_POLYBAR:
FONT_SIZE_POLYBAR=10;2

# FONT_SIZE_DUNST:
FONT_SIZE_DUNST=10

# FONT_SIZE_ROFI:
FONT_SIZE_ROFI=10.5
"""
        )

    return font_file


def get_polybar_font_size() -> str:
    path = ensure_font_file()

    font_size_global = ""
    font_size_polybar = "10;2"

    for line in path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if key == "FONT_SIZE_GLOBAL":
            font_size_global = value
        elif key == "FONT_SIZE_POLYBAR":
            font_size_polybar = value

    return font_size_global if font_size_global else font_size_polybar


def apply_polybar_color(config: str, main: str) -> str:
    config = config.replace(
        "primary = ${env:MAIN_COLOR:#329DA4}",
        f"primary = {main}",
    )

    config = re.sub(
        r"(?m)^\s*primary\s*=\s*#[0-9a-fA-F]{6}\s*$",
        f"primary = {main}",
        config,
    )

    return config


def apply_polybar_font_size(config: str, font_size: str) -> str:
    if not font_size:
        return config

    pattern = r'(?m)^(\s*font-\d+\s*=\s*"[^"\n]*:size=)([^"\n]+)(")$'
    config, _ = re.subn(pattern, rf"\g<1>{font_size}\g<3>", config)

    return config


def write_polybar(main: str, font_size: str) -> bool:
    path = Path.home() / ".config/polybar/config.ini"

    config = polybar_config()
    config = apply_polybar_color(config, main)
    config = apply_polybar_font_size(config, font_size)

    return write_file(path, config)


def reload_polybar() -> None:
    subprocess.run(
        ["killall", "-q", "polybar"],
        stderr=subprocess.DEVNULL,
    )

    subprocess.run(
        [
            "sh",
            "-c",
            "while pgrep -x polybar >/dev/null; do sleep 0.5; done; polybar main &",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    main_color = get_main_color()
    font_size = get_polybar_font_size()

    print("Loaded config:")
    print(f"MAIN={main_color}")
    print(f"FONT_SIZE_POLYBAR={font_size}")

    if write_polybar(main_color, font_size):
        print("OK: write polybar config")
        reload_polybar()
    else:
        print("FAILED: write polybar config")

    if write_kitty():
        print("OK: write kitty config")
    else:
        print("FAILED: write kitty config")


if __name__ == "__main__":
    main()