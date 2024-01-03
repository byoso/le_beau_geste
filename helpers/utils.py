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