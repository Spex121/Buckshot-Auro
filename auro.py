# Hello! Auro script
import os
import time
global lang
def quitapp():
    print("\nQuit...\n")
    exit()
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
print("    Developed by Spex121\n")
print("=" * 30)
print("    Buckshot Auro Script\n")
print("=" * 30)
def setup():
    while True:
        print("    Available language")
        print(" 1. English")
        print(" 2. Russian\n")
        try:
            global lang
            lang = int(input("1 or 2: "))
            if lang == 1:
                print(" The language is set!")
                time.sleep(2)
                clear()
                break
            elif lang == 2:
                print(" Язык настроен!")
                time.sleep(1)
                clear()
                break
 
            else:
                print(" ERROR!")
                print(" 1 or 2")
                time.sleep(2)
                clear()
                continue
        except (ValueError, KeyboardInterrupt):
            print(" ERROR")
            print("1 or 2\n")
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                pass
            clear()
        except EOFError:
            quitapp()
def main():
    while True:
        clear()
        print("BuckShot Auro Script")
        if lang == 1:
            try:
                clear()
                print("Syntax: \"Combat/Blank\"")
                user_input = input("*: ")
                parts = user_input.split('/')
                boevie = int(parts[0])
                holostie = int(parts[1])
                total = (boevie + holostie)
                print("Let's start the game!\n")
                print("Plus - combat\nMinus - blank\n")
                while total > 0:
                    user_input = input("Shot?: ")
                    clear()
                    if user_input == "+":
                        if boevie > 0:
                            boevie -= 1
                            total -= 1
                        elif boevie == 0:
                            print("The combat is gone!")
                        print(f"Combat: {boevie}\n Blank: {holostie}")
                    elif user_input == "-":
                        if holostie > 0:
                            holostie -= 1
                            total -= 1
                        elif holostie == 0:
                            print("The blanks are gone!")
                        print(f"Combat: {boevie}\n Blank: {holostie}")
                    else:
                        continue
                    if total > 0:
                        chance_b = round(boevie / total * 100, 1)
                        chance_h = round(holostie / total * 100, 1)
                        print(f"Combat chance: {chance_b}%")
                        print(f"Blank chance: {chance_h}%") 
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
        elif lang == 2:
            try:
                clear()
                print("Синтаксис: \"Боевые/Холостые\"")
                user_input = input("*: ")
                parts = user_input.split('/')
                boevie = int(parts[0])
                holostie = int(parts[1])
                total = (boevie + holostie)
                print("Начинаем игру!\n")
                print("Плюс - боевой\nМинус - холостой\n")
                while total > 0:
                    user_input = input("Выстрел?: ")
                    clear()
                    if user_input == "+":
                        if boevie > 0:
                            boevie -= 1
                            total -= 1
                        elif boevie == 0:
                            print("Боевых нет!")
                        print(f"Боевые: {boevie}\n Холостые: {holostie}")
                    elif user_input == "-":
                        if holostie > 0:
                            holostie -= 1
                            total -= 1
                        elif holostie == 0:
                            print("Холостых нет!")
                        print(f"Боевые: {boevie}\n Холостые: {holostie}")
                    else:
                        continue
                    if total > 0:
                        chance_b = round(boevie / total * 100, 1)
                        chance_h = round(holostie / total * 100, 1)
                        print(f"Шанс боевого: {chance_b}%")
                        print(f"Шанс холостого: {chance_h}%")
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
setup()
main()
