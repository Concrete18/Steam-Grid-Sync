# standard library
from dataclasses import dataclass, field, fields
from pathlib import Path
import shutil, os

# third-party imports
from rich.console import Console
from rich.theme import Theme

# local imports
from utils.utils import *

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


@dataclass
class Image:
    path: Path
    name: str = field(default_factory=str)
    type: str = field(default_factory=str)
    app_id: int = field(default_factory=int)

    def __post_init__(self):
        if isinstance(self.path, str):
            self.path = Path(self.path)

        image_parts = self.path.stem.split("_")

        if len(image_parts) != 3:
            print(f"\n{self.path.stem} is in wrong format")
            return {}

        self.name = image_parts[0]

        self.type = image_parts[1]

        self.app_id = int(image_parts[2])

    def __bool__(self):
        VALID_TYPES = ["hero", "logo", "grid", "active"]
        valid_type = self.type in VALID_TYPES
        return bool(self.name and valid_type and self.app_id and self.path.exists())

    def __eq__(self, other):
        if not self.path.exists() or not other.exists():
            return False
        return self.hash() == other.hash()

    def __repr__(self):  # pragma: no cover
        string = "Image("
        if self:
            for field in fields(self):
                string += f"\n  {field.name}: {getattr(self, field.name)}"
            string += "\n)"
        else:
            string = "Image(\n  Invalid\n)"
        return string

    def hash(self) -> int:
        """
        Returns the images sha256 hash.
        """
        return hash_file(self.path)

    def is_identical_to(self, image_path: Path | str) -> bool:
        """
        Determines if the current image is identical to another image at `image_path` based on their hash values.
        """
        if not image_path.exists():
            return False
        return self.hash() == hash_file(image_path)

    def exists(self) -> bool:
        """
        Whether this path exists.
        """
        return self.path.exists()

    def create_filename(self) -> Path:
        """
        Creates the new filename for the Steam Grid image so it
        is ready to be used by the Steam App.
        """
        match self.type:
            case "hero":
                filename = f"{self.app_id}_hero{self.path.suffix}"
            case "logo":
                filename = f"{self.app_id}_logo{self.path.suffix}"
            case "grid":
                filename = f"{self.app_id}p{self.path.suffix}"
            case "active":
                filename = f"{self.app_id}{self.path.suffix}"
            case _:
                return None
        return Path(filename)

    def backup(self, destination: str, steam_grid_path) -> None:
        """
        Backs up the current Steam Grid Image if it exists.
        """
        path, original_ext = os.path.splitext(destination)
        possible_file_exts = ["jpg", "png"]
        if original_ext not in possible_file_exts:
            possible_file_exts.append(original_ext)
        for file_ext in possible_file_exts:
            new_path = f"{path}.{file_ext}"
            if os.path.exists(new_path):
                backup_path = os.path.join(steam_grid_path, "originals")
                if os.path.exists(destination):
                    if not self.images_are_identical(new_path, destination):
                        shutil.move(new_path, backup_path)
                print(f"Backed up {new_path} to {backup_path}")
            else:
                print("Backup already exists")

    def update_steam_image(self, steam_grid_path):
        """
        Updates the Steam Grid Image if the it is not identical to the current image.
        """
        future_filename = self.create_filename()
        destination = steam_grid_path / future_filename

        if not self.path.exists() and not destination.parent.exists():
            return None

        if self.is_identical_to(destination):
            msg = f"[info]Skipped[/] [secondary]{self.name}[/]'s {self.type} identical image - {self.app_id}"
            console.print(msg)
            return False

        try:
            # self.backup(destination, steam_grid_path)
            # shutil.copyfile(self.path, destination)
            msg = f"[secondary]Replaced[/] [secondary]{self.name}[/]'s {self.type} image - {self.app_id}"
            console.print(msg)
        except PermissionError:
            msg = f"[danger]Failed[/] [secondary]{self.name}[/]'s image Update/Backup"
            console.print(msg)
            return None
        return True
