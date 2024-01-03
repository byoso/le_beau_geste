
import subprocess
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from data import data
from helpers.utils import open_folder


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class IconMenuItem(Gtk.MenuItem):
    """Replaces Gtk.ImageMenuItem which is deprecated"""
    def __init__(self, label='', icon_name=None, icon_size=5):
        super().__init__()
        label = Gtk.Label(label=label)
        box = Gtk.Box()
        self.add(box)
        if icon_name is not None:
            image = Gtk.Image.new_from_icon_name(
            icon_name,
            Gtk.IconSize(icon_size)
            )
            box.pack_start(image, False, False, 0)
        box.pack_start(label, False, False, 0)
        self.show_all()


class FolderItem(Gtk.Grid):
    def __init__(self, folder):
        super().__init__()
        self.folder = folder

        self.input = Gtk.Entry(max_length=64, text=folder["name"])

        btn_save = Gtk.Button(label="Save", tooltip_text="Save name")
        btn_save.connect("clicked", self.save)
        btn_save.get_style_context().add_class("success")

        btn_open = Gtk.Button(label="Open", tooltip_text="Open the folder")
        btn_open.connect("clicked", self.open)

        btn_delete = Gtk.Button(label="Delete", tooltip_text="Delete this entry")
        btn_delete.get_style_context().add_class("danger")
        btn_delete.connect("clicked", self.delete)

        self.set_column_homogeneous(True)
        self.set_row_homogeneous(True)
        self.attach(self.input, 0, 0, 4, 1)
        self.attach(btn_save, 5, 0, 1, 1)
        self.attach(btn_open, 6, 0, 1, 1)
        self.attach(btn_delete, 7, 0, 1, 1)
        self.show_all()

    def delete(self, widget):
        data.delete_folder(self.folder["id"])
        self.emit("update_folders")
        self.destroy()

    def save(self, widget):
        self.folder["name"] = self.input.get_text().strip()
        data.rename_folder(self.folder["id"], self.folder["name"])
        self.emit("send_notification", object(), f"Name '{self.folder['name']}' saved", "notif-success")
        self.emit("update_folders")

    def open(self, widget):
        opening = open_folder(self.folder["path"])
        if not opening:
            self.emit("send_notification", object(), f"No folder found for '{self.folder['name']}'", "notif-danger")

    @GObject.Signal()
    def update_folders(self):
        pass

    @GObject.Signal(flags=GObject.SignalFlags.RUN_LAST, return_type=bool,
                    arg_types=(object, str, str),
                    accumulator=GObject.signal_accumulator_true_handled)
    def send_notification(self, obj, message, type):
        pass


class Notification(Gtk.Button):
    def __init__(self, message="Notification", type="info"):
        super().__init__(label=message)
        self.connect("clicked", self.close)
        self.get_style_context().add_class(type)
        self.show_all()

    def close(self, widget):
        # self.hide()
        self.destroy()

    def set(self, label, type="info"):
        self.set_label(label)
        self.get_style_context().remove_class("notif-success")
        self.get_style_context().remove_class("notif-danger")
        self.get_style_context().remove_class("notif-info")
        self.get_style_context().remove_class("notif-warning")
        self.get_style_context().add_class(type)
        self.show_all()
