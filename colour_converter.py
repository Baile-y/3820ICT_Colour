from conversion_functions import *
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb  # Import ttkbootstrap for modern themes

class ColourConverterPage(ttkb.Frame):  # Inherit from ttkbootstrap's Frame
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Initialize variables
        self.color_format = tk.StringVar()
        self.color_input = tk.StringVar()
        self.rgb_value = tk.StringVar()
        self.hsl_value = tk.StringVar()
        self.hsv_value = tk.StringVar()
        self.cmyk_value = tk.StringVar()
        self.hex_value_var = tk.StringVar()

        # Configure the theme (choose from themes like 'darkly', 'flatly', 'journal', etc.)
        style = ttkb.Style("darkly")  # Apply a theme
        self.configure(style="TFrame")  # Apply the theme style to the frame

        # Color format selection dropdown
        color_format_selector = ttkb.Combobox(self, textvariable=self.color_format, values=["RGB", "HEX", "CMYK", "HSL", "HSV"], bootstyle="info")
        color_format_selector.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E))
        color_format_selector.set("HEX")

        # Input entry for color value
        color_input_entry = ttkb.Entry(self, textvariable=self.color_input, width=25, bootstyle="info")
        color_input_entry.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E))

        # Convert button
        convert_button = ttkb.Button(self, text="Convert", command=self.convert_color, bootstyle="primary")
        convert_button.grid(column=2, row=1, sticky=(tk.W, tk.E))

        # Display area for the color
        self.color_display = tk.Label(self, width=10, height=5, bg='#fff', relief='solid')
        self.color_display.grid(column=0, row=2, rowspan=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels and read-only entries for the color values
        labels = ["RGB:", "HSL:", "HSV:", "CMYK:", "HEX:"]
        variables = [self.rgb_value, self.hsl_value, self.hsv_value, self.cmyk_value, self.hex_value_var]

        for i, (label_text, var) in enumerate(zip(labels, variables), start=2):
            label = ttkb.Label(self, text=label_text, bootstyle="info")
            label.grid(column=1, row=i, sticky=tk.W)
            entry = ttkb.Entry(self, textvariable=var, state='readonly', bootstyle="info")
            entry.grid(column=2, row=i, sticky=(tk.W, tk.E))

        # Error label
        self.error_label = ttkb.Label(self, text="", bootstyle="danger")
        self.error_label.grid(column=0, row=7, columnspan=3, sticky=tk.W)

        # Configure padding for all widgets
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def convert_color(self):
        input_value = self.color_input.get().strip()
        input_format = self.color_format.get()

        if not input_value:
            self.error_label.config(text="Invalid input value")
            return

        try:
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

            self.error_label.config(text="")
        except ValueError:
            self.error_label.config(text="Invalid input value")

# Example usage:
if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")  # Create a themed window
    root.title("Color Converter")
    ColourConverterPage(root, None).pack(fill="both", expand=True)
    root.mainloop()