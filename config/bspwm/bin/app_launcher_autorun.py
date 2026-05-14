#!/usr/bin/env python3

import time
from pathlib import Path
import subprocess

def open_link_in_browser(link: str, desktop: str) -> None:
    subprocess.run(
        [
            "bspc",
            "rule",
            "-a",
            "firefox",
            f"desktop=^{desktop}",
            "follow=off",
            "-o",
        ],
        check=True,
    )

    subprocess.Popen(
        ["firefox", "--new-window", link],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def open_on_desktop(app_class: str, command: list[str], desktop: str, rules_count: int = 1) -> None:
    for _ in range(rules_count):
        subprocess.run(
            [
                "bspc",
                "rule",
                "-a",
                app_class,
                f"desktop=^{desktop}",
                "follow=off",
                "-o",
            ],
            check=True,
        )

    subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def load_config():
    conf_file = Path.home() / ".config" / "bspwm" / "conf" / "run_workspaces.conf"

    default = """# TYPE|RULE_CLASS|COMMAND|DESKTOP|RULES_COUNT

app|obsidian|obsidian|4|1
url||https://chatgpt.com/|5|1
app|TelegramDesktop|Telegram|6|1
url||https://music.youtube.com|6|1
app|discord|discord|6|2
"""

    conf_file.parent.mkdir(parents=True, exist_ok=True)

    if not conf_file.exists():
        conf_file.write_text(default)

    actions = []

    for line in conf_file.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = [p.strip() for p in line.split("|")]

        if len(parts) < 4:
            continue

        action_type = parts[0]
        rule_class = parts[1]
        command = parts[2]
        desktop = parts[3]
        rules_count = 1

        if len(parts) >= 5 and parts[4]:
            try:
                rules_count = int(parts[4])
            except ValueError:
                rules_count = 1

        actions.append({
            "type": action_type,
            "rule_class": rule_class,
            "command": command,
            "desktop": desktop,
            "rules_count": rules_count,
        })

    return actions


def run_actions(actions, delay: float = 1.0):
    for action in actions:
        action_type = action["type"]
        rule_class = action["rule_class"]
        command = action["command"]
        desktop = action["desktop"]
        rules_count = action["rules_count"]

        if action_type == "app":
            open_on_desktop(rule_class, [command], desktop, rules_count=rules_count)
        elif action_type == "url":
            open_link_in_browser(command, desktop)

        time.sleep(delay)


def main():
    actions = load_config()
    run_actions(actions, 2)


if __name__ == "__main__":
    main()
