#!/usr/bin/env python3

import subprocess
import sys
import time
import re
from pathlib import Path

IMG = "/tmp/lock.png"

COLOR_CONF = Path.home() / ".config/bspwm/conf/color.conf"

DEFAULT_MAIN = "#329DA4"
COLOR_BACKGROUND = "#000000"
COLOR_SECONDARY_TEXT = "#C5C8C6"
COLOR_FOREGROUND = "#ffffff"


def get_main_color() -> str:
    if not COLOR_CONF.exists():
        return DEFAULT_MAIN

    for line in COLOR_CONF.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)

        if key.strip() == "MAIN":
            color = value.strip()

            if re.match(r"^#[0-9a-fA-F]{6}$", color):
                return color

    return DEFAULT_MAIN


def hex_to_i3lock(hex_color: str) -> str:
    return hex_color.lstrip("#") + "FF"


def run(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"command failed: {cmd}", file=sys.stderr)
        print(e, file=sys.stderr)
        return False


def main() -> None:
    MAIN = get_main_color()

    time.sleep(0)

    if not run(["scrot", "-o", IMG]):
        return
    if not run(["magick", IMG, "-blur", "0x8", IMG]):
        return

    if not run(
        [
            "i3lock",
            "-i",
            IMG,
            f"--ring-color={hex_to_i3lock(MAIN)}",
            f"--inside-color={hex_to_i3lock(COLOR_BACKGROUND)}",
            f"--ringver-color={hex_to_i3lock(COLOR_SECONDARY_TEXT)}",
            f"--insidever-color={hex_to_i3lock(COLOR_BACKGROUND)}",
            f"--verif-color={hex_to_i3lock(COLOR_FOREGROUND)}",
            f"--ringwrong-color={hex_to_i3lock(MAIN)}",
            f"--insidewrong-color={hex_to_i3lock(COLOR_BACKGROUND)}",
            f"--wrong-color={hex_to_i3lock(MAIN)}",
            f"--keyhl-color={hex_to_i3lock(COLOR_SECONDARY_TEXT)}",
            f"--bshl-color={hex_to_i3lock(COLOR_SECONDARY_TEXT)}",
        ]
    ):
        return


if __name__ == "__main__":
    main()
