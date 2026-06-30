# imports
import os
import time
import sys
import subprocess
import requests
import json
from rich.console import Console
from rich.progress import Progress, TransferSpeedColumn, BarColumn, DownloadColumn
from rich.prompt import Confirm
from lang import language

# Base variable
console = Console()
current_version = "v0.1.5-beta"
config_app = {
    "language": "",
    "pre_update": None,
    "style": 0,
    "smart_shot_prediction": None,
    "shot_history": None,
}
t = {}


# Config
def config():
    global t, config_app, DATA_PATH
    if getattr(sys, "frozen", False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "config.json")

    copy_config_app = config_app
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            copy_config_app = json.load(f)
    except FileNotFoundError:
        console.print("[red]Configuration file not found![/red]")
        time.sleep(1)
    except json.JSONDecodeError:
        console.print("\n[red]The configuration file is invalid![/red]\n")
        console.print_exception()
        time.sleep(1.6)
    if copy_config_app:
        config_app = copy_config_app
    lang_code = config_app["language"]
    if lang_code:
        t = language[lang_code]


# Updater
def updater():
    print("Checking for updates...")
    url = "https://api.github.com/repos/Spex121/Buckshot-Auro/releases"
    try:
        response = requests.get(url, timeout=6)
    except requests.exceptions.ConnectTimeout:
        console.print("\n[red]Timeout for Github[/red]\n")
        return
    except requests.exceptions.ConnectionError:
        console.print("\n[red]ConnectionError[/red]\n")
        return
    if response.status_code != 200:
        console.print(f"[red]Github API error: {response.status_code}[/red]")
        return
    releases_date = response.json()
    latest_release = releases_date[0]
    new_version = latest_release["tag_name"]
    if new_version == current_version:
        return
    is_prerelease = latest_release["prerelease"]
    if is_prerelease:
        if not config_app["pre_update"]:
            return
        is_prerelease = "[yellow]pre[/yellow]"
    else:
        is_prerelease = "[green]stable[/green]"
    console.print(f"New version: {new_version}")
    console.print(f"Installed version: {current_version}")
    console.print(f"Type: {is_prerelease}")
    while True:
        try:
            console.print(
                "\n[yellow]A new version is out! Would you like to update? (yes/no):[/yellow]",
                end="",
            )
            user_input = input(" ")
            break
        except (KeyboardInterrupt, EOFError):
            continue
    if user_input == "yes" or user_input == "y":
        console.print("[yellow]Starting...[/yellow]")
        is_windows = os.name == "nt"
        download_url = None
        filename = None
        for asset in latest_release["assets"]:
            asset_name = asset["name"]
            if is_windows and asset_name.endswith(".exe"):
                download_url = asset["browser_download_url"]
                filename = "auro_temp.exe"
                total = asset["size"]
                break
            elif not is_windows and not asset_name.endswith(".exe"):
                download_url = asset["browser_download_url"]
                filename = "auro_temp"
                total = asset["size"]
                break
        try:
            response = requests.get(
                download_url, stream=True, allow_redirects=True, timeout=6
            )
            if response.status_code != 200:
                console.print("[red]ERROR[/red]\n")
                return
            with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
            ) as progress:
                task = progress.add_task("Downloading...", total=total)
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        progress.update(task, advance=len(chunk))
        except (requests.exceptions.RequestException, KeyboardInterrupt, EOFError):
            console.print("[red]ERROR[/red]")
        console.print("[green]OK[/green]\n")
        print("Starting helper_update")
        if not is_windows:
            subprocess.Popen(["./helper", filename])
            quitapp()
        else:
            subprocess.Popen(["helper.exe", filename])
            quitapp()


# Quit app
def quitapp():
    console.print("\n[blue]Quit[/blue]...\n")
    sys.exit()


# Clear terminal
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# STARTING
print("\n    Developed by Spex121\n")
print("=" * 30)
print("    Buckshot Auro Script\n")
print("=" * 30)


# Overlay
def overlay(t):
    try:
        if os.name != "nt":
            is_wayland = os.environ.get("WAYLAND_DISPLAY")
            if is_wayland == "wayland-0":
                console.print(t["overlayE"])
                time.sleep(3)
                return
        import pywinctl

        win = pywinctl.getActiveWindow()
        win.alwaysOnTop(True)
        console.print(t["overlay"])
        time.sleep(1)
        clear()
    except Exception:
        console.print_exception()
        console.print("[red]Failed to launch overlay![/red]")


# Settings setup
def setup():
    global t, config_app
    while True:
        if not t:
            print("\n    Available language")
            print(" 1. English")
            print(" 2. Russian\n")
            lang = input("en or ru: ").strip().lower()
            if lang not in ["1", "2", "en", "ru"]:
                console.print(" [red]ERROR![/red]\nen or ru")
                time.sleep(2)
                clear()
                continue
            lang_code = "en" if lang in ["en", "1"] else "ru"
            config_app["language"] = lang_code
            t = language[lang_code]
            console.print(t["language"])

            answer = Confirm.ask(t["pre_update"])
            if answer:
                config_app["pre_update"] = True
            else:
                config_app["pre_update"] = False

            console.print("[green]OK[/green]")
            time.sleep(1)

            while True:
                try:
                    console.print(f"1. {t['syntax']}\n2. {t['syntax2']}")
                    answer = int(console.input(t["style"]).strip())
                    if answer not in [1, 2]:
                        console.print("\n[red]1 or 2[/red]\n")
                        continue
                    break
                except (TypeError, ValueError):
                    console.print("\n[red]Num only![/red]\n")
            if answer == 1:
                config_app["style"] = 1
            else:
                config_app["style"] = 2
            console.print("[green]OK[/green]")
            time.sleep(1)

            answer = Confirm.ask(t["smart"])
            if answer:
                config_app["smart_shot_prediction"] = True
            else:
                config_app["smart_shot_prediction"] = False

            console.print("[green]OK[/green]")
            time.sleep(1)

            answer = Confirm.ask(t["shot_history"])
            if answer:
                config_app["shot_history"] = True
            else:
                config_app["shot_history"] = False

            console.print("[green]OK[/green]")
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(config_app, f, ensure_ascii=False, indent=4)
            console.print("[yellow][INFO][/yellow] Saving complete!\n")
        time.sleep(0.8)
        answer = Confirm.ask(t["overlay_ask"])
        if answer:
            time.sleep(0.5)
            console.print("[yellow]Starting...[/yellow]")
            overlay(t)
        else:
            console.print("[red]OK[/red]")
            time.sleep(0.5)
        break


# Main logic
def main():
    while True:
        clear()
        print("BuckShot Auro Script")
        try:
            clear()
            if config_app["style"] == 1:
                console.print(t["syntax"])
                user_input = input("*: ")
                parts = user_input.split("/")
                combat = int(parts[0])
                blank = int(parts[1])
            else:
                console.print(t["syntax2"])
                user_input = input("x: ")
                parts = user_input.split("/")
                blank = int(parts[0])
                combat = int(parts[1])
            total = combat + blank
            console.print(t["help"])
            console.print(t["start"])
            h = []
            while total > 0:
                user_input = input(t["shot"])
                clear()
                if user_input == "+":
                    if combat > 0:
                        combat -= 1
                        total -= 1
                        h.append("| + |")
                    elif combat == 0:
                        console.print(t["combat_gone"])
                    print(t["result"](combat, blank))

                elif user_input == "-":
                    if blank > 0:
                        blank -= 1
                        total -= 1
                        h.append("| - |")
                    elif blank == 0:
                        console.print(t["blank_gone"])
                    print(t["result"](combat, blank))
                else:
                    continue
                if total > 0:
                    if config_app["smart_shot_prediction"]:
                        chance_c = round(combat / total * 100, 1)
                        chance_b = round(blank / total * 100, 1)
                        console.print(t["chance_c"](chance_c))
                        console.print(t["chance_b"](chance_b))
            console.print(t["round_over"])
            if config_app["shot_history"]:
                console.print(t["history"] + (" ".join(h)))
            while True:
                user_input = input(t["continue"])
                if user_input == "yes" or user_input == "y":
                    break
                elif user_input == "no" or user_input == "n":
                    quitapp()
        except (ValueError, IndexError, KeyboardInterrupt):
            console.print("\n [red]Error![/red]")
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                pass
            clear()
            continue
        except EOFError:
            quitapp()


# GeneraL
try:
    config()
    updater()
    setup()
    main()
except Exception as e:
    if isinstance(e, EOFError):
        quitapp()
    console.print(
        "\n[red]Critical error!\nAn emergency shutdown has been triggered[/red]"
    )
    time.sleep(1)
    console.print_exception()
except KeyboardInterrupt:
    pass
