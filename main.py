# standard library
import os, sys, subprocess, configparser
from pathlib import Path

# third-party imports
from rich.console import Console
from rich.theme import Theme
from pick import pick

# local imports
from utils.utils import *
from utils.steam_image import Image


# rich console
custom_theme = Theme(
    {
        "primary": "bold deep_sky_blue1",
        "secondary": "bold pale_turquoise1",
        # error
        "info": "dim cyan",
        "warning": "bold magenta",
        "danger": "bold red",
    }
)
console = Console(theme=custom_theme)


class SteamGrid:

    cfg = configparser.ConfigParser()
    cfg.read("config.ini")

    STEAM_ID_3 = cfg.get("Settings", "STEAM_ID_3")
    GRID_IMAGE_PATH = cfg.get("Settings", "GRID_IMAGE_PATH")
    if GRID_IMAGE_PATH:
        GRID_IMAGE_PATH = Path(GRID_IMAGE_PATH)
    STEAM_PATH_OVERRIDE = cfg.get("Overrides", "STEAM_PATH")

    if STEAM_PATH_OVERRIDE:
        steam_grid_path = Path(STEAM_PATH_OVERRIDE)
    else:
        steam_grid_path = Path(
            f"C:/Program Files (x86)/Steam/userdata/{STEAM_ID_3}/config/grid"
        )

    def get_images(self) -> list[Image]:
        """
        Gets custom Steam Grid Image from Grid image path.
        """
        print("\nGetting Images")

        image_dicts = []
        for image_path in os.listdir(self.GRID_IMAGE_PATH):
            steam_image = Image(self.GRID_IMAGE_PATH / image_path)
            if steam_image:
                image_dicts.append(steam_image)
            else:
                continue
        print(f"{len(image_dicts)} Valid Images Found\n")
        return image_dicts

    def sync(self):
        """
        Syncs all the Steam Grid Images into the Grid folder.
        """
        console.print("Starting Steam Grid Sync", style="primary")

        valid_images = self.get_images()

        if not self.steam_grid_path.exists():
            input("Can't run sync, Steam Grid Directory does not exist.")
            return

        failures = 0
        for img in valid_images:
            if img:
                success = img.update_steam_image(self.steam_grid_path)
                if not success:
                    failures += 1
            else:
                failures += 1
        if failures:
            msg = f"\nImages failed to Update/Backup {failures} times\nTry closing Steam and try again"
            print(msg)

        print("\nSteam Grid Sync Complete\nRestart Steam to see changes")

    @staticmethod
    def advanced_picker(choices: list[tuple], prompt: str) -> list:
        """
        Choice picker using the advanced and less compatible Pick module.
        """
        options = [choice[0] for choice in choices]
        selected_index = pick(options, prompt, indicator="->")[1]
        return choices[selected_index]

    def pick_task(self, choices: list[tuple], repeat: bool = True) -> None:
        """
        Allows picking a task using Arrow Keys and Enter.
        """
        if not sys.stdout.isatty():
            # runs if it is not an interactable terminal
            print("\nSkipping Task Picker.\nInput can't be used")
            return
        input("\nPress Enter to Pick Next Action:")
        PROMPT = "What do you want to do? (Use Arrow Keys and Enter):"
        selected = self.advanced_picker(choices, PROMPT)
        if selected:
            name, func = selected[0], selected[1]
            msg = f"\n[b underline]{name}[/] Selected"
            console.print(msg, highlight=False)
            func()
            if "exit" in name.lower():
                return
            if repeat:
                self.pick_task(choices, repeat)

    def open_custom_grid_folder(self):
        print(f"Opening Directory | {self.GRID_IMAGE_PATH}")
        subprocess.Popen(f'explorer "{self.GRID_IMAGE_PATH}"')

    def open_steam_grid_folder(self):
        print(f"Opening Directory | {self.steam_grid_path}")
        subprocess.Popen(f'explorer "{self.steam_grid_path}"')

    def game_library_actions(self) -> None:
        """
        Gives a choice of actions for the current game library.
        """
        choices = [
            ("Exit", exit),
            ("Open Custom Grid Image Folder", self.open_custom_grid_folder),
            ("Open Steam Grid Image Folder", self.open_steam_grid_folder),
        ]
        self.pick_task(choices)
        exit()

    def main(self):
        self.sync()
        self.game_library_actions()


if __name__ == "__main__":

    grid = SteamGrid()
    grid.main()
