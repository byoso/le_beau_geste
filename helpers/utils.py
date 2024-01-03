import os
import sys
import subprocess


def open_folder(folder_path):
    """open a folder"""
    if not os.path.exists(folder_path):
        return False
    if sys.platform == "win32":
        os.startfile(folder_path)
    else:
        subprocess.Popen(["xdg-open", folder_path])
    return True


def get_images(folder_path):
    """return a list of images in a folder"""
    images = []
    for file in os.listdir(folder_path):
        if file.endswith((".jpg", ".png", ".jpeg")):
            images.append(os.path.join(folder_path, file))
    return images