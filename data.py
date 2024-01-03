
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

    def add_folder(self, folder_name=None, folder_path=""):
        """add a folder to the list"""
        id = str(uuid.uuid4())
        if folder_name is None:
            folder_name = f"_ Unitled collection- {id[:4]}"
        folder = {"name": folder_name, "path": folder_path, "id": id}
        if len(self.data["folders"]) == 0:
            self.data["folders"].append(folder)
        else:
            self.data["folders"].insert(0, folder)
        self.__save()

    def delete_folder(self, folder_id):
        for folder in self.data["folders"]:
            if folder["id"] == folder_id:
                self.data["folders"].remove(folder)
        self.__save()

    def rename_folder(self, folder_id, new_name):
        for folder in self.data["folders"]:
            if folder["id"] == folder_id:
                folder["name"] = new_name
        self.__save()

    def get_data(self):
        """get data from json file"""
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            data["folders"].sort(key=lambda x: x["name"])
        return data

    def __save(self):
        """save data to json file"""
        # print('saving data:', self.data)
        self.data["folders"].sort(key=lambda x: x["name"])
        with open(DATA_FILE, "w") as file:
            json.dump(self.data, file, indent=2)


data = Data()
