#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path

IMAGE_PATH = Path.home() / ".config" / "bspwm" / "wallpaper" / "rofi" / "custom_script_checks.png"

FAIL_COUNT = 0
WARN_COUNT = 0

STD_PKG = [
    "python",
    "openssh",

    "ttf-dejavu",
    "ttf-font-awesome",
    "ttf-nerd-fonts-symbols",
    "ttf-jetbrains-mono-nerd",
    "noto-fonts",

    "dunst",
    "libnotify",

    "dbus",
    "libcanberra",
    "xdg-desktop-portal",
    "xdg-desktop-portal-gtk",

    "xorg-server",
    "xorg-xinit",
    "xorg-xrandr",

    "bspwm",
    "sxhkd",

    "bat",
    "eza",
    "btop",
    "fastfetch",
    "less",

    "vim",
    "neovim",
    "nodejs",
    "npm",
    "git",
    "base-devel",

    "kitty",

    "feh",
    "mpv",

    "picom",
    "polybar",

    "xclip",
    "xsel",

    "rofi",
    "firefox",

    "yazi",
    "ffmpegthumbnailer",
    "poppler",
    "fd",
    "ripgrep",
    "fzf",
    "zoxide",
    "chafa",
    "resvg",
    "7zip",

    "pipewire",
    "pipewire-audio",
    "pipewire-alsa",
    "pipewire-pulse",
    "wireplumber",
    "alsa-utils",

    "flameshot",

    "imagemagick",
    "scrot",

    "xcolor",

    "reflector",
    "pacman-contrib",

    "dconf",
    "gsettings-desktop-schemas",

    "udisks2",
    "udiskie",
    "ntfs-3g",
    "exfatprogs",
    "gvfs",
    "gvfs-mtp",

    "networkmanager",

    "gtk3",
    "gtk4",
    "glib2",
    "gdk-pixbuf2",
    "pango",
    "cairo",
    "atk",
    "adwaita-icon-theme",
    "gtk3-demos",
    "lxappearance",

    "calcurse",
]

YAY_PKG = [
    "greenclip",
    "i3lock-color",
    "xwinwrap-git",
    "tokyonight-gtk-theme-git",
]

PROCESS_LIST = [
    "bspwm",
    "sxhkd",
    "dunst",
    "picom",
    "polybar",
    "greenclip",
    "pipewire",
    "pipewire-pulse",
    "wireplumber",
    "udiskie",
]

USER_SERVICES = [
    "pipewire.service",
    "pipewire-pulse.service",
    "wireplumber.service",
]

SYSTEM_SERVICES = [
    "NetworkManager.service",
    "dbus.service",
]

ENV_LIST = [
    ("dbus", "DBUS_SESSION_BUS_ADDRESS"),
    ("desktop", "XDG_CURRENT_DESKTOP"),
    ("display", "DISPLAY"),
]

CMD_LIST = [
    "python",
    "ssh",
    "bspwm",
    "sxhkd",
    "dunst",
    "notify-send",
    "rofi",
    "polybar",
    "kitty",
    "feh",
    "xrandr",
    "mpv",
    "picom",
    "greenclip",
    "flameshot",
    "xclip",
    "xsel",
    "yazi",
    "fastfetch",
    "chafa",
    "reflector",
    "checkupdates",
    "yay",
]


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def ok(text: str) -> None:
    print(f"OK   {text}")


def fail(text: str) -> None:
    global FAIL_COUNT
    FAIL_COUNT += 1
    print(f"FAIL {text}")


def warn(text: str) -> None:
    global WARN_COUNT
    WARN_COUNT += 1
    print(f"WARN {text}")


def print_image(path: Path) -> None:
    if not path.exists():
        print(f"[image not found: {path}]")
        return

    if shutil.which("chafa") is None:
        print("[chafa not installed]")
        return

    try:
        subprocess.run(["chafa", str(path), "--size=40x20"], check=True)
    except Exception:
        print("[failed to render image]")


def has_cmd(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def pacman_installed(pkg: str) -> bool:
    return run(["pacman", "-Q", pkg]).returncode == 0


def check_pkg_list() -> None:
    print("\n== PACMAN PACKAGES ==\n")

    for pkg in STD_PKG:
        if pacman_installed(pkg):
            ok(f"pkg: {pkg}")
        else:
            fail(f"pkg: {pkg}")


def check_yay_pkg_list() -> None:
    print("\n== YAY / AUR PACKAGES ==\n")

    if not has_cmd("yay"):
        fail("yay not installed")
        return

    for pkg in YAY_PKG:
        if pacman_installed(pkg):
            ok(f"aur: {pkg}")
        else:
            fail(f"aur: {pkg}")


def check_cmd_list() -> None:
    print("\n== COMMANDS ==\n")

    for cmd in CMD_LIST:
        if has_cmd(cmd):
            ok(f"cmd: {cmd}")
        else:
            fail(f"cmd: {cmd}")


def check_process(process: str) -> bool:
    return run(["pgrep", "-x", process]).returncode == 0


def check_process_list() -> None:
    print("\n== PROCESSES ==\n")

    for process in PROCESS_LIST:
        if check_process(process):
            ok(f"process: {process}")
        else:
            fail(f"process: {process}")


def check_env_list() -> None:
    print("\n== ENV ==\n")

    for name, var in ENV_LIST:
        if os.environ.get(var):
            ok(f"env: {name} / {var}")
        else:
            fail(f"env: {name} / {var}")


def systemctl_user_active(service: str) -> bool:
    return run(["systemctl", "--user", "is-active", "--quiet", service]).returncode == 0


def systemctl_system_active(service: str) -> bool:
    return run(["systemctl", "is-active", "--quiet", service]).returncode == 0


def check_user_services() -> None:
    print("\n== USER SERVICES ==\n")

    for service in USER_SERVICES:
        if systemctl_user_active(service):
            ok(f"user service: {service}")
        else:
            fail(f"user service: {service}")


def check_system_services() -> None:
    print("\n== SYSTEM SERVICES ==\n")

    for service in SYSTEM_SERVICES:
        if systemctl_system_active(service):
            ok(f"system service: {service}")
        else:
            fail(f"system service: {service}")


def check_bspwm_config() -> None:
    print("\n== BSPWM CONFIG ==\n")

    paths = [
        Path.home() / ".config/bspwm/bspwmrc",
        Path.home() / ".config/sxhkd/sxhkdrc",
        Path.home() / ".config/polybar/config.ini",
        Path.home() / ".config/dunst/dunstrc",
        Path.home() / ".config/rofi",
        Path.home() / ".config/bspwm/conf",
    ]

    for path in paths:
        if path.exists():
            ok(f"path: {path}")
        else:
            fail(f"path: {path}")


def check_wallpaper_assets() -> None:
    print("\n== WALLPAPER / ROFI ASSETS ==\n")

    paths = [
        Path.home() / ".config/bspwm/conf/wallpaper",
        Path.home() / ".config/bspwm/conf/wallpaper.conf",
        Path.home() / ".config/bspwm/wallpaper/rofi",
    ]

    for path in paths:
        if path.exists():
            ok(f"path: {path}")
        else:
            fail(f"path: {path}")


def check_theme_soft() -> None:
    print("\n== THEME SOFT CHECK ==\n")

    gtk3 = Path.home() / ".config/gtk-3.0/settings.ini"
    gtk4 = Path.home() / ".config/gtk-4.0/settings.ini"

    if gtk3.exists():
        ok(f"gtk3 settings: {gtk3}")
    else:
        warn(f"gtk3 settings missing: {gtk3}")

    if gtk4.exists():
        ok(f"gtk4 settings: {gtk4}")
    else:
        warn(f"gtk4 settings missing: {gtk4}")

    if Path("/usr/share/icons/Adwaita").exists():
        ok("icons: Adwaita")
    else:
        warn("icons missing: Adwaita")

    tokyo_paths = [
        Path("/usr/share/themes/Tokyonight-Dark"),
        Path("/usr/share/themes/Tokyonight"),
        Path("/usr/share/themes/Tokyonight-Storm"),
        Path.home() / ".themes/Tokyonight-Dark",
        Path.home() / ".themes/Tokyonight",
        Path.home() / ".themes/Tokyonight-Storm",
    ]

    if any(p.exists() for p in tokyo_paths):
        ok("theme: Tokyonight found")
    else:
        warn("theme: Tokyonight not found")


def check_audio() -> None:
    print("\n== AUDIO ==\n")

    if not has_cmd("pactl"):
        fail("cmd: pactl")
        return

    result = run(["pactl", "info"])

    if result.returncode == 0:
        ok("pactl info")
    else:
        fail("pactl info")


def print_result() -> None:
    print("\n== RESULT ==\n")

    if FAIL_COUNT > 0:
        print(f"System unhealthy: {FAIL_COUNT} failed, {WARN_COUNT} warnings")
    else:
        print(f"System OK: {WARN_COUNT} warnings")


def main() -> None:
    print_image(IMAGE_PATH)

    check_pkg_list()
    check_yay_pkg_list()
    check_cmd_list()
    check_process_list()
    check_env_list()
    check_user_services()
    check_system_services()
    check_bspwm_config()
    check_wallpaper_assets()
    check_theme_soft()
    check_audio()

    print_result()

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
