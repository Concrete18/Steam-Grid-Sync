# standard library
from pathlib import Path
import hashlib, os


def hash_file(file_path: Path) -> str:
    """
    Returns the images sha256 hash.
    """
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def yes_or_no(msg=""):
    """
    Asks for user input and will return True if user inputs any for of yes.
    """
    response = input(msg)
    return response.lower() in ["yes", "y", "yeah"]
