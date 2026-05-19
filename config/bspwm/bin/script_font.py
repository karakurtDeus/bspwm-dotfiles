#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess


def read_conf(path: Path) -> dict[str, str]:
    values = {}

    if not path.exists():
        return values

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()

    return values


def load_config() -> dict[str, str]:
    path = Path.home() / ".config/bspwm/conf/font.conf"
    values = read_conf(path)

    return {
        "FONT_SIZE_GLOBAL": values.get("FONT_SIZE_GLOBAL", ""),
        "FONT_SIZE_KITTY": values.get("FONT_SIZE_KITTY", "10.5"),
        "FONT_SIZE_POLYBAR": values.get("FONT_SIZE_POLYBAR", "10;3"),
        "FONT_SIZE_DUNST": values.get("FONT_SIZE_DUNST", "10"),
        "FONT_SIZE_ROFI": values.get("FONT_SIZE_ROFI", "10.5"),
    }


def font_value(config: dict[str, str], key: str) -> str:
    return config["FONT_SIZE_GLOBAL"] or config[key]


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


def change_kitty_font(font_size: str) -> bool:
    try:
        path = Path.home() / ".config/kitty/kitty.conf"

        if not path.exists():
            print("kitty error: kitty.conf not found")
            return False

        lines = path.read_text(encoding="utf-8").splitlines()
        new_lines = []
        inserted = False

        for line in lines:
            stripped = line.strip()

            if stripped in {"P", "H.5"}:
                continue

            if re.match(r"^\s*font_size\s+", line):
                continue

            new_lines.append(line)

            if re.match(r"^\s*font_family\s+", line) and not inserted:
                new_lines.append(f"font_size {font_size}")
                inserted = True

        if not inserted:
            new_lines.insert(0, f"font_size {font_size}")

        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return True

    except Exception as e:
        print(f"kitty error: {e}")
        return False


def change_dunst_font(font_size: str) -> bool:
    try:
        path = Path.home() / ".config/dunst/dunstrc"

        if not path.exists():
            print("dunst error: dunstrc not found")
            return False

        lines = path.read_text(encoding="utf-8").splitlines()
        new_lines = []
        replaced = False

        for line in lines:
            if re.match(r"^\s*font\s*=", line):
                new_lines.append(f"    font = JetBrainsMono Nerd Font {font_size}")
                replaced = True
            else:
                new_lines.append(line)

        if not replaced:
            result = []
            inserted = False

            for line in new_lines:
                result.append(line)

                if line.strip() == "[global]" and not inserted:
                    result.append(f"    font = JetBrainsMono Nerd Font {font_size}")
                    inserted = True

            if not inserted:
                result.insert(0, "[global]")
                result.insert(1, f"    font = JetBrainsMono Nerd Font {font_size}")

            new_lines = result

        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return True

    except Exception as e:
        print(f"dunst error: {e}")
        return False


def change_rofi_font(font_size: str) -> bool:
    try:
        path = Path.home() / ".config/rofi/config.rasi"

        if not path.exists():
            print("rofi error: config.rasi not found")
            return False

        text = path.read_text(encoding="utf-8")
        replacement = f'font: "JetBrainsMono Nerd Font {font_size}";'

        if re.search(r'font:\s*"[^"]+";', text):
            text = re.sub(r'font:\s*"[^"]+";', replacement, text)
        else:
            text = re.sub(
                r"(?m)^\*\s*\{",
                "* {\n    " + replacement,
                text,
                count=1,
            )

        path.write_text(text, encoding="utf-8")
        return True

    except Exception as e:
        print(f"rofi error: {e}")
        return False


def change_polybar_font(font_size: str) -> bool:
    try:
        path = Path.home() / ".config/polybar/config.ini"

        if not path.exists():
            print("polybar error: config.ini not found")
            return False

        text = path.read_text(encoding="utf-8")

        pattern = r'(?m)^(\s*font-\d+\s*=\s*"[^"\n]*:size=)([^"\n]+)(")$'
        text, count = re.subn(pattern, rf"\g<1>{font_size}\g<3>", text)

        if count == 0:
            print("polybar error: no font lines matched")
            return False

        path.write_text(text, encoding="utf-8")
        return True

    except Exception as e:
        print(f"polybar error: {e}")
        return False


def main() -> None:
    config = load_config()

    kitty_size = font_value(config, "FONT_SIZE_KITTY")
    dunst_size = font_value(config, "FONT_SIZE_DUNST")
    rofi_size = font_value(config, "FONT_SIZE_ROFI")
    polybar_size = font_value(config, "FONT_SIZE_POLYBAR")

    print("Loaded config:")
    print(f"FONT_SIZE_GLOBAL={config['FONT_SIZE_GLOBAL']}")
    print(f"FONT_SIZE_KITTY={kitty_size}")
    print(f"FONT_SIZE_DUNST={dunst_size}")
    print(f"FONT_SIZE_ROFI={rofi_size}")
    print(f"FONT_SIZE_POLYBAR={polybar_size}")

    if change_kitty_font(kitty_size):
        print("OK: kitty font changed")
    else:
        print("FAILED: kitty font changed")

    if change_dunst_font(dunst_size):
        print("OK: dunst font changed")
        reload_dunst()
    else:
        print("FAILED: dunst font changed")

    if change_rofi_font(rofi_size):
        print("OK: rofi font changed")
    else:
        print("FAILED: rofi font changed")

    if change_polybar_font(polybar_size):
        print("OK: polybar font changed")
        reload_polybar()
    else:
        print("FAILED: polybar font changed")


if __name__ == "__main__":
    main()