# standard library
from dataclasses import dataclass, field, fields
from pathlib import Path

# local imports
from utils.utils import *


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
        VALID_TYPES = ["hero", "logo", "grid", "active"]
        if self.type not in VALID_TYPES:
            print(f"Type is invalid for {self.path.stem}")

        self.app_id = int(image_parts[2])

    def __bool__(self):
        return bool(self.name and self.type and self.app_id and self.path.exists())

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
        return hash_image(self.path)

    def is_identical_to(self, image_path: Path | str) -> bool:
        """
        Determines if the current image is identical to another image at `image_path` based on their hash values.
        """
        return self.hash() == hash_image(image_path)

    def exists(self) -> bool:
        """
        Whether this path exists.
        """
        return self.path.exists()

    def create_filename(self) -> Path:
        """
        Creates the new filename for the Steam image so it
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
