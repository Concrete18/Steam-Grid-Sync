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


# rich console
custom_theme = Theme(
    {
        "prim": "bold deep_sky_blue1",
        "sec": "bold pale_turquoise1",
        "pass": "bold green",
        "skip": "dim cyan",
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

    steam_id_3 = cfg.get("Settings", "STEAM_ID_3")
    custom_grid_path = cfg.get("Settings", "CUSTOM_GRID_PATH")
    steam_folder = cfg.get("Settings", "STEAM_FOLDER")

    if custom_grid_path:
        custom_grid_path = Path(custom_grid_path)
    steam_grid_path_override = cfg.get("Overrides", "STEAM_GRID_PATH")

    if steam_grid_path_override:
        steam_grid_path = Path(steam_grid_path_override)
    else:
        steam_grid_path = Path(f"{steam_folder}/userdata/{steam_id_3}/config/grid")

    def get_images(self) -> list[Image]:
        """
        Gets custom Steam Grid Image from Grid image path.
        """
        print("\nGetting Valid Images\n")

        valid_images = []
        for image_name in os.listdir(self.custom_grid_path):
            image_path = self.custom_grid_path / image_name
            steam_image = Image(image_path, self.steam_grid_path)

            if not steam_image.path.exists():
                msg = f"[warning]Missing[/] [sec]{steam_image.name}[/] does not exist - {steam_image.app_id}"
                console.print(msg)
                continue

            if steam_image.is_identical_to_destination():
                msg = f"[skip]Skipped[/] [sec]{steam_image.name}[/]'s {steam_image.type.upper()} image is identical - {steam_image.app_id}"
                console.print(msg)
                continue

            if steam_image:
                valid_images.append(steam_image)

        return valid_images

    def update_images(self, images_to_update: list[Image]):
        for img in images_to_update:
            try:
                img.update()
                msg = f"[pass]Replaced[/] [sec]{img.name}[/]'s {img.type.upper()} image - {img.app_id}"
            except PermissionError:
                msg = f"[danger]Failed[/] to update [sec]{img.name}[/]'s image - {img.app_id}"
            console.print(msg)

    def sync(self) -> None:
        """
        Syncs all the Steam Grid Images into the Grid folder.
        """
        console.print("Starting Steam Grid Sync", style="prim")

        if not self.steam_grid_path.exists():
            input("Can't run sync, Steam Grid Directory does not exist.")
            return

        images_to_update = self.get_images()

        if not images_to_update:
            console.print("\nNo updates needed\nSteam Grid Sync complete")
            return

        update_total = len(images_to_update)

        if update_total == 0:
            print("No images to update")
            return

        msg = f"\n{update_total} Image{' is' if update_total == 1 else 's are'} ready to be updated"

        if update_total <= 10:
            print(msg)
            for img in images_to_update:
                print(f"{img.name} - {img.type.upper()}")
        else:
            print(msg)

        input("\nPress Enter to start the update...\n")

        self.update_images(images_to_update)

        print("\nSteam Grid Sync Complete\nRestart Steam if you don't see changes")

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
        print(f"Opening Directory | {self.custom_grid_path}")
        subprocess.Popen(f'explorer "{self.custom_grid_path}"')

    def open_steam_grid_folder(self):
        print(f"Opening Directory | {self.steam_grid_path}")
        subprocess.Popen(f'explorer "{self.steam_grid_path}"')

    # TODO make a new option that will auto format games images in the custom grid image folder

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
        try:
            self.sync()
            self.game_library_actions()
        except EOFError or KeyboardInterrupt:
            pass


if __name__ == "__main__":

    grid = SteamGrid()
    grid.main()
