# standard library
from dataclasses import dataclass, field, fields
from pathlib import Path
import shutil

# local imports
from utils.utils import *


@dataclass
class Image:
    path: Path
    steam_grid_path: Path
    name: str = field(default_factory=str)
    type: str = field(default_factory=str)
    app_id: int = field(default_factory=int)
    destination: Path = field(default_factory=Path)

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
        self.destination = self.create_destination()

    def __bool__(self):
        VALID_TYPES = ["hero", "logo", "grid", "active"]
        if not self.type in VALID_TYPES:
            return False

        must_be_truthy = [self.name, self.app_id, self.path]
        return all(must_be_truthy)

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

    def create_destination(self) -> Path:
        """
        Creates the new filename for the Steam Grid image so it is ready to be used by the Steam App.
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
        return self.steam_grid_path / Path(filename)

    def hash(self) -> int:
        """
        Returns the images sha256 hash.
        """
        return hash_file(self.path)

    def is_identical_to_destination(self) -> bool:
        """
        Determines if the current image is identical to another image at `image_path` based on their hash values.
        """
        return self.hash() == hash_file(self.destination)

    def exists(self) -> bool:
        """
        Whether this path exists.
        """
        return self.path.exists()

    def update(self):
        """
        Deletes the current Steam Grid Image and copies the new one to that location.
        """
        # deletes the any files that need to be replaced
        paths = Path(self.steam_grid_path).glob(f"{self.destination.stem}.*")
        for path in paths:
            path.unlink(missing_ok=True)

        shutil.copyfile(self.path, self.destination)
