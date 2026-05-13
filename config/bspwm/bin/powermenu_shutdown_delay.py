#!/usr/bin/env python3

from pathlib import Path
import subprocess
import time
import re

IMAGE_PATH = Path.home() / ".config/bspwm/wallpaper/rofi/powermenu_shutdown_delay.png"


def parse_time(value: str) -> int | None:
    value = value.strip().lower()

    hours = 0
    minutes = 0

    h_match = re.search(r"(\d+)\s*h", value)
    m_match = re.search(r"(\d+)\s*m", value)

    if h_match:
        hours = int(h_match.group(1))

    if m_match:
        minutes = int(m_match.group(1))

    if hours == 0 and minutes == 0:
        return None

    return hours * 3600 + minutes * 60


def print_image(path: Path) -> None:
    if not path.exists():
        print(f"[image not found: {path}]")
        return

    try:
        subprocess.run(
            ["chafa", str(path), "--size=40x20"],
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        print("[failed to render image]")


def format_time(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def countdown(seconds: int) -> None:
    while seconds > 0:
        print(f"\rPoweroff in: {format_time(seconds)}", end="", flush=True)
        time.sleep(1)
        seconds -= 1

    print("\nPoweroff now...")
    subprocess.run(["systemctl", "poweroff"])


def main() -> None:
    print_image(IMAGE_PATH)

    value = input("\nShutdown after [example: 30m / 1h / 2h 30m]: ")
    seconds = parse_time(value)

    if seconds is None:
        print("FAILED: use format like 30m, 1h, 2h 30m")
        return

    print()
    print(f"Timer set: {format_time(seconds)}")
    print("Keep this window open. Ctrl+C cancels.")
    print()

    try:
        countdown(seconds)
    except KeyboardInterrupt:
        print("\nCancelled")


if __name__ == "__main__":
    main()
