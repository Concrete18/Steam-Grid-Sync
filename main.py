# standard library
import os, sys, shutil, subprocess, configparser

# third-party imports
from rich.console import Console
from rich.theme import Theme
from PIL import Image
from pick import pick

# local imports
from utils.utils import *


class SteamGrid:

    cfg = configparser.ConfigParser()
    cfg.read("config.ini")

    STEAM_ID_3 = cfg.get("Settings", "STEAM_ID_3")
    GRID_IMAGE_PATH = cfg.get("Settings", "GRID_IMAGE_PATH")
    STEAM_PATH_OVERRIDE = cfg.get("Overrides", "STEAM_PATH")

    if STEAM_PATH_OVERRIDE:
        STEAM_PATH = STEAM_PATH_OVERRIDE
    else:
        STEAM_PATH = f"C:/Program Files (x86)/Steam/userdata/{STEAM_ID_3}/config/grid"

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

    def get_image_type(filepath):
        """
        ph
        """
        # TODO finish get_image_type
        img = Image.open(filepath)
        width = img.width
        height = img.height

        if width == 600 and height == 900:
            return "grid"
        elif width == 600 and height == 900:
            return "grid"

    def get_image_data(self, image_filename):
        """
        ph
        """
        image_parts = image_filename.split(".")[0].split("_")

        if len(image_parts) != 3:
            print(f"\n{image_filename} is in wrong format")
            return {}

        name = image_parts[0]
        if not isinstance(name, str):
            return {}

        type = image_parts[1]
        VALID_TYPES = ["hero", "logo", "grid", "active"]
        if type not in VALID_TYPES:
            print(f"Type is invalid for {image_filename}")
            return {}

        app_id = int(image_parts[2])
        # TODO validate app_id

        path = os.path.join(self.GRID_IMAGE_PATH, image_filename)

        return {
            "name": name,
            "type": type,
            "app_id": app_id,
            "path": path,
        }

    def get_images(self) -> list[dict[str, int, str, str]]:
        """
        ph
        """
        print("\nGetting Images")

        image_dicts = []
        for image_filename in os.listdir(self.GRID_IMAGE_PATH):
            image_data = self.get_image_data(image_filename)
            if image_data:
                image_dicts.append(image_data)
            else:
                continue
        print(f"{len(image_dicts)} Valid Images Found\n")
        return image_dicts

    def create_dest_path(self, app_id: int, image_type: str, filetype: str) -> str:
        """
        ph
        """
        match image_type:
            case "hero":
                dest_path = os.path.join(self.STEAM_PATH, f"{app_id}_hero.{filetype}")
            case "logo":
                dest_path = os.path.join(self.STEAM_PATH, f"{app_id}_logo.{filetype}")
            case "grid":
                dest_path = os.path.join(self.STEAM_PATH, f"{app_id}p.{filetype}")
            case _:
                dest_path = os.path.join(self.STEAM_PATH, f"{app_id}.{filetype}")
        return dest_path

    def images_are_identical(self, image1, image2):
        """
        Compares images by hash.
        """
        if not os.path.exists(image1) or not os.path.exists(image2):
            return False
        image1_hash = hash_image(image1)
        image2_hash = hash_image(image2)
        return image1_hash == image2_hash

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

    def change_steam_hero_image(self, image: dict[str, int, str, str]):
        name = image["name"]
        app_id = image["app_id"]
        image_path = image["path"]
        image_type = image["type"]
        filetype = image_path.split(".")[-1]

        dest_path = self.create_dest_path(app_id, image_type, filetype)

        # hash check
        dest_exists = os.path.exists(dest_path)
        new_image_exists = os.path.exists(image_path)
        if not dest_exists and not new_image_exists:
            return False

        if self.images_are_identical(image_path, dest_path):
            msg = f"[info]Skipped[/] [secondary]{name}[/]'s {image_type} image as it is identical - {app_id}"
            self.console.print(msg)
            return True

        try:
            # backup the old image
            self.backup(dest_path)

            shutil.copyfile(image_path, dest_path)
            msg = f"[secondary]Replaced[/] [secondary]{name}[/]'s {image_type} image - {app_id}"
            self.console.print(msg)
        except PermissionError:
            msg = f"[danger]Failed[/] [secondary]{name}[/]'s image Update/Backup"
            self.console.print(msg)
            return False
        return True

    def sync(self):
        """
        ph
        """
        self.console.print("Starting Steam Grid Sync", style="primary")

        valid_iamges = self.get_images()

        failures = 0
        for img in valid_iamges:
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
