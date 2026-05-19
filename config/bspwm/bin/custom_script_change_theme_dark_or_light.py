#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


GTK_SCHEMA = "org.gnome.desktop.interface"

THEME_DARK = "Tokyonight-Dark"
THEME_LIGHT = "Tokyonight-Light"

ICON_THEME = "Tokyonight-Dark-Cyan"

FONT_NAME = "Adwaita Sans 11"
CURSOR_THEME = "Qogir-cursors"
CURSOR_SIZE = 24

TOOLBAR_STYLE = "GTK_TOOLBAR_BOTH_HORIZ"
TOOLBAR_ICON_SIZE = "GTK_ICON_SIZE_LARGE_TOOLBAR"
BUTTON_IMAGES = 0
MENU_IMAGES = 0
EVENT_SOUNDS = 1
INPUT_FEEDBACK_SOUNDS = 1
XFT_ANTIALIAS = 1
XFT_HINTING = 1
XFT_HINTSTYLE = "hintmedium"


def gsettings_get(schema: str, key: str) -> str:
    result = subprocess.run(
        ["gsettings", "get", schema, key],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip().strip("'")


def gsettings_set(schema: str, key: str, value: str) -> None:
    subprocess.run(
        ["gsettings", "set", schema, key, value],
        check=True,
    )


def write_default_cursor_theme() -> None:
    content = f"""[Icon Theme]
Inherits={CURSOR_THEME}
"""

    for path in (
        Path.home() / ".icons/default/index.theme",
        Path.home() / ".local/share/icons/default/index.theme",
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def set_cursor_global() -> None:
    gsettings_set(GTK_SCHEMA, "cursor-theme", CURSOR_THEME)
    gsettings_set(GTK_SCHEMA, "cursor-size", str(CURSOR_SIZE))
    write_default_cursor_theme()
    subprocess.run(["xsetroot", "-cursor_name", "left_ptr"], check=False)


def build_settings_ini(theme_name: str) -> str:
    return f"""[Settings]
gtk-theme-name={theme_name}
gtk-icon-theme-name={ICON_THEME}
gtk-font-name={FONT_NAME}
gtk-cursor-theme-name={CURSOR_THEME}
gtk-cursor-theme-size={CURSOR_SIZE}
gtk-toolbar-style={TOOLBAR_STYLE}
gtk-toolbar-icon-size={TOOLBAR_ICON_SIZE}
gtk-button-images={BUTTON_IMAGES}
gtk-menu-images={MENU_IMAGES}
gtk-enable-event-sounds={EVENT_SOUNDS}
gtk-enable-input-feedback-sounds={INPUT_FEEDBACK_SOUNDS}
gtk-xft-antialias={XFT_ANTIALIAS}
gtk-xft-hinting={XFT_HINTING}
gtk-xft-hintstyle={XFT_HINTSTYLE}
"""


def write_settings_ini(theme_name: str) -> None:
    for gtk_dir in (
        Path.home() / ".config/gtk-3.0",
        Path.home() / ".config/gtk-4.0",
    ):
        gtk_dir.mkdir(parents=True, exist_ok=True)
        (gtk_dir / "settings.ini").write_text(
            build_settings_ini(theme_name),
            encoding="utf-8",
        )


def set_light() -> None:
    gsettings_set(GTK_SCHEMA, "gtk-theme", THEME_LIGHT)
    gsettings_set(GTK_SCHEMA, "icon-theme", ICON_THEME)
    gsettings_set(GTK_SCHEMA, "color-scheme", "default")
    write_settings_ini(THEME_LIGHT)
    set_cursor_global()


def set_dark() -> None:
    gsettings_set(GTK_SCHEMA, "gtk-theme", THEME_DARK)
    gsettings_set(GTK_SCHEMA, "icon-theme", ICON_THEME)
    gsettings_set(GTK_SCHEMA, "color-scheme", "prefer-dark")
    write_settings_ini(THEME_DARK)
    set_cursor_global()


def main() -> None:
    try:
        current_theme = gsettings_get(GTK_SCHEMA, "gtk-theme")
        current_scheme = gsettings_get(GTK_SCHEMA, "color-scheme")

        print(f"Current gtk-theme: {current_theme}")
        print(f"Current color-scheme: {current_scheme}")

        if current_theme == THEME_DARK or current_scheme == "prefer-dark":
            set_light()
            print(f"Switched to LIGHT: {THEME_LIGHT}")
        else:
            set_dark()
            print(f"Switched to DARK: {THEME_DARK}")

        print(f"Icon theme: {ICON_THEME}")
        print(f"Cursor theme: {CURSOR_THEME}")

    except subprocess.CalledProcessError as exc:
        print("gsettings command failed")
        print(exc)
        sys.exit(1)
    except Exception as exc:
        print("theme switch failed")
        print(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()