import hashlib, os


def hash_file(file_path: str) -> int:
    """
    Returns the images sha256 hash.
    """
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
