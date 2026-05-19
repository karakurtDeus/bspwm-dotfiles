#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess

from config_templates import dunst_config, rofi_config, fastfetch_config

DEFAULT_MAIN = "#329DA4"

COLOR_SECONDARY_TEXT = "#C5C8C6"
COLOR_FOREGROUND = "#ffffff"
COLOR_BACKGROUND = "#000000"


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
""",
            encoding="utf-8",
        )

    return color_file


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
""",
            encoding="utf-8",
        )

    return font_file


def read_conf(path: Path) -> dict[str, str]:
    values = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    return values


def get_main_color() -> str:
    values = read_conf(ensure_color_file())
    color = values.get("MAIN", DEFAULT_MAIN)

    if re.match(r"^#[0-9a-fA-F]{6}$", color):
        return color

    return DEFAULT_MAIN


def get_rofi_font_size() -> str:
    values = read_conf(ensure_font_file())

    return (
        values.get("FONT_SIZE_GLOBAL", "")
        or values.get("FONT_SIZE_ROFI", "")
        or values.get("FONT_SIZE_KITTY", "")
        or "10.5"
    )


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def hex_to_fastfetch(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return f"38;2;{r};{g};{b}"


def write_file(path: Path, content: str) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"FAILED write {path}: {e}")
        return False


def write_dunst(main: str) -> bool:
    path = Path.home() / ".config/dunst/dunstrc"

    config = dunst_config(
        main=main,
        bg=COLOR_BACKGROUND,
        fg=COLOR_FOREGROUND,
    )

    return write_file(path, config)


def write_rofi(main: str, font_size: str) -> bool:
    path = Path.home() / ".config/rofi/config.rasi"

    config = rofi_config(
        main=main,
        bg=COLOR_BACKGROUND,
        fg=COLOR_FOREGROUND,
        secondary=COLOR_SECONDARY_TEXT,
        font_size=font_size,
    )

    return write_file(path, config)


def write_fastfetch(main: str) -> bool:
    path = Path.home() / ".config/fastfetch/config.jsonc"

    config = fastfetch_config(
        main_ansi=hex_to_fastfetch(main),
        font_ansi=hex_to_fastfetch(COLOR_FOREGROUND),
    )

    return write_file(path, config)


def apply_bspwm_color(main: str) -> bool:
    try:
        subprocess.run(
            ["bspc", "config", "focused_border_color", main],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


def reload_dunst() -> None:
    subprocess.run(
        ["killall", "dunst"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    subprocess.Popen(
        ["dunst"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    main_color = get_main_color()
    rofi_font_size = get_rofi_font_size()

    print("Loaded config:")
    print(f"MAIN={main_color}")
    print(f"FONT_SIZE_ROFI={rofi_font_size}")

    if apply_bspwm_color(main_color):
        print("OK: bspwm focused_border_color")
    else:
        print("FAILED: bspwm focused_border_color")

    if write_rofi(main_color, rofi_font_size):
        print("OK: write rofi config")
    else:
        print("FAILED: write rofi config")

    if write_dunst(main_color):
        print("OK: write dunst config")
    else:
        print("FAILED: write dunst config")

    if write_fastfetch(main_color):
        print("OK: write fastfetch config")
    else:
        print("FAILED: write fastfetch config")

    reload_dunst()


if __name__ == "__main__":
    main()