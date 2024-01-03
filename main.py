#! /usr/bin/env python3
# -*- coding : utf-8 -*-

import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

import config
from helpers.main_interface import MainInterface
from helpers.utils import get_images
from data import data


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MainWindow(Gtk.Window):
    """Basic gtk window"""
    def __init__(self):
        # Basic construction
        super().__init__(title=f"le beau geste ({config.VERSION})")
        self.set_size_request(1000, 600)
        self.set_default_icon_from_file(os.path.join(BASE_DIR, "helpers", "icon.png"))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.current_collection = None
        scroll = Gtk.ScrolledWindow()
        self.add(scroll)
        viewport = Gtk.Viewport()
        scroll.add(viewport)
        self.box = Gtk.VBox()
        viewport.add(self.box)
        # connect the quit button of the window
        self.connect("delete-event", Gtk.main_quit)

        self.image_index = 0
        try:
            if os.path.exists(data["last_collection"]["path"]):
                self.images = get_images(data["last_collection"]["path"])
        except TypeError:
            self.images = []

        # upper interface grid
        self.interface_grid = MainInterface()
        self.interface_grid.go_button.connect("clicked", self.display)
        self.interface_grid.my_folders.connect("changed", self.collection_changed)
        self.interface_grid.btn_previous.connect("clicked", self.previous)
        self.interface_grid.btn_next.connect("clicked", self.next)
        self.interface_grid.btn_refresh.connect("clicked", self.collection_changed)
        self.box.pack_start(self.interface_grid, False, True, 0)

        self.display()

    def collection_changed(self, *args):
        self.image_index = 0
        self.display()

    def display(self, *args):
        """display the images of a folder"""
        try:
            if os.path.exists(data["last_collection"]["path"]):
                self.images = get_images(data["last_collection"]["path"])
        except TypeError:
            self.images = []

        if hasattr(self, "image"):
            try:
                self.image.set_from_file(self.images[self.image_index])
            except IndexError:
                self.image_index = 0
                self.image.set_from_file(self.images[self.image_index])
            return
        if self.images:
            self.image = Gtk.Image.new_from_file(self.images[self.image_index])
            self.box.pack_end(self.image, False, True, 0)
            print(self.images[self.image_index])

    def previous(self, *args):
        """display the previous image"""
        if self.images is None:
            return
        self.image_index -= 1
        if self.image_index < 0:
            self.image_index = len(self.images) - 1
        self.display()

    def next(self, *args):
        """display the next image"""
        if self.images is None:
            return
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.display()


if __name__ == "__main__":

    # CSS styling
    provider = Gtk.CssProvider()
    provider.load_from_path(os.path.join(BASE_DIR, "helpers", "style.css"))
    Gtk.StyleContext().add_provider_for_screen(
        Gdk.Screen.get_default(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


    window = MainWindow()
    window.show_all()
    Gtk.main()
