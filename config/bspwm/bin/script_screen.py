#!/usr/bin/env python3

from pathlib import Path
import subprocess


def load_config():
    conf_file = Path.home() / ".config" / "bspwm" / "conf" / "screen.conf"

    default = """# SCREEN_TIMEOUT:
# screen saver timeout in seconds
# 5400 = 1.5 hours
# 7200 = 2 hours
SCREEN_TIMEOUT=5400

# DPMS_STANDBY:
DPMS_STANDBY=5400

# DPMS_SUSPEND:
DPMS_SUSPEND=5400

# DPMS_OFF:
DPMS_OFF=5400
"""

    conf_file.parent.mkdir(parents=True, exist_ok=True)

    if not conf_file.exists():
        conf_file.write_text(default)

    SCREEN_TIMEOUT = "5400"
    DPMS_STANDBY = "5400"
    DPMS_SUSPEND = "5400"
    DPMS_OFF = "5400"

    for line in conf_file.read_text().splitlines():
        if "=" not in line:
            continue

        key, value = line.strip().split("=", 1)
        key = key.strip()
        value = value.strip()

        if key == "SCREEN_TIMEOUT":
            SCREEN_TIMEOUT = value
        elif key == "DPMS_STANDBY":
            DPMS_STANDBY = value
        elif key == "DPMS_SUSPEND":
            DPMS_SUSPEND = value
        elif key == "DPMS_OFF":
            DPMS_OFF = value

    return SCREEN_TIMEOUT, DPMS_STANDBY, DPMS_SUSPEND, DPMS_OFF


def is_number(value: str) -> bool:
    return value.isdigit()


def apply_screen_settings(
    screen_timeout: str,
    dpms_standby: str,
    dpms_suspend: str,
    dpms_off: str,
) -> bool:
    try:
        values = [screen_timeout, dpms_standby, dpms_suspend, dpms_off]

        if not all(is_number(value) for value in values):
            print("screen error: all values must be numbers")
            return False

        subprocess.run(
            ["xset", "s", screen_timeout],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        subprocess.run(
            ["xset", "dpms", dpms_standby, dpms_suspend, dpms_off],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        return True

    except Exception as e:
        print(f"screen error: {e}")
        return False


def main():
    screen_timeout, dpms_standby, dpms_suspend, dpms_off = load_config()

    print("Loaded config:")
    print(f"SCREEN_TIMEOUT={screen_timeout}")
    print(f"DPMS_STANDBY={dpms_standby}")
    print(f"DPMS_SUSPEND={dpms_suspend}")
    print(f"DPMS_OFF={dpms_off}")

    if apply_screen_settings(
        screen_timeout,
        dpms_standby,
        dpms_suspend,
        dpms_off,
    ):
        print("OK: screen settings applied")
    else:
        print("FAILED: screen settings applied")


if __name__ == "__main__":
    main()
