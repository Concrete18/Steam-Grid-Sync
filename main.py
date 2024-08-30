# standard library
import os, configparser
from pathlib import Path

# third-party imports
from rich.console import Console
from rich.theme import Theme

# local imports
from utils.utils import *
from utils.steam_image import Image
from utils.action_picker import ActionPicker

# rich console
custom_theme = Theme(
    {
        "prim": "bold deep_sky_blue1",
        "sec": "bold pale_turquoise1",
        "queue": "bold dark_green",
        "pass": "bold green",
        "skip": "dim cyan",
        # error
        "info": "dim cyan",
        "warning": "bold magenta",
        "danger": "bold red",
    }
)
console = Console(theme=custom_theme)


class SteamGrid(ActionPicker):

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

    @staticmethod
    def info_print(image: Image, action_type: str):
        """
        Prints formatted information about the image action status.
        """
        actions = {
            "queued": ("QUEUED", "queue", "image queued for update"),
            "updated": ("UPDATED", "pass", "image has been updated"),
            "skip": ("SKIPPED", "skip", "image has been skipped"),
            "missing": ("MISSING", "warning", "image does not exist"),
        }
        action, format_type, info = actions.get(
            action_type, ("FAILED", "danger", "image update failed")
        )

        msg = f"[{format_type}]{action.ljust(7)}[/] [sec]{image.name}[/]'s {image.type.upper()} {info} - {image.app_id}"
        console.print(msg)

    def info_print_tester(self):
        image_path = "tests/test_images/Hitman 3_grid_1659040.jpg"
        image = Image(image_path, self.steam_grid_path)
        self.info_print(image, "queued")
        self.info_print(image, "updated")
        self.info_print(image, "skip")
        self.info_print(image, "missing")
        self.info_print(image, "failure")

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
                self.info_print(steam_image, "missing")
                continue

            if steam_image.is_identical_to_destination():
                self.info_print(steam_image, "skip")
                continue

            if steam_image:
                valid_images.append(steam_image)

        return valid_images

    def update_images(self, images_to_update: list[Image]):
        for img in images_to_update:
            try:
                img.update()
                self.info_print(img, "updated")
            except PermissionError:
                self.info_print(img, "failure")

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
        msg = f"\n{update_total} Image{' is' if update_total == 1 else 's are'} queued for update\n"
        if update_total <= 10:
            print(msg)
            for img in images_to_update:
                self.info_print(img, "queued")
        else:
            print(msg)

        input("\nPress Enter to start the update\n")

        self.update_images(images_to_update)

        print("\nSteam Grid Sync Complete\nRestart Steam if you don't see changes")

    # TODO make a new option that will auto format games images in the custom grid image folder

    def game_library_actions(self) -> None:
        """
        Gives a choice of actions for the current game library.
        """
        open_custom_grid_folder = lambda: self.open_folder(self.custom_grid_path)
        open_steam_grid_folder = lambda: self.open_folder(self.steam_grid_path)
        choices = [
            ("Exit", exit),
            ("Open Custom Grid Image Folder", open_custom_grid_folder),
            ("Open Steam Grid Image Folder", open_steam_grid_folder),
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
