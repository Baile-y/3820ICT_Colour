import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk
import math
from conversion_functions import *
from colour_converter import ColourConverterPage
from colour_gear import ColourGearPage
from colour_grab import ColourGrabPage

class MainApplication(tk.Tk):
    def __init__(self, *args: str, **kwargs: dict) -> None:
        """
        Initialize the Colour Converter main window and its pages.
        """
        super().__init__(*args, **kwargs)
        self.title("Color Converter")
        self.geometry("800x700")

        # Frames dictionary to hold the pages
        self.frames: dict[str, ttk.Frame] = {}

        # Create and configure the notebook for tab-like navigation
        self.create_notebook()

    def create_notebook(self) -> None:
        """
        Create a notebook (tab-like navigation) to hold different pages.
        """
        # Create the notebook for holding all the pages
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Configure the grid for responsiveness
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create the pages lazily, add them to the notebook
        self.create_lazy_page("Colour Converter", ColourConverterPage)
        self.create_lazy_page("Colour Gear", ColourGearPage)
        self.create_lazy_page("Colour Grab", ColourGrabPage)

    def create_lazy_page(self, page_name: str, page_class: type) -> None:
        """
        Create and add a page to the notebook lazily when it is first accessed.

        @param page_name: Name of the page (used as a key in the frames dictionary).
        @param page_class: Class of the page that should be created.
        """
        # Check if the page is already created
        if page_name not in self.frames:
            # Instantiate the page and store it in the frames dictionary
            frame = page_class(parent=self.notebook, controller=self)
            self.frames[page_name] = frame
            # Add the frame to the notebook and assign the tab's name
            self.notebook.add(frame, text=page_name)

    def show_frame(self, page_name: str) -> None:
        """
        Show the frame with the given page name.

        @param page_name: The name of the page to show.
        """
        # Lazy load the page if it hasn't been created yet
        if page_name not in self.frames:
            if page_name == "Colour Converter":
                self.create_lazy_page("Colour Converter", ColourConverterPage)
            elif page_name == "Colour Gear":
                self.create_lazy_page("Colour Gear", ColourGearPage)
            elif page_name == "Colour Grab":
                self.create_lazy_page("Colour Grab", ColourGrabPage)

        # Select the corresponding tab in the notebook
        self.notebook.select(self.frames[page_name])

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
