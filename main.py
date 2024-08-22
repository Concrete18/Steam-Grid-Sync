import os
import shutil

def change_steam_hero_image(app_id, new_image_path, steam_user_id):
    # Define the Steam userdata path
    steam_path = os.path.join("C:", "Program Files (x86)", "Steam", "userdata", steam_user_id, "config", "grid")
    
    # Define the destination file path
    dest_path = os.path.join(steam_path, f"{app_id}p.jpg")
    
    # Backup the old image (optional)
    if os.path.exists(dest_path):
        shutil.copyfile(dest_path, dest_path + ".backup")

    # Replace with the new image
    shutil.copyfile(new_image_path, dest_path)
    print(f"Hero image for game {app_id} replaced successfully!")

# Example usage
steam_user_id = "<YOUR_STEAM_USER_ID>"
app_id = "480"  # Replace with the correct App ID
new_image_path = "C:/path/to/your/new/image.jpg"

change_steam_hero_image(app_id, new_image_path, steam_user_id)
