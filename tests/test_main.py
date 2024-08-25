# local imports
from main import SteamGrid


class TestCheckPlatform:
    grid = SteamGrid()
    grid.GRID_IMAGE_PATH = "test_folder"

    def test_check_platform(self):

        image_filename = "Warframe_grid_230410.jpg"
        image_data = self.grid.get_image_data(image_filename)
        assert image_data["name"] == "Warframe"
        assert image_data["type"] == "grid"
        assert image_data["app_id"] == 230410
        assert image_data["path"] == "test_folder\Warframe_grid_230410.jpg"
