#!/usr/bin/env python3

from pathlib import Path
import subprocess


keyboard_shortcuts_window = [
    ("super + w", "close window"),
    ("super + t", "tiled"),
    ("super + s", "floating"),
    ("super + f", "fullscreen"),
    ("super + h/j/k/l", "focus window"),
    ("super + shift + h/j/k/l", "move window"),
    ("super + c", "next window"),
    ("super + shift + c", "previous window"),
    ("super + m", "toggle layout"),
    ("super + 1-6", "switch workspace"),
    ("super + shift + 1-6", "move window to workspace"),
    ("super + left mouse", "move window with mouse"),
    ("super + right mouse", "resize window from corner"),
]

keyboard_shortcuts_system = [
    ("super + alt + r", "reload bspwm"),
    ("super + escape", "reload sxhkd"),
    ("alt + shift", "switch keyboard layout"),
    ("super + enter", "open terminal"),
    ("super + space", "app launcher"),
    ("super + d", "custom menu"),
    ("super + v", "clipboard history"),
    ("super + p", "power menu"),
    ("super + e", "file manager"),
    ("print / super + shift + s", "screenshot"),
    ("super + alt + c", "pick color"),

    ("ctrl + shift + c/v", "copy / paste terminal"),
    ("ctrl + r", "search command history"),
    ("ctrl + l", "clear terminal"),
    ("ctrl + a/e", "line start / end"),
    ("ctrl + w", "delete previous word"),
    ("ctrl + u", "delete before cursor"),
    ("ctrl + k", "delete after cursor"),
    ("tab", "autocomplete"),
]

keyboard_shortcuts_yazi = [
    ("!", "open shell here"),
    (":", "command mode"),
    ("h/j/k/l", "navigate"),
    ("Enter", "open file / enter dir"),
    ("Backspace", "go back"),
    ("Space", "select file"),
    ("y / p", "copy / paste"),
    ("x / p", "cut / paste"),
    ("a", "new file"),
    ("Shift + A", "new directory"),
    ("r", "rename"),
    ("d", "delete"),
    ("o", "open with"),
    ("xdg-open file", "open in default app"),
    ("q", "quit"),
]

keyboard_shortcuts_nvim = [
    ("0 / ^ / $", "line start / first char / end"),
    ("w / b", "next / prev word"),
    ("gg / G", "top / bottom"),
    ("{ / }", "prev / next paragraph"),
    ("space + e", "file explorer"),
    ("/text", "search"),
    ("n / N", "next / prev result"),
    ("i / a", "insert before / after"),
    ("I / A", "start / end of line"),
    ("o / O", "new line below / above"),
    ("x", "delete char"),
    ("dd", "delete line"),
    ("yy / p", "copy / paste line"),
    ("d", "delete"),
    ("diw", "delete word"),
    ("ciw", "change word"),
    ("C", "change to end of line"),
    ("v / V", "select"),
    ("ggVG", "select all"),
    (":%s/old/new/g", "replace all"),
    (":%s/old/new/gc", "replace confirm"),
    (":w", "save"),
    (":q", "quit"),
    (":wq", "save & quit"),
    (":bd", "close buffer"),
    ("shift + h / l", "prev / next buffer"),
    (":vsp", "vertical split"),
    (":sp", "horizontal split"),
    ("ctrl + h/j/k/l", "move between splits"),
    ("u / ctrl + r", "undo / redo"),
    (":SudaWrite", "save as root"),
    ("alt + →", "accept copilot"),
    ("ctrl + ] / [", "next / prev copilot"),
    (":Copilot auth", "enable copilot"),
]

IMAGE_PATH = Path.home() / ".config/bspwm/wallpaper/rofi/custom_script_help.png"


def load_main_color() -> str | None:
    conf_file = Path.home() / ".config/bspwm/conf/color.conf"

    if not conf_file.exists():
        return None

    for line in conf_file.read_text().splitlines():
        if "=" not in line:
            continue

        key, value = line.strip().split("=", 1)

        if key.strip() == "MAIN":
            return value.strip()

    return None


def c(text: str, color: str | None) -> str:
    if not color or not color.startswith("#") or len(color) != 7:
        return text

    try:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
    except ValueError:
        return text

    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def print_image(path: Path) -> None:
    if not path.exists():
        print(f"[image not found: {path}]")
        return

    try:
        subprocess.run(
            [
                "chafa",
                str(path),
                "--size=40x20",
            ],
            check=True,
        )
    except Exception:
        print("[failed to render image]")


def get_global_width(blocks):
    width = 0

    for shortcuts in blocks:
        max_key_len = max(len(k) for k, _ in shortcuts)

        for key, desc in shortcuts:
            line_len = max_key_len + 3 + len(desc)

            if line_len > width:
                width = line_len

    return width


def print_block(title, shortcuts, color, line_width):
    print()

    print(c(f"\033[1m{title}\033[0m", color))

    # линия цветная
    print(c("─" * line_width, color))

    max_key_len = max(len(k) for k, _ in shortcuts)

    for key, desc in shortcuts:
        key_colored = c(key.ljust(max_key_len), color)
        print(f"{key_colored}   {desc}")


def keyboard_help(color):
    blocks = [
        keyboard_shortcuts_window,
        keyboard_shortcuts_system,
        keyboard_shortcuts_yazi,
        keyboard_shortcuts_nvim,
    ]

    line_width = get_global_width(blocks)

    print_block(
        "WINDOW MANAGEMENT",
        keyboard_shortcuts_window,
        color,
        line_width,
    )

    print_block(
        "SYSTEM / GENERAL",
        keyboard_shortcuts_system,
        color,
        line_width,
    )

    print_block(
        "YAZI FILE MANAGER",
        keyboard_shortcuts_yazi,
        color,
        line_width,
    )

    print_block(
        "NEOVIM",
        keyboard_shortcuts_nvim,
        color,
        line_width,
    )


def main():
    main_color = load_main_color()

    print_image(IMAGE_PATH)

    keyboard_help(main_color)

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
