# standard library
import os, shutil, configparser

# third-party imports
from rich.console import Console
from rich.theme import Theme

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
        Compares images by hash
        """
        if not os.path.exists(image1) or not os.path.exists(image2):
            return False
        image1_hash = hash_image(image1)
        image2_hash = hash_image(image2)
        return image1_hash == image2_hash

    def backup_old_image(self, dest_path):
        """
        ph
        """
        backup_path = os.path.join(self.STEAM_PATH, "originals")
        if os.path.exists(backup_path):
            if self.images_are_identical(backup_path, dest_path):
                return

        shutil.copyfile(dest_path, backup_path)

    def change_steam_hero_image(self, image):
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
            return

        if self.images_are_identical(image_path, dest_path):
            msg = f"[info]Skipped[/] [secondary]{name}[/]'s {image_type} image as it is identical - {app_id}"
            self.console.print(msg)
            return

        try:
            # backup the old image
            if os.path.exists(dest_path):
                backup_path = os.path.join(self.STEAM_PATH, "originals")
                shutil.move(dest_path, backup_path)

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

        input("\nSteam Grid Sync Complete\nRestart Steam to see changes")

        # TODO delete unisted images


if __name__ == "__main__":
    grid = SteamGrid()
    grid.sync()
