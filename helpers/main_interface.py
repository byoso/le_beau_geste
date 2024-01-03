import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from data import data
from helpers.folders_window import FoldersWindow


class MainInterface(Gtk.Grid):
    def __init__(self):
        super().__init__()
        self.set_column_homogeneous(False)
        self.set_row_homogeneous(False)
        self.set_border_width(10)
        self.set_column_spacing(10)
        self.set_row_spacing(10)
        self.set_hexpand(False)
        self.set_vexpand(False)
        self.width = 600

        # Items
        # + collections
        btn_folders = Gtk.Button(label="+ collections", tooltip_text="Manage your collections")
        btn_folders.connect("clicked", self.open_folders_window)
        self.attach(btn_folders, 0, 0, 1, 1)

        # my collections
        self.refresh_combo()

        # refresh
        self.btn_refresh = Gtk.Button(label="Refresh", tooltip_text="Refresh the list")
        self.btn_refresh.connect("clicked", self.refresh_combo)
        self.attach(self.btn_refresh, 12, 0, 1, 1)

        # timer
        self.timer_button = Gtk.Button(label="timer", tooltip_text="Click to save the setting")
        self.timer_button.connect("clicked", self.save_timer)
        self.timer_button.set_hexpand(False)
        self.attach(self.timer_button, 0, 1, 3, 1)
        self.timer = Gtk.SpinButton.new_with_range(30, 1200, 30)
        self.timer.set_value(int(data["timer"]))
        self.set_timer_button()
        self.timer.connect("value-changed", self.timer_changed)
        self.attach(self.timer, 3, 1, 1, 1)

        # GO !
        self.go_button = Gtk.Button(label="GO !", tooltip_text="Click to start the timer")
        self.go_button.get_style_context().add_class("success")
        self.attach(self.go_button, 4, 1, 1, 1)

        # previous /next
        self.btn_previous = Gtk.Button(label="< Previous")
        self.attach(self.btn_previous, 5, 1, 1, 1)
        self.btn_next = Gtk.Button(label="Next >")
        self.attach(self.btn_next, 6, 1, 1, 1)

    # callbacks
    def save_timer(self, widget):
        data["timer"] = self.timer.get_value_as_int()

    def timer_changed(self, timer):
        self.set_timer_button()

    def set_timer_button(self):
        value = self.timer.get_value_as_int()
        seconds = value % 60
        minutes = int((value - seconds) / 60)
        self.timer_button.set_label(f"timer ({minutes}m {seconds}s)")

    def open_folders_window(self, widget):
        window = FoldersWindow(data=data)
        window.show_all()

    def refresh_combo(self, *args):
        if hasattr(self, "collection_store"):
            self.collection_store.clear()
        if hasattr(self, "my_folders"):
            self.my_folders.destroy()
        self.collection_store = Gtk.ListStore(str, str, str)
        self.collection_store.append(["0", "-- Select a collection --", ""])
        for folder in data["folders"]:
            self.collection_store.append([folder["id"], folder["name"], folder["path"]])
        self.my_folders = Gtk.ComboBox.new_with_model(self.collection_store)
        self.my_folders.set_entry_text_column(0)
        self.my_folders.set_active(0)
        renderer_text = Gtk.CellRendererText()
        self.my_folders.pack_start(renderer_text, True)
        self.my_folders.add_attribute(renderer_text, "text", 1)
        self.my_folders.set_hexpand(False)
        self.my_folders.connect("changed", self.on_folder_changed)
        self.attach(self.my_folders, 2, 0, 10, 1)
        if data["last_collection"] is not None:
            for i, row in enumerate(self.collection_store):
                if row[0] == data["last_collection"]["id"]:
                    self.my_folders.set_active(i)
                    break
        self.show_all()


    def on_folder_changed(self, combo):
        index = combo.get_active()
        if index < 0:
            return
        folder_id = self.collection_store[index][0]
        folder = data.get_folder(folder_id)
        data["last_collection"] = folder
