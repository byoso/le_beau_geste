
"""
this module is used to manipulate data stored in a json file
"""
import uuid

import os
import json
from pprint import pprint
from typing import Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")


class Data:
    def __init__(self):
        """Abstraction to manipulate data stored in a json file"""
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as file:
                json.dump(
                    {   "timer": 60,
                        "last_collection": None,
                        "folders": []
                    },
                    file,
                    indent=2
                    )
        self.data = self.get_data()

    def __repr__(self):
        pprint(self.data)

    def __getitem__(self, key: str) -> Any:
        """get an item from the data"""
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """set an item to the data"""
        self.data[key] = value
        self.save()

    def add_folder(self, folder_name=None, folder_path=""):
        """add a folder to the list"""
        id = str(uuid.uuid4())
        if folder_name is None:
            folder_name = folder_path.split("/")[-1]
        folder = {"name": folder_name, "path": folder_path, "id": id}
        if len(self.data["folders"]) == 0:
            self.data["folders"].append(folder)
        else:
            self.data["folders"].insert(0, folder)
        self.save()

    def delete_folder(self, folder_id):
        for folder in self.data["folders"]:
            if folder["id"] == folder_id:
                self.data["folders"].remove(folder)
        self.save()

    def get_folder(self, folder_id):
        for folder in self.data["folders"]:
            if folder["id"] == folder_id:
                return folder
        return None

    def rename_folder(self, folder_id, new_name):
        for folder in self.data["folders"]:
            if folder["id"] == folder_id:
                folder["name"] = new_name
        self.save()

    def get_data(self):
        """get data from json file"""
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            data["folders"].sort(key=lambda x: x["name"])
        return data

    def save(self):
        """save data to json file"""
        self.data["folders"].sort(key=lambda x: x["name"])
        with open(DATA_FILE, "w") as file:
            json.dump(self.data, file, indent=2)


data = Data()
