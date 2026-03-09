# standard library
from pathlib import Path

# local imports
from utils.steam_image import SteamImage
from utils.add_image import *

DESTINATION = Path("tests/test_destination")


class TestImage:

    def test_valid_image(self):
        test_path = Path("tests/test_images/Hitman 3_grid_1659040.jpg")
        grid_image = SteamImage(test_path, DESTINATION)

        assert grid_image.name == "Hitman 3"
        assert grid_image.type == "grid"
        assert grid_image.app_id == 1659040
        assert grid_image.path == Path(test_path)
        assert grid_image.destination == Path("tests/test_destination/1659040p.jpg")
        assert grid_image


class TestIsIdenticalTo:

    def test_is_identical(self):
        test_path = Path("tests/test_images/Hitman 3_grid_1659040.jpg")
        grid_image = SteamImage(test_path, DESTINATION)

        assert grid_image.is_identical_to_destination()

    def test_is_not_identical(self):
        test_path = Path("tests/test_images/Hitman 3_test_1659040.jpg")
        grid_image = SteamImage(test_path, DESTINATION)

        grid_image.destination = Path("tests/test_destination/1659040_hero.jpg")
        assert not grid_image.is_identical_to_destination()


class TestEQ:

    def test_eq(self):
        # same one is identical to itself
        test_path1 = Path("tests/test_images/Hitman 3_grid_1659040.jpg")
        grid_image1 = SteamImage(test_path1, DESTINATION)
        assert grid_image1 == grid_image1

        # two different ones are not identical
        test_path2 = Path("tests/test_images/The Beginner's Guide_grid_303210.jpg")
        grid_image2 = SteamImage(test_path2, DESTINATION)
        assert grid_image1 != grid_image2


class TestHash:

    def test_hash(self):
        test_path = Path("tests/test_images/Hitman 3_grid_1659040.jpg")
        grid_image = SteamImage(test_path, DESTINATION)

        image_hash = "91e3e8539eba9eebb32f77e243b01f1989f67623c86386cf0bfe43e3d00c3f3b"
        assert grid_image.digest == image_hash


class TestExists:

    def test_exists(self):
        test_path = Path("tests/test_images/Hitman 3_grid_1659040.jpg")
        grid_image = SteamImage(test_path, DESTINATION)

        assert grid_image.exists()

    def test_does_not_exists(self):
        test_path = Path("tests/test_images/Hitman 47_grid_1659040.jpg")
        grid_image = SteamImage(test_path, DESTINATION)

        assert not grid_image.exists()
