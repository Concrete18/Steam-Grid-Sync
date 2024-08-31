# standard library
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog

# third-party imports
from pick import pick

# local imports
from utils.action_picker import advanced_picker


def get_file_path() -> Path:
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a file")
    return Path(file_path)


def create_filename(steam_url: str, image_type: str, suffix: str) -> str:
    """
    ph
    """
    url_parts = steam_url.split("/")
    game_name = url_parts[5]
    if game_name:
        game_name = game_name.replace("_", " ").title()
    else:
        game_name = input("What is the game's name?")
    app_id = url_parts[4]
    print(f"\nName: {game_name}\nApp ID: {app_id}")
    return f"{game_name}_{image_type}_{app_id}{suffix}"


def add_image(custom_grid_image_dir: Path) -> None:
    """
    ph
    """
    target = get_file_path()
    steam_url = input("\nWhat is the Steam Game URL?\n")

    IMAGE_TYPES = ["Grid", "Hero", "Logo", "Active"]
    index = pick(
        IMAGE_TYPES,
        "What type of Steam Grid image is this image?",
        indicator="->",
    )[1]

    filename = create_filename(steam_url, IMAGE_TYPES[index].lower(), target.suffix)
    destination = custom_grid_image_dir / filename

    shutil.move(target, destination)
    print("\nNew Steam Grid Image Added")
