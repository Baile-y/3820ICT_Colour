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
    def __init__(self, *args, **kwargs):
        """
         Initialize the Colour Converter. This is where you create the frames and attach them
        """
        super().__init__(*args, **kwargs)
        self.title("Color Converter")
        
        # Set the window size
        self.geometry("800x700")
        # Navigation Bar Frame
        nav_bar = ttk.Frame(self)
        nav_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Content Frame
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=1, column=0)#, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.frames = {}
        # Set the frame to the frame.
        for F in (ColourConverterPage, ColourGearPage, ColourGrabPage):
            page_name = F.__name__
            frame = F(parent=self.content_frame, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ColourConverterPage")

        # Navigation Buttons
        button1 = ttk.Button(nav_bar, text="Colour Converter", command=lambda: self.show_frame("ColourConverterPage"))
        button1.grid(row=0, column=0, padx=75)

        button2 = ttk.Button(nav_bar, text="Colour Gear", command=lambda: self.show_frame("ColourGearPage"))
        button2.grid(row=0, column=1, padx=75)

        button3 = ttk.Button(nav_bar, text="Colour Grab", command=lambda: self.show_frame("ColourGrabPage"))
        button3.grid(row=0, column=2, padx=75)


    def show_frame(self, page_name):
        """
         Show frame with given page name. This is equivalent to pressing enter in Tkinter's main window.
         
         @param page_name - Name of page to show frame for
        """
        frame = self.frames[page_name]
        frame.tkraise()


# This is a wrapper around MainApplication. mainloop.
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
