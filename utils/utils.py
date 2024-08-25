# standard library
import hashlib


def hash_image(path: str) -> int:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
