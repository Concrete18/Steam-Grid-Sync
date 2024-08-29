# standard library
from pathlib import Path

# local imports
from utils.steam_image import Image

DESTINATION = "tests/test_destination"


class TestImage:

    def test_valid_image(self):
        test_path = "tests/test_images/Hitman 3_grid_1659040.jpg"
        grid_image = Image(test_path, DESTINATION)

        assert grid_image.name == "Hitman 3"
        assert grid_image.type == "grid"
        assert grid_image.app_id == 1659040
        assert grid_image.path == Path(test_path)
        assert grid_image.destination == Path("tests/test_destination/1659040p.jpg")
        assert grid_image

    # TODO create

    # def test_create_grid(self):
    #     test_path = "tests/test_images/Hitman 3_grid_1659040.jpg"
    #     grid_image = Image(test_path, DESTINATION)

    #     new_filename = grid_image.create_filename()
    #     assert grid_image.create_filename() == Path("1659040p.jpg")
    #     assert isinstance(new_filename, Path)

    #     destination = "tests/test_images/" / new_filename
    #     assert isinstance(destination, Path)

    # def test_create_hero(self):
    #     test_path = "tests/test_images/Hitman 3_hero_1659040.jpg"
    #     grid_image = Image(test_path, DESTINATION)

    #     assert grid_image.create_filename() == Path("1659040_hero.jpg")

    # def test_create_logo(self):
    #     test_path = "tests/test_images/Hitman 3_logo_1659040.jpg"
    #     grid_image = Image(test_path, DESTINATION)

    #     assert grid_image.create_filename() == Path("1659040_logo.jpg")

    # def test_create_active(self):
    #     test_path = "tests/test_images/Hitman 3_active_1659040.jpg"
    #     grid_image = Image(test_path, DESTINATION)

    #     assert grid_image.create_filename() == Path("1659040.jpg")


class TestIsIdenticalTo:

    def test_is_identical(self):
        test_path = "tests/test_images/Hitman 3_grid_1659040.jpg"
        grid_image = Image(test_path, DESTINATION)

        assert grid_image.is_identical_to_destination()

    def test_is_not_identical(self):
        test_path = "tests/test_images/Hitman 3_test_1659040.jpg"
        grid_image = Image(test_path, DESTINATION)

        grid_image.destination = Path("tests/test_destination/1659040_hero.jpg")
        assert not grid_image.is_identical_to_destination()


class TestEQ:

    def test_eq(self):
        # same one is identical to itself
        test_path1 = "tests/test_images/Hitman 3_grid_1659040.jpg"
        grid_image1 = Image(test_path1, DESTINATION)
        assert grid_image1 == grid_image1

        # two different ones are not identical
        test_path2 = "tests/test_images/The Beginner's Guide_grid_303210.jpg"
        grid_image2 = Image(test_path2, DESTINATION)
        assert grid_image1 != grid_image2


class TestHash:

    def test_hash(self):
        test_path = "tests/test_images/Hitman 3_grid_1659040.jpg"
        grid_image = Image(test_path, DESTINATION)

        image_hash = "91e3e8539eba9eebb32f77e243b01f1989f67623c86386cf0bfe43e3d00c3f3b"
        assert grid_image.hash() == image_hash


class TestExists:

    def test_exists(self):
        test_path = "tests/test_images/Hitman 3_grid_1659040.jpg"
        grid_image = Image(test_path, DESTINATION)

        assert grid_image.exists()

    def test_does_not_exists(self):
        test_path = "tests/test_images/Hitman 47_grid_1659040.jpg"
        grid_image = Image(test_path, DESTINATION)

        assert not grid_image.exists()
