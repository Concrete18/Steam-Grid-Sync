# Steam Grid Sync

## Quick Start

### 1. Create Steam Grid Images Folder

It will contain your images in the following format.

```py
{game name}_{grid or active or hero or logo}_{game appid}
```

#### Example:

Game1_grid_123456.png

### 2. Fill out Config

```ini
[Settings]
STEAM_ID=Insert Steam ID
STEAM_ID_3=Insert Steam ID 3
STEAM_FOLDER=C:/Program Files (x86)/Steam
CUSTOM_GRID_PATH=Insert Path to folder container your images

[Overrides]
STEAM_GRID_PATH=Insert override path for Steam Grid folder (Optional)
```

### 3. Run main.py

```bash
py main.py
```
