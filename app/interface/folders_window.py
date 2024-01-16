import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

from app.interface.widgets import FolderItem, Notification
from app.data.data import data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data = data


class FoldersWindow(gtk.Window):
    """Basic gtk window"""
    def __init__(self, data):
        # Basic construction
        super().__init__()
        self.set_size_request(800, 300)
        self.set_default_icon_from_file(os.path.join(BASE_DIR, "icon_trans_le_beau_geste.png"))
        self.set_position(gtk.WindowPosition.CENTER)
        scroll = gtk.ScrolledWindow()
        self.add(scroll)
        viewport = gtk.Viewport()
        scroll.add(viewport)
        self.box = gtk.VBox()
        viewport.add(self.box)
        # connect the quit button of the window
        self.connect("delete-event", self.close)

        # Items

        button_1 = gtk.Button(label="+ Add a collection")
        button_1.connect("clicked", self.on_folder_clicked)
        self.box.pack_start(button_1, False, True, 0)

        self.folders_box = gtk.VBox()
        self.box.pack_start(self.folders_box, False, True, 0)

        self.folders = self.show_folders()

    def show_folders(self, *args):
        """show folders"""
        self.folders_box.destroy()
        self.folders_box = gtk.VBox()
        for folder in data["folders"]:
            # print(folder)
            folder_item = FolderItem(folder)
            folder_item.connect("update_folders", self.show_folders)
            folder_item.connect("send_notification", self.add_notification)
            self.folders_box.pack_start(folder_item, False, True, 0)
        self.box.pack_start(self.folders_box, False, True, 0)
        self.show_all()


    def add_notification(self, source, obj, message, type):
        if hasattr(self, "notification"):
            self.notification.destroy()
        self.notification = Notification(message, type)
        self.box.pack_end(self.notification, False, True, 0)


    # callbacks
    def close(self, widget, event=None):
        """Close this window"""
        self.destroy()

    def on_folder_clicked(self, widget):
        dialog = gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self,
            action=gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL, "Select", gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == gtk.ResponseType.OK:
            data.add_folder(folder_path=dialog.get_filename())
            self.show_folders()
        elif response == gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
