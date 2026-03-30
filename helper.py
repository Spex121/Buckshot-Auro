import os
import subprocess
import sys
import shutil
from rich import console

console = Console()


def update_file():
    try:
        temp_filename = sys.argv[1]
        console.print("[yellow]Updating...[/yellow]")
        if os.name == "nt":
            main_filename = "auro.exe"
        else:
            main_filename = "auro"
        shutil.move(temp_filename, main_filename)
        console.print("[green]Done[/green]")
        if os.name != "nt":
            os.chmod(main_filename, 0o755)
        if os.name == "nt":
            subprocess.Popen([main_filename])
        else:
            subprocess.Popen([f"./{main_filename}"])
        console.print("[yellow]STARTING[/yellow]")
    except KeyboardInterrupt, EOFError:
        pass


if __name__ == "__main__":
    update_file()
