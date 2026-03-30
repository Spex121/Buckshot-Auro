# Hello!
import os
import time
import sys
import subprocess
import requests


# Updater
def updater():
    print("Checking for updates...")
    current_version = "v0.1.3-alpha"
    url = "https://api.github.com/repos/Spex121/Buckshot-Auro/releases"
    response = requests.get(url)
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
            user_input = input(
                "\nA new version is out! Would you like to update? (yes/no): "
            )
            break
        except KeyboardInterrupt:
            continue
        except EOFError:
            continue
    if user_input.lower() == "yes":
        print("Downloading...")
        is_windows = os.name == "nt"
        download_url = None
        filename = None
        for asset in latest_release["assets"]:
            asset_name = asset["name"]
            if is_windows and asset_name.endswith(".exe"):
                download_url = asset["browser_download_url"]
                filename = "auro_temp.exe"
                break
            elif not is_windows and not asset_name.endswith(".exe"):
                download_url = asset["browser_download_url"]
                filename = "auro_temp"
                break
        file_response = requests.get(download_url)
        errorD = False
        if file_response.status_code != 200:
            print("ERROR\n")
            errorD = True
        if errorD == False:
            with open(filename, "wb") as f:
                f.write(file_response.content)
            print("OK\n")
            print("Starting helper_update")
            subprocess.run(["python", "helper.py", filename])


# Localization
language = {
    "en": {
        "syntax": 'Syntax: "Combat/Blank"',
        "start": "Let's start the game!\n",
        "help": "Plus - combat\nMinus - blank\n",
        "shot": "Shot?: ",
        "combat_gone": "\nThe combat is gone!\n",
        "blank_gone": "\nThe blank are gone!\n",
        "result": lambda combat, blank: f"Combat: {combat}\nBlank: {blank}",
        "chance_c": lambda chance_c: f"Combat chance: {chance_c}%",
        "chance_b": lambda chance_b: f"Blank chance: {chance_b}%",
        "round_over": "\nThe round is over!\n",
        "history": "History: ",
        "continue": "Continue? (yes or no): ",
    },
    "ru": {
        "syntax": 'Синтаксис: "Боевые/Холостые"',
        "start": "Начинаем игру!\n",
        "help": "Плюс - боевой\nМинус - холостой\n",
        "shot": "Выстрел?: ",
        "combat_gone": "\nБоевых нет!\n",
        "blank_gone": "\nХолостых нет!\n",
        "result": lambda combat, blank: f"Боевые: {combat}\nХолостые: {blank}",
        "chance_c": lambda chance_c: f"Шанс на боевой: {chance_c}%",
        "chance_b": lambda chance_b: f"Шанс на холостой: {chance_b}%",
        "round_over": "\nРаунд окончен!\n",
        "history": "История: ",
        "continue": "Продолжить? (yes or no): ",
    },
}


# Quit app
def quitapp():
    print("\nQuit...\n")
    sys.exit()


# Clear terminal
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# STARTING
print("\n    Developed by Spex121\n")
print("=" * 30)
print("    Buckshot Auro Script\n")
print("=" * 30)


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
                print(" The language is set!")
                t = language[lang]
                time.sleep(1)
                clear()
                break
            elif lang == "ru" or lang == "2":
                lang = "ru"
                print(" Язык настроен!")
                time.sleep(1)
                t = language[lang]
                clear()
                break
            else:
                print(" ERROR!")
                print(" en or ru")
                time.sleep(2)
                clear()
                continue
        except (ValueError, KeyboardInterrupt):
            print(" ERROR")
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
            print(t["start"])
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
                        print(t["combat_gone"])
                    print(t["result"](combat, blank))
                elif user_input == "-":
                    if blank > 0:
                        blank -= 1
                        total -= 1
                        h.append("| - |")
                    elif blank == 0:
                        print(t["blank_gone"])
                    print(t["result"](combat, blank))
                else:
                    continue
                if total > 0:
                    chance_c = round(combat / total * 100, 1)
                    chance_b = round(blank / total * 100, 1)
                    print(t["chance_c"](chance_c))
                    print(t["chance_b"](chance_b))
            print(t["round_over"])
            print(t["history"] + (" ".join(h)))
            while True:
                user_input = input(t["continue"])
                if user_input == "yes" or user_input == "y":
                    break
                elif user_input == "no" or user_input == "n":
                    quitapp()
        except (ValueError, IndexError, KeyboardInterrupt):
            print("\n Error!")
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                pass
            clear()
            continue
        except EOFError:
            quitapp()


# General
updater()
setup()
main()
