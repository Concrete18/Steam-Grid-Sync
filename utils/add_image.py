# standard library
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog

# third-party imports
from PIL import Image


def get_file_paths() -> list[Path]:
    """
    ph
    """
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfiles(title="Select a file")

    paths = []
    for file in files:
        if file.name == ".":
            continue
        path = Path(file.name)
        paths.append(path)
    return paths


def get_steam_image_type(image_path):
    """
    Gets the type of image for customizaing Steam game images.
    """
    with Image.open(image_path) as img:
        width, height = img.size
    res = f"{width} x {height}"
    types = {
        "1920 x 620": "hero",
        "920 x 430": "active",
        "600 x 900": "grid",
    }
    image_type = types.get(res, "logo")
    return image_type


def create_filename(steam_url: str, image_type: str, suffix: str) -> str:
    """
    Creates the new filename for a steam grid image.
    """
    # TODO swap to using regex
    url_parts = steam_url.split("/")
    if len(url_parts) > 5:
        game_name = url_parts[5].replace("_", " ").title()
    else:
        game_name = input("What is the game's name?\n")
    game_name = game_name.replace("_", " ")
    app_id = url_parts[4]
    return f"{game_name}_{image_type}_{app_id}{suffix}"


def move_image(
    image_path: Path,
    final_filename: str,
    custom_grid_image_dir: Path,
) -> None:
    """
    Moves the image to the grid image directory so it can be
    used to update Steam customization.
    """
    destination = custom_grid_image_dir / final_filename
    if destination.exists():
        # TODO add input to ask if it should be replaced
        print(f"{final_filename} image already exists.")
        return
    shutil.move(image_path, destination)


def add_images(custom_grid_image_dir: Path, image_paths=[]) -> None:
    """
    ph
    """
    if not image_paths:
        image_paths = get_file_paths()
        if not image_paths:
            return

    steam_url = input("\nWhat is the Steam Game URL?\n")
    for image_path in image_paths:
        image_type = get_steam_image_type(image_path)
        final_filename = create_filename(steam_url, image_type, image_path.suffix)
        move_image(image_path, final_filename, custom_grid_image_dir)

    print("\nNew Steam Grid Image Added")
