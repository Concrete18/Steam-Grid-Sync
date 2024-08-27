# standard library
import os, sys, shutil, subprocess, configparser
from pathlib import Path

# third-party imports
from rich.console import Console
from rich.theme import Theme

from pick import pick

# local imports
from utils.utils import *
from utils.steam_image import Image


class SteamGrid:

    cfg = configparser.ConfigParser()
    cfg.read("config.ini")

    STEAM_ID_3 = cfg.get("Settings", "STEAM_ID_3")
    GRID_IMAGE_PATH = cfg.get("Settings", "GRID_IMAGE_PATH")
    if GRID_IMAGE_PATH:
        GRID_IMAGE_PATH = Path(GRID_IMAGE_PATH)
    STEAM_PATH_OVERRIDE = cfg.get("Overrides", "STEAM_PATH")

    if STEAM_PATH_OVERRIDE:
        STEAM_PATH = Path(STEAM_PATH_OVERRIDE)
    else:
        STEAM_PATH = Path(
            f"C:/Program Files (x86)/Steam/userdata/{STEAM_ID_3}/config/grid"
        )

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

    def verify_steam_paths(self):
        """
        ph
        """
        return os.path.exists(self.STEAM_PATH)

    def get_images(self) -> list[dict[str, int, str, str]]:
        """
        ph
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

    def backup(self, dest_path: str) -> None:
        """
        ph
        """
        path, original_ext = os.path.splitext(dest_path)
        possible_file_exts = ["jpg", "png"]
        if original_ext not in possible_file_exts:
            possible_file_exts.append(original_ext)
        for file_ext in possible_file_exts:
            new_path = f"{path}.{file_ext}"
            if os.path.exists(new_path):
                backup_path = os.path.join(self.STEAM_PATH, "originals")
                if os.path.exists(dest_path):
                    if not self.images_are_identical(new_path, dest_path):
                        shutil.move(new_path, backup_path)
                print(f"Backed up {new_path} to {backup_path}")
            else:
                print("Backup already exists")

    def change_steam_hero_image(self, steam_image: Image):
        """
        ph
        """
        future_filename = steam_image.create_filename()
        future_destination = self.STEAM_PATH / future_filename

        if not steam_image.path.exists() and not future_filename.exists():
            return False

        if steam_image.hash() == hash_image(future_destination):
            msg = f"[info]Skipped[/] [secondary]{steam_image.name}[/]'s {steam_image.type} identical image - {steam_image.app_id}"
            self.console.print(msg)
            return True

        try:
            # TODO uncomment
            # image_destination = self.STEAM_PATH / future_filename
            # self.backup(image_destination)
            # shutil.copyfile(steam_image.path, image_destination)
            msg = f"[secondary]Replaced[/] [secondary]{steam_image.name}[/]'s {steam_image.type} image - {steam_image.app_id}"
            self.console.print(msg)
        except PermissionError:
            msg = f"[danger]Failed[/] [secondary]{steam_image.name}[/]'s image Update/Backup"
            self.console.print(msg)
            return False
        return True

    def sync(self):
        """
        ph
        """
        self.console.print("Starting Steam Grid Sync", style="primary")

        valid_images = self.get_images()

        failures = 0
        for img in valid_images:
            success = self.change_steam_hero_image(img)
            if not success:
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
            self.console.print(msg, highlight=False)
            func()
            if "exit" in name.lower():
                return
            if repeat:
                self.pick_task(choices, repeat)

    def open_custom_grid_folder(self):
        print(f"Opening Directory | {self.GRID_IMAGE_PATH}")
        subprocess.Popen(f'explorer "{self.GRID_IMAGE_PATH}"')

    def open_steam_grid_folder(self):
        print(f"Opening Directory | {self.STEAM_PATH}")
        subprocess.Popen(f'explorer "{self.STEAM_PATH}"')

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
