# imports
import os
import time
import sys
import subprocess
import requests
from rich.console import Console
from rich.progress import Progress, TransferSpeedColumn, BarColumn, DownloadColumn
import pywinctl

# Base variable
console = Console()


# Updater
def updater():
    print("Checking for updates...")
    current_version = "v0.1.4-alpha"
    url = "https://api.github.com/repos/Spex121/Buckshot-Auro/releases"
    try:
        response = requests.get(url, timeout=6)
    except requests.exceptions.ConnectTimeout:
        console.print("\n[red]Timeout for Github[/red]\n")
        return
    except requests.exceptions.ConnectionError:
        console.print("\n[red]ConnectionError[/red]\n")
        return

    releases_date = response.json()
    latest_release = releases_date[0]
    new_version = latest_release["tag_name"]
    if new_version == current_version:
        return
    is_prerelease = latest_release["prerelease"]
    print(f"New version: {new_version}")
    if is_prerelease == True:
        is_prerelease = "pre"
    else:
        is_prerelease = "stable"
    print(f"Type: {is_prerelease}")
    while True:
        try:
            console.print(
                "\n[yellow]A new version is out! Would you like to update? (yes/no):[/yellow]",
                end="",
            )
            user_input = input(" ")
            break
        except KeyboardInterrupt, EOFError:
            continue
    if user_input.lower() == "yes":
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
        except requests.exceptions.RequestException, KeyboardInterrupt, EOFError:
            console.print("[red]ERROR[/red]")
        console.print("[green]OK[/green]\n")
        print("Starting helper_update")
        if not is_windows:
            subprocess.run(["python", "helper", filename])
        else:
            subprocess.run(["python", "helper.exe", filename])


# Localization
language = {
    "en": {
        "syntax": 'Syntax: "Combat/Blank"',
        "start": "[green]Let's start the game![/green]\n",
        "help": "Plus - combat\nMinus - blank\n",
        "shot": "Shot?: ",
        "combat_gone": "\n[red]The combat is gone![/red]\n",
        "blank_gone": "\n[red]The blank are gone![/red]\n",
        "result": lambda combat, blank: f"Combat: {combat}\nBlank: {blank}",
        "chance_c": lambda chance_c: f"Combat chance: {chance_c}%",
        "chance_b": lambda chance_b: f"Blank chance: {chance_b}%",
        "round_over": "\n[yellow]The round is over![/yellow]\n",
        "history": "History: ",
        "continue": "Continue? (yes or no): ",
        "overlay": "[green]The overlay is running![/green]",
    },
    "ru": {
        "syntax": 'Синтаксис: "Боевые/Холостые"',
        "start": "Начинаем игру!\n",
        "help": "Плюс - боевой\nМинус - холостой\n",
        "shot": "Выстрел?: ",
        "combat_gone": "\n[red]Боевых нет![/red]\n",
        "blank_gone": "\n[red]Холостых нет![/red]\n",
        "result": lambda combat, blank: f"Боевые: {combat}\nХолостые: {blank}",
        "chance_c": lambda chance_c: f"Шанс на боевой: {chance_c}%",
        "chance_b": lambda chance_b: f"Шанс на холостой: {chance_b}%",
        "round_over": "\nРаунд окончен!\n",
        "history": "История: ",
        "continue": "Продолжить? (yes or no): ",
        "overlay": "[green]Оверлей запущен![/green]",
    },
}


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
    win = pywinctl.getActiveWindow()
    win.alwaysOnTop(True)
    console.print(t["overlay"])
    time.sleep(1)
    clear()


# Settings setup
def setup():
    global t
    while True:
        print("\n    Available language")
        print(" 1. English")
        print(" 2. Russian\n")
        try:
            lang = input("en or ru: ")
            if lang == "en" or lang == "1":
                lang = "en"
                console.print(" [green]The language is set![/green]")
                t = language[lang]
                time.sleep(1)
                user_input = input("Do you want to launch the overlay? (yes or no): ")
                if user_input == "yes" or user_input == "y":
                    console.print("[green]Starting...[/green]")
                    time.sleep(1)
                    overlay(t)
                else:
                    console.print("[red]Okay[/red]")
                    time.sleep(1)
                break
            elif lang == "ru" or lang == "2":
                lang = "ru"
                console.print(" [green]Язык настроен![/green]")
                time.sleep(1)
                t = language[lang]
                user_input = input("Вы хотите запустить оверлей? (yes или no): ")
                if user_input == "yes" or user_input == "y":
                    console.print("[green]Запускаю...[/green]")
                    time.sleep(1)
                    overlay(t)
                else:
                    console.print("[red]Окей[/red]")
                    time.sleep(1)
                break
            else:
                console.print(" [red]ERROR![/red]")
                print(" en or ru")
                time.sleep(2)
                clear()
                continue
        except (ValueError, KeyboardInterrupt):
            console.print(" [red]ERROR[/red]")
            print("en or ru\n")
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                pass
            clear()
        except EOFError:
            quitapp()


# Main logic
def main():
    while True:
        clear()
        print("BuckShot Auro Script")
        try:
            clear()
            print(t["syntax"])
            user_input = input("*: ")
            parts = user_input.split("/")
            combat = int(parts[0])
            blank = int(parts[1])
            total = combat + blank
            print(t["help"])
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
                    chance_c = round(combat / total * 100, 1)
                    chance_b = round(blank / total * 100, 1)
                    print(t["chance_c"](chance_c))
                    print(t["chance_b"](chance_b))
            console.print(t["round_over"])
            print(t["history"] + (" ".join(h)))
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
        return t


# General
updater()
setup()
main()
