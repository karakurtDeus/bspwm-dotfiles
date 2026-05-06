#!/usr/bin/env python

from pathlib import Path
import subprocess
import re

CONF_FILE = Path.home() / ".config/bspwm/conf/keyboard.conf"

DEFAULT_CONFIG = """# layouts
LAYOUTS=us
#LAYOUTS=us,ru
#LAYOUTS=us,ua
#LAYOUTS=us,ru,ua

# switch hotkey
OPTION=grp:alt_shift_toggle
#OPTION=grp:caps_toggle
#OPTION=grp:win_space_toggle
"""


def ensure_config() -> None:
    CONF_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not CONF_FILE.exists():
        CONF_FILE.write_text(DEFAULT_CONFIG)


def read_config() -> tuple[str, str]:
    ensure_config()

    layouts = "us"
    option = "grp:alt_shift_toggle"

    for line in CONF_FILE.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if key == "LAYOUTS" and re.match(r"^[a-zA-Z_,]+$", value):
            layouts = value

        elif key == "OPTION" and re.match(r"^[a-zA-Z0-9_:,-]+$", value):
            option = value

    return layouts, option


def main() -> None:
    layouts, option = read_config()

    cmd = ["setxkbmap", "-layout", layouts]

    if option:
        cmd += ["-option", option]

    subprocess.run(cmd)


if __name__ == "__main__":
    main()
