from conversion_functions import *
import tkinter as tk
from tkinter import ttk

class ColourConverterPage(ttk.Frame):
    def __init__(self, parent, controller):
        """
         Initialize the control. This is where you create the widgets and bind them to the parent widget
         
         @param parent - The parent widget that will receive the widgets
         @param controller - The controller that manages the GUI ( s
        """
        super().__init__(parent)
        self.controller = controller
        
        self.color_format = tk.StringVar()
        self.color_input = tk.StringVar()
        self.rgb_value = tk.StringVar()
        self.hsl_value = tk.StringVar()
        self.hsv_value = tk.StringVar()
        self.cmyk_value = tk.StringVar()
        self.hex_value_var = tk.StringVar()

        color_format_selector = ttk.Combobox(self, textvariable=self.color_format, values=["RGB", "HEX", "CMYK", "HSL", "HSV"])
        color_format_selector.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E))
        color_format_selector.set("HEX")

        color_input_entry = tk.Entry(self, textvariable=self.color_input, width=25)
        color_input_entry.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E))

        convert_button = ttk.Button(self, text="Convert", command=self.convert_color)
        convert_button.grid(column=2, row=1, sticky=(tk.W, tk.E))

        self.color_display = tk.Label(self, width=10, height=5, bg='#fff', relief='solid')
        self.color_display.grid(column=0, row=2, rowspan=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        rgb_label = ttk.Label(self, text="RGB:")
        rgb_label.grid(column=1, row=2, sticky=tk.W)
        rgb_entry = ttk.Entry(self, textvariable=self.rgb_value, state='readonly')
        rgb_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))

        hsl_label = ttk.Label(self, text="HSL:")
        hsl_label.grid(column=1, row=3, sticky=tk.W)
        hsl_entry = ttk.Entry(self, textvariable=self.hsl_value, state='readonly')
        hsl_entry.grid(column=2, row=3, sticky=(tk.W, tk.E))

        hsv_label = ttk.Label(self, text="HSV:")
        hsv_label.grid(column=1, row=4, sticky=tk.W)
        hsv_entry = ttk.Entry(self, textvariable=self.hsv_value, state='readonly')
        hsv_entry.grid(column=2, row=4, sticky=(tk.W, tk.E))

        cmyk_label = ttk.Label(self, text="CMYK:")
        cmyk_label.grid(column=1, row=5, sticky=tk.W)
        cmyk_entry = ttk.Entry(self, textvariable=self.cmyk_value, state='readonly')
        cmyk_entry.grid(column=2, row=5, sticky=(tk.W, tk.E))

        hex_label = ttk.Label(self, text="HEX:")
        hex_label.grid(column=1, row=6, sticky=tk.W)
        hex_entry = ttk.Entry(self, textvariable=self.hex_value_var, state='readonly')
        hex_entry.grid(column=2, row=6, sticky=(tk.W, tk.E))

        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.grid(column=0, row=7, columnspan=3, sticky=tk.W)

        # Configure the grid grid for all the children.
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def convert_color(self):
        """
         Convert color from input to RGB and return it. This is called by the user when he presses the OK button.
         
         
         @return tuple of RGB values in form [ r g b
        """
        input_value = self.color_input.get().strip()
        input_format = self.color_format.get()

        # If input_value is not a valid input value
        if not input_value:
            self.error_label.config(text="Invalid input value")
            return

        try:
            # Convert input value to RGB.
            if input_format == 'HEX':
                rgb = hex_to_rgb(input_value)
            elif input_format == 'RGB':
                rgb = tuple(map(int, input_value.split(',')))
            elif input_format == 'CMYK':
                cmyk = tuple(map(float, input_value.split(',')))
                rgb = cmyk_to_rgb(*cmyk)
            elif input_format == 'HSL':
                hsl = tuple(map(float, input_value.split(',')))
                rgb = hsl_to_rgb(*hsl)
            elif input_format == 'HSV':
                hsv = tuple(map(float, input_value.split(',')))
                rgb = hsv_to_rgb(*hsv)
            else:
                self.error_label.config(text="Invalid input format")
                return

            hex_value = rgb_to_hex(*rgb)
            cmyk = rgb_to_cmyk(*rgb)
            hsl = rgb_to_hsl(*rgb)
            hsv = rgb_to_hsv(*rgb)

            self.color_display.config(bg=hex_value)
            self.rgb_value.set(f"{rgb[0]}, {rgb[1]}, {rgb[2]}")
            self.hsl_value.set(f"{hsl[0]}, {hsl[1]}, {hsl[2]}")
            self.hsv_value.set(f"{hsv[0]}, {hsv[1]}, {hsv[2]}")
            self.cmyk_value.set(f"{cmyk[0]}, {cmyk[1]}, {cmyk[2]}, {cmyk[3]}")
            self.hex_value_var.set(hex_value)

            self.error_label.config(text="")  # Clear the error label
        except ValueError:
            self.error_label.config(text="Invalid input value")