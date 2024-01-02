#! /usr/bin/env python3
# -*- coding : utf-8 -*-

import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import Gdk

import config
from folders_window import FoldersWindow
from data import Data


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data = Data()

class MainWindow(gtk.Window):
    """Basic gtk window"""
    def __init__(self):
        # Basic construction
        super().__init__(title=f"le beau geste ({config.VERSION})")
        self.set_size_request(400, 800)
        self.set_default_icon_from_file(os.path.join(BASE_DIR, "icon.png"))
        self.set_position(gtk.WindowPosition.CENTER)
        scroll = gtk.ScrolledWindow()
        self.add(scroll)
        viewport = gtk.Viewport()
        scroll.add(viewport)
        box = gtk.VBox()
        viewport.add(box)
        # connect the quit button of the window
        self.connect("delete-event", gtk.main_quit)

        # upper interface grid
        grid_1 = gtk.Grid()
        grid_1.set_column_homogeneous(True)
        grid_1.set_row_homogeneous(True)
        box.pack_start(grid_1, False, True, 0)

        # Items
        btn_folders = gtk.Button(label="+ folder")
        btn_folders.connect("clicked", self.open_folders_window)
        grid_1.attach(btn_folders, 0, 0, 1, 1)

    # callbacks
    def open_folders_window(self, widget):
        window = FoldersWindow(data=data)
        window.show_all()


if __name__ == "__main__":

    window = MainWindow()
    window.show_all()
    gtk.main()
