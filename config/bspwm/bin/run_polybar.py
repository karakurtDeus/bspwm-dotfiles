#!/usr/bin/env python3

import os
import re
import subprocess
import time
from pathlib import Path

COLOR_CONF = Path.home() / ".config/bspwm/conf/color.conf"
DEFAULT_COLOR = "#329DA4"


def load_main_color() -> str:
    if not COLOR_CONF.exists():
        return DEFAULT_COLOR

    for line in COLOR_CONF.read_text().splitlines():
        if line.startswith("MAIN="):
            color = line.split("=", 1)[1].strip()
            if re.match(r"^#[0-9a-fA-F]{6}$", color):
                return color

    return DEFAULT_COLOR


def run(cmd):
    return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_monitors():
    result = subprocess.run(
        ["polybar", "--list-monitors"],
        capture_output=True,
        text=True,
    )

    return [line.split(":")[0] for line in result.stdout.splitlines() if ":" in line]


def start_polybar(color: str):
    run(["killall", "-q", "polybar"])

    while run(["pgrep", "-x", "polybar"]).returncode == 0:
        time.sleep(0.5)

    monitors = get_monitors()

    for m in monitors:
        print(f"polybar -> {m} (color={color})")

        env = os.environ.copy()
        env["MONITOR"] = m
        env["MAIN_COLOR"] = color

        subprocess.Popen(
            ["polybar", "main"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def main():
    color = load_main_color()
    start_polybar(color)


if __name__ == "__main__":
    main()
