# standard library
from dataclasses import dataclass, field, fields
from pathlib import Path
import hashlib


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
        return bool(self.name and self.type and self.app_id and self.path)

    def __eq__(self, other):
        if not self.path.exists() or not other.exist():
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
        with self.path.open("rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def exists(self):
        """
        Whether this path exists.
        """
        return self.path.exists()

    def create_filename(self) -> "Image":
        """
        ph
        """
        match self.type:
            case "hero":
                filename = f"{self.app_id}_hero{self.path.suffix}"
            case "logo":
                filename = f"{self.app_id}_logo{self.path.suffix}"
            case "grid":
                filename = f"{self.app_id}p{self.path.suffix}"
            case _:
                filename = f"{self.app_id}{self.path.suffix}"
        return Path(filename)


if __name__ == "__main__":
    path = Path("tests/test_images/Team Fortress 2_grid_440.png")
    grid_image = Image(path=path)

    print(grid_image)

    hash = grid_image.hash()
    print(hash)

    future_path = grid_image.create_filename()
    print(future_path)
