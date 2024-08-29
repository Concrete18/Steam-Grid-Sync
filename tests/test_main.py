# local imports
from main import SteamGrid
from utils.steam_image import Image


# class TestUpdateImages:

#     def test_new_image(self, mocker):

#         test_path = "tests/test_images/Hitman 3_hero_1659040.jpg"
#         steam_image = Image(test_path, DESTINATION)

#         mocker.patch("shutil.copyfile", return_value=None)
#         mocker.patch("utils.steam_image.Image.backup", return_value=None)
#         steam_grid_path = "tests/test_destination"
#         success = steam_image.update_steam_image(steam_grid_path)
#         assert success

#     def test_replace_image(self, mocker):

#         test_path = "tests/test_images/Hitman 3_hero_1659040.jpg"
#         steam_image = Image(test_path, DESTINATION)

#         mocker.patch("shutil.copyfile", return_value=None)
#         mocker.patch("utils.steam_image.Image.backup", return_value=None)
#         steam_grid_path = "tests/test_destination"
#         success = steam_image.update_steam_image(steam_grid_path)
#         assert success

#     def test_identical_image(self, mocker):

#         test_path = "tests/test_images/Hitman 3_grid_1659040.jpg"
#         steam_image = Image(test_path, DESTINATION)

#         mocker.patch("shutil.copyfile", return_value=None)
#         mocker.patch("utils.steam_image.Image.backup", return_value=None)
#         steam_grid_path = "tests/test_destination"
#         success = steam_image.update_steam_image(steam_grid_path)
#         assert not success
