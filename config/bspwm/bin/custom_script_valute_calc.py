#!/usr/bin/env python3

import urllib.request
import json
from pathlib import Path
import subprocess

IMAGE_PATH = Path.home() / ".config" / "bspwm" / "wallpaper" / "rofi" / "custom_script_valute_calc.png"


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
            check=True
        )

    except Exception:
        print("[failed to render image]")


def get_rates(base="USD"):
    url = f"https://open.er-api.com/v6/latest/{base}"

    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode())


def input_currency(currencies):
    print("Available currencies:\n")
    print(", ".join(currencies))

    base = input("\nEnter the base currency: ").upper()

    if base not in currencies:
        raise ValueError(f"Invalid base currency: {base}")

    target = input("Enter the target currency: ").upper()

    if target not in currencies:
        raise ValueError(f"Invalid target currency: {target}")

    return base, target


def input_amount():
    amount = input("\nEnter the amount: ")

    try:
        return float(amount)

    except ValueError:
        raise ValueError(f"Invalid amount: {amount}")


def main():
    try:
        # only 1 request here
        usd_data = get_rates("USD")

        currencies = sorted(usd_data["rates"].keys())

        base, target = input_currency(currencies)

        # reuse first request if base is USD
        if base == "USD":
            data = usd_data
        else:
            # second request only if needed
            data = get_rates(base)

        print(f"\nCurrent rate:")
        print(f"1 {base} = {data['rates'][target]:.4f} {target}")

        amount = input_amount()

        converted = amount * data["rates"][target]

        print(f"\n{amount} {base} = {converted:.2f} {target}")

    except ValueError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    print_image(IMAGE_PATH)
    main()
    input("\nPress Enter to exit...")