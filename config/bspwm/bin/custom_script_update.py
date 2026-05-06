#!/usr/bin/env python3

from pathlib import Path
import subprocess
import shutil

from custom_script_checks import YAY_PKG

IMAGE_PATH = Path.home() / ".config" / "bspwm" / "wallpaper" / "rofi" / "custom_script_update.png"


def print_image(path: Path) -> None:
    if not path.exists():
        print(f"[image not found: {path}]")
        return

    if shutil.which("chafa") is None:
        print("[chafa not installed]")
        return

    try:
        subprocess.run(["chafa", str(path), "--size=40x20"], check=True)
    except subprocess.CalledProcessError:
        print("[failed to render image]")


def run(cmd) -> int:
    return subprocess.call(cmd)


def ask(q: str) -> bool:
    return input(f"{q} [y/N]: ").strip().lower() in ("y", "yes")


def has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def update_mirrors() -> None:
    if not has("reflector"):
        print("reflector not installed (skip)")
        return

    print("\nUpdating mirrors...\n")
    run([
        "sudo", "reflector",
        "--latest", "10",
        "--sort", "rate",
        "--save", "/etc/pacman.d/mirrorlist",
    ])


def check_repo_updates() -> list[str]:
    if not has("checkupdates"):
        print("Install pacman-contrib")
        return []

    result = subprocess.run(
        ["checkupdates"],
        capture_output=True,
        text=True,
    )

    return [line for line in result.stdout.splitlines() if line.strip()]


def check_aur_updates() -> list[str]:
    if not has("yay"):
        print("yay not installed (skip AUR check)")
        return []

    result = subprocess.run(
        ["yay", "-Qua"],
        capture_output=True,
        text=True,
    )

    return [line for line in result.stdout.splitlines() if line.strip()]


def is_installed(pkg: str) -> bool:
    result = subprocess.run(
        ["pacman", "-Q", pkg],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def upgrade_repo() -> None:
    print("\nUpgrading repo packages...\n")
    run(["sudo", "pacman", "-Syu"])


def upgrade_aur() -> None:
    if not has("yay"):
        print("yay not installed (skip AUR upgrade)")
        return

    print("\nUpgrading AUR packages...\n")
    run(["yay", "-Sua"])


def full_rebuild_yay_package(pkg: str) -> None:
    if not has("yay"):
        print("yay not installed")
        return

    print(f"\nFull rebuild: {pkg}\n")

    if is_installed(pkg):
        print(f"Removing {pkg} with unused deps...\n")
        run(["yay", "-Rns", "--noconfirm", pkg])
    else:
        print(f"{pkg} is not installed, installing fresh...\n")

    print(f"\nInstalling/Rebuilding {pkg}...\n")
    run(["yay", "-S", "--noconfirm", pkg])


def choose_rebuild_package() -> None:
    print("\nAvailable yay packages for full rebuild:\n")

    for i, pkg in enumerate(YAY_PKG, start=1):
        installed = "installed" if is_installed(pkg) else "not installed"
        print(f"{i}) {pkg} [{installed}]")

    choice = input("\nChoose package number: ").strip()

    if not choice.isdigit():
        print("Invalid choice")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(YAY_PKG):
        print("Invalid choice")
        return

    full_rebuild_yay_package(YAY_PKG[index])


def main() -> None:
    print_image(IMAGE_PATH)

    if ask("Update mirrors?"):
        update_mirrors()

    repo_updates = check_repo_updates()
    repo_count = len(repo_updates)

    print(f"\nFound {repo_count} repo updates\n")
    if repo_count > 0:
        for update in repo_updates:
            print(update)

    if repo_count > 0 and ask("\nUpgrade repo packages?"):
        upgrade_repo()

    aur_updates = check_aur_updates()
    aur_count = len(aur_updates)

    print(f"\nFound {aur_count} AUR updates\n")
    if aur_count > 0:
        for update in aur_updates:
            print(update)

    if aur_count > 0 and ask("\nUpgrade AUR packages?"):
        upgrade_aur()

    if ask("\nDo you want yay package full rebuild?"):
        choose_rebuild_package()

    print("\nDone.")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
