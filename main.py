import os, shutil, hashlib


class SteamGrid:

    steam_id_3 = 22360464

    STEAM_PATH = f"C:/Program Files (x86)/Steam/userdata/{steam_id_3}/config/grid"

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
        image_path = "test_images"
        image_dicts = []
        for image_filename in os.listdir(image_path):
            image_parts = image_filename.split("_")
            if len(image_parts) != 3:
                print(f"\n{image_filename} is in wrong format")
                continue
            image_dicts.append(
                {
                    "name": image_parts[0],
                    "app_id": int(image_parts[1]),
                    "type": image_parts[2].split(".")[0],
                    "path": os.path.join("test_images", image_filename),
                }
            )

        return image_dicts

    def create_dest_path(self, app_id: int, image_type: str) -> str:
        """
        ph
        """
        match image_type:
            case "hero":
                dest_path = os.path.join(self.STEAM_PATH, f"{app_id}_hero.jpg")
            case "logo":
                dest_path = os.path.join(self.STEAM_PATH, f"{app_id}_logo.jpg")
            case "grid":
                dest_path = os.path.join(self.STEAM_PATH, f"{app_id}p.jpg")
            case _:
                dest_path = os.path.join(self.STEAM_PATH, f"{app_id}.jpg")
        return dest_path

    @staticmethod
    def hash_image(path: str) -> int:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def images_are_identical(self, image1, image2):
        """
        Compares images by hash
        """
        image1_hash = self.hash_image(image1)
        image2_hash = self.hash_image(image2)
        # print(f"{new_image_hash}\n{dest_hash}")
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

    def change_steam_hero_image(self, app_id, image_path, image_type):
        dest_path = self.create_dest_path(app_id, image_type)

        # hash check
        dest_exists = os.path.exists(dest_path)
        new_image_exists = os.path.exists(image_path)
        if not dest_exists and not new_image_exists:
            return

        if self.images_are_identical(image_path, dest_path):
            print(f"Skipped {app_id}'s {image_type} image as it is identical")
            return

        # backup the old image
        backup_path = os.path.join(self.STEAM_PATH, "originals")
        # shutil.copyfile(dest_path, backup_path)

        # shutil.copyfile(image_path, dest_path)
        print(f"Replaced {app_id}'s {image_type} image")

    def sync(self):
        """
        ph
        """
        print("Starting Steam Grid Sync")
        VALID_TYPES = ["hero", "logo", "grid", "active"]
        for image in self.get_images():
            print(f"\n{image['name']}")
            if image["type"] not in VALID_TYPES:
                print(f"Type is invalid for {image}")
                continue
            print(
                f"Changing {image['name']}'s {image['type']} image to {image['path']}"
            )
            self.change_steam_hero_image(
                app_id=image["app_id"],
                image_path=image["path"],
                image_type=image["type"],
            )


if __name__ == "__main__":
    grid = SteamGrid()
    grid.sync()
