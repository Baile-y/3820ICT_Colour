from conversion_functions import *
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb  # Import ttkbootstrap for modern themes

class ColourConverterPage(ttkb.Frame):  # Inherit from ttkbootstrap's Frame
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create a container frame to center all content
        self.container = ttk.Frame(self)
        self.container.pack(expand=True, anchor="center")  # Center the container frame

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
        color_format_selector = ttkb.Combobox(self.container, textvariable=self.color_format,
                                              values=["RGB", "HEX", "CMYK", "HSL", "HSV"],
                                              bootstyle="info")
        color_format_selector.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E))
        color_format_selector.set("HEX")  # Set default to HEX

        # Automatically update placeholder for color input based on selected format
        self.color_format.trace('w', self.update_placeholder)

        # Input entry for color value
        color_input_entry = ttkb.Entry(self.container, textvariable=self.color_input, width=25, bootstyle="info")
        color_input_entry.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E))

        # Convert button
        convert_button = ttkb.Button(self.container, text="Convert", command=self.convert_color, bootstyle="primary")
        convert_button.grid(column=2, row=1, sticky=(tk.W, tk.E))

        # Display area for the color
        self.color_display = tk.Label(self.container, width=10, height=5, bg='#fff', relief='solid')
        self.color_display.grid(column=0, row=2, rowspan=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels and read-only entries for the color values
        labels = ["RGB:", "HSL:", "HSV:", "CMYK:", "HEX:"]
        variables = [self.rgb_value, self.hsl_value, self.hsv_value, self.cmyk_value, self.hex_value_var]

        for i, (label_text, var) in enumerate(zip(labels, variables), start=2):
            label = ttkb.Label(self.container, text=label_text, bootstyle="info")
            label.grid(column=1, row=i, sticky=tk.W)
            entry = ttkb.Entry(self.container, textvariable=var, state='readonly', bootstyle="info")
            entry.grid(column=2, row=i, sticky=(tk.W, tk.E))

        # Error label
        self.error_label = ttkb.Label(self.container, text="", bootstyle="danger")
        self.error_label.grid(column=0, row=7, columnspan=3, sticky=tk.W)

        # Configure padding for all widgets
        for child in self.container.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def update_placeholder(self, *args):
        """
        Update the placeholder value based on the selected color format.
        """
        input_format = self.color_format.get()
        if input_format == 'RGB':
            self.color_input.set("255, 255, 255")  # Example for RGB
        elif input_format == 'HEX':
            self.color_input.set("#FFFFFF")  # Example for HEX
        elif input_format == 'CMYK':
            self.color_input.set("0.0, 0.0, 0.0, 0.0")  # Example for CMYK
        elif input_format == 'HSL':
            self.color_input.set("360, 100, 50")  # Example for HSL
        elif input_format == 'HSV':
            self.color_input.set("360, 100, 100")  # Example for HSV

    def convert_color(self):
        input_value = self.color_input.get().strip()
        input_format = self.color_format.get()

        if not input_value:
            self.error_label.config(text="Please provide a valid input value")
            return

        try:
            if input_format == 'HEX':
                if not input_value.startswith("#"):
                    input_value = "#" + input_value  # Add missing '#' if necessary
                rgb = hex_to_rgb(input_value)

            elif input_format == 'RGB':
                values = [x.strip() for x in input_value.split(',')]
                if len(values) != 3:
                    raise ValueError("RGB input must have 3 values (e.g., 255, 255, 255)")
                rgb = tuple(map(int, values))

            elif input_format == 'CMYK':
                values = [x.strip() for x in input_value.split(',')]
                if len(values) != 4:
                    raise ValueError("CMYK input must have 4 values (e.g., 0.0, 0.0, 0.0, 0.0)")
                cmyk = tuple(map(float, values))
                rgb = cmyk_to_rgb(*cmyk)

            elif input_format == 'HSL':
                values = [x.strip() for x in input_value.split(',')]
                if len(values) != 3:
                    raise ValueError("HSL input must have 3 values (e.g., 360, 100, 50)")
                hsl = tuple(map(float, values))
                rgb = hsl_to_rgb(*hsl)

            elif input_format == 'HSV':
                values = [x.strip() for x in input_value.split(',')]
                if len(values) != 3:
                    raise ValueError("HSV input must have 3 values (e.g., 360, 100, 100)")
                hsv = tuple(map(float, values))
                rgb = hsv_to_rgb(*hsv)

            else:
                raise ValueError("Invalid input format")

            # Convert RGB to other formats
            hex_value = rgb_to_hex(*rgb)
            cmyk = rgb_to_cmyk(*rgb)
            hsl = rgb_to_hsl(*rgb)
            hsv = rgb_to_hsv(*rgb)

            # Update UI with converted values
            self.color_display.config(bg=hex_value)
            self.rgb_value.set(f"{rgb[0]}, {rgb[1]}, {rgb[2]}")
            self.hsl_value.set(f"{hsl[0]}, {hsl[1]}, {hsl[2]}")
            self.hsv_value.set(f"{hsv[0]}, {hsv[1]}, {hsv[2]}")
            self.cmyk_value.set(f"{cmyk[0]}, {cmyk[1]}, {cmyk[2]}, {cmyk[3]}")
            self.hex_value_var.set(hex_value)

            self.error_label.config(text="")  # Clear error message on success

        except ValueError as e:
            self.error_label.config(text=str(e))  # Display specific error messages

# Example usage:
if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")  # Create a themed window
    root.title("Color Converter")
    ColourConverterPage(root, None).pack(fill="both", expand=True)
    root.mainloop()
