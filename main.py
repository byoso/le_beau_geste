#! /usr/bin/env python3
# -*- coding : utf-8 -*-

import os
from threading import Thread
import time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk, GdkPixbuf

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
        self.set_default_icon_from_file(os.path.join(BASE_DIR, "helpers", "icon_trans_le_beau_geste.png"))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.current_collection = None
        self.scroll = Gtk.ScrolledWindow()
        self.main_box = Gtk.VBox()
        self.add(self.main_box)

        self.interface_box = Gtk.VBox()
        self.display_box = Gtk.VBox()
        self.main_box.pack_start(self.interface_box, False, True, 0)
        self.main_box.pack_start(self.display_box, True, True, 0)

        # self.add(self.scroll)
        self.display_box.add(self.scroll)

        self.viewport = Gtk.Viewport()
        self.scroll.add(self.viewport)
        self.box = Gtk.VBox()

        self.viewport.add(self.box)
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
        self.interface_grid.btn_go.connect("clicked", self.display)
        self.interface_grid.my_folders.connect("changed", self.collection_changed)
        self.interface_grid.btn_previous.connect("clicked", self.previous)
        self.interface_grid.btn_next.connect("clicked", self.next)
        self.interface_grid.btn_refresh.connect("clicked", self.collection_changed)
        self.interface_grid.btn_go.connect("clicked", self.running_changed)
        self.interface_box.pack_start(self.interface_grid, False, True, 0)

        self.running = False
        self.waiting = None
        self.timer = self.get_timer()

        self.display()

    def get_timer(self):
        return self.interface_grid.timer.get_value_as_int()

    def set_remaining_time(self, label=None):
        if label is not None:
            value = label
        else:
            minutes = int(self.timer / 60)
            seconds = self.timer % 60
            value = f"{minutes}m {seconds}s"
        self.interface_grid.lbl_remaining_time.set_label(f"remaining time: {value}")

    def running_changed(self, *args):
        self.running = not self.running
        if self.running:
            self.interface_grid.btn_go.set_label("STOP")
            self.timer = self.get_timer()
            self.cycle()
        else:
            self.interface_grid.btn_go.set_label("GO !")
            if self.waiting is not None:
                self.waiting.join()
            self.timer = self.get_timer()
            self.set_remaining_time()
            self.waiting = None

    def cycle(self):
        if self.running:
            self.set_remaining_time()
            if self.timer == 0:
                self.next()
                self.timer = self.get_timer()
            self.waiting = Thread(target=self.wait_for_timer, daemon=True).start()

    def wait_for_timer(self):
        time.sleep(1)
        self.timer -= 1
        self.cycle()

    def collection_changed(self, *args):
        self.image_index = 0
        try:
            if os.path.exists(data["last_collection"]["path"]):
                self.images = get_images(data["last_collection"]["path"])
        except TypeError:
            self.images = []
        self.display()

    def set_image_count_label(self, index, images):
        self.interface_grid.set_image_count(index, images)

    def display(self, *args):
        """display the images of a folder"""

        fitting_size = type("Empty_class", (object,), {})
        fitting_size.width, fitting_size.height = self.get_size().width, self.get_size().height - 100

        self.interface_grid.set_image_count(self.image_index, len(self.images))
        if self.interface_grid.my_folders.get_active() == 0:
            return

        if hasattr(self, "image"):
            try:
                image = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    self.images[self.image_index],
                    width=fitting_size.width,
                    height=fitting_size.height,
                    preserve_aspect_ratio=True
                    )
            except IndexError:
                self.image_index = 0
                image = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    self.images[self.image_index],
                    width=fitting_size.width,
                    height=fitting_size.height,
                    preserve_aspect_ratio=True
                    )
            self.image.set_from_pixbuf(image)
            # self.image.set_from_file(self.images[self.image_index])

        elif self.images:
            # self.image = Gtk.Image.new_from_file(self.images[self.image_index])
            image = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                self.images[self.image_index],
                width=fitting_size.width,
                height=fitting_size.height,
                preserve_aspect_ratio=True
                )

            self.image = Gtk.Image.new_from_pixbuf(image)
            self.box.pack_start(self.image, False, True, 0)

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
