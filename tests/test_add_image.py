# standard library
from pathlib import Path

# local imports
from utils.add_image import *


class TestCreateFilename:

    def test_full_url(self):
        steam_url = "https://store.steampowered.com/app/1466640/Road_96/"

        print(steam_url)
        filename = create_filename(steam_url, "grid", ".png")
        assert filename == "Road 96_grid_1466640.png"

    def test_near_full_url(self):
        steam_url = "https://store.steampowered.com/app/1466640/Road_96"

        print(steam_url)
        filename = create_filename(steam_url, "grid", ".png")
        assert filename == "Road 96_grid_1466640.png"

    def test_valid_image(self, mocker):
        steam_url = "https://store.steampowered.com/app/1466640/"

        print(steam_url)
        mocker.patch("builtins.input", return_value="Road 96")
        filename = create_filename(steam_url, "grid", ".png")
        assert filename == "Road 96_grid_1466640.png"
