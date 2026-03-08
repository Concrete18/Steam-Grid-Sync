# standard library
from dataclasses import dataclass, field, fields
from pathlib import Path
from functools import cached_property
import shutil

# local imports
from utils.utils import hash_file


VALID_TYPES = frozenset({"hero", "logo", "grid", "active"})

TYPE_TO_FILENAME = {
    "hero": lambda app_id, suffix: f"{app_id}_hero{suffix}",
    "logo": lambda app_id, suffix: f"{app_id}_logo{suffix}",
    "grid": lambda app_id, suffix: f"{app_id}p{suffix}",
    "active": lambda app_id, suffix: f"{app_id}{suffix}",
}


@dataclass
class SteamImage:
    path: Path
    steam_grid_path: Path
    name: str = field(default="")
    type: str = field(default="")
    app_id: int = field(default=0)
    destination: Path | None = field(default=None)

    def __post_init__(self):
        self.path = Path(self.path)
        self.steam_grid_path = Path(self.steam_grid_path)

        parts = self.path.stem.split("_")
        if len(parts) != 3:
            self.name = self.path.stem
            self.type = "unknown"
            return

        self.name, self.type, raw_id = parts
        try:
            self.app_id = int(raw_id)
        except ValueError:
            self.type = "unknown"
            return

        self.destination = self._build_destination()

    def __bool__(self) -> bool:
        return (
            self.type in VALID_TYPES
            and bool(self.name)
            and bool(self.app_id)
            and self.path.exists()
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SteamImage):
            return NotImplemented
        if not self.path.exists() or not other.path.exists():
            return False
        return self.digest == other.digest

    def __repr__(self) -> str:  # pragma: no cover
        if not self:
            return "SteamImage(\n  Invalid\n)"
        field_lines = "\n".join(
            f"  {f.name}: {getattr(self, f.name)}" for f in fields(self)
        )
        return f"SteamImage(\n{field_lines}\n)"

    def _build_destination(self) -> Path | None:
        """Return the resolved destination path in the Steam grid folder, or None for unknown types."""
        formatter = TYPE_TO_FILENAME.get(self.type)
        if formatter is None:
            return None
        return self.steam_grid_path / formatter(self.app_id, self.path.suffix)

    @cached_property
    def digest(self) -> str:
        """SHA-256 hash of the source image (cached after first read)."""
        return hash_file(self.path)

    def is_identical_to_destination(self) -> bool:
        """Return True if the source file is byte-for-byte identical to the destination."""
        if self.destination is None or not self.destination.exists():
            return False
        return self.digest == hash_file(self.destination)

    def exists(self) -> bool:
        """Return True if the source image file exists on disk."""
        return self.path.exists()

    def update(self) -> None:
        """
        Replace any existing Steam grid files for this image and copy the source into place.
        Removes all files sharing the destination stem (to handle extension changes).
        """
        if not self or self.destination is None:
            raise ValueError(f"Cannot update an invalid SteamImage: {self!r}")

        for stale_image in self.steam_grid_path.glob(f"{self.destination.stem}.*"):
            stale_image.unlink(missing_ok=True)

        shutil.copyfile(self.path, self.destination)
