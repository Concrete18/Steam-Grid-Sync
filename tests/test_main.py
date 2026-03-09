# standard library
from pathlib import Path

# local imports
from main import SteamGrid

DESTINATION = Path("tests/test_destination")


class TestUpdateImages:

    def test_new_image(self):
        updated = SteamGrid().update_images([])
        assert updated == 0
