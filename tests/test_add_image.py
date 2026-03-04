# standard library
from pathlib import Path

# local imports
from utils.add_image import *


class TestCreateFilename:

    def test_full_url(self):
        steam_url = "https://store.steampowered.com/app/1466640/Road_96/"
        filename = create_filename(steam_url, "grid", ".png")
        assert filename == "Road 96_grid_1466640.png"

    def test_near_full_url(self):
        steam_url = "https://store.steampowered.com/app/1466640/Road_96"
        filename = create_filename(steam_url, "grid", ".png")
        assert filename == "Road 96_grid_1466640.png"

    def test_no_name_in_url(self, mocker):
        steam_url = "https://store.steampowered.com/app/1466640"
        mocker.patch("builtins.input", return_value="Road 96")
        filename = create_filename(steam_url, "grid", ".png")
        assert filename == "Road 96_grid_1466640.png"


class TestGetImageType:

    def test_active(self):
        image_path = "tests/test_images/Cyberpunk 2077_active_1091500.png"
        image_type = get_steam_image_type(image_path)
        assert image_type == "active"

    def test_grid(self):
        image_path = "tests/test_images/Cyberpunk 2077_grid_1091500.png"
        image_type = get_steam_image_type(image_path)
        assert image_type == "grid"

    def test_hero(self):
        image_path = "tests/test_images/Cyberpunk 2077_hero_1091500.png"
        image_type = get_steam_image_type(image_path)
        assert image_type == "hero"

    def test_logo(self):
        image_path = "tests/test_images/Cyberpunk 2077_logo_1091500.png"
        image_type = get_steam_image_type(image_path)
        assert image_type == "logo"
