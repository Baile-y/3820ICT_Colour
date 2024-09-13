from conversion_functions import *
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk
import math

class ColourGearPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.size = 300
        self.current_harmony = tk.StringVar(value="Complementary")

        # Cache the colour wheel image
        self.colour_wheel = self.create_colour_wheel(self.size)
        self.colour_wheel_tk = ImageTk.PhotoImage(self.colour_wheel)

        # Ensure the image object is held in memory
        self.image_cache = self.colour_wheel_tk

        # Create the canvas for the colour wheel
        self.canvas = Canvas(self, width=self.size, height=self.size)
        self.canvas.create_image((self.size // 2, self.size // 2), image=self.colour_wheel_tk)
        self.canvas.pack(pady=10)

        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<Button-1>", self.on_click)

        self.harmony_buttons_frame = tk.Frame(self)
        self.harmony_buttons_frame.pack(pady=10)
        self.harmony_title_label = tk.Label(self.harmony_buttons_frame, text="Select Colour Harmony", font=('Arial', 12, 'bold'), fg="white", bg="gray")
        self.harmony_title_label.pack(pady=(0, 5))

        self.create_harmony_buttons()

        # Selected Colour Label
        self.selected_colour_label = tk.Label(self, text="Selected colour", width=22, height=3, relief="ridge", padx=5, pady=5, font=('Arial', 12, 'bold'))
        self.selected_colour_label.pack(pady=10)

        # Frame for harmony labels
        self.info_frame = tk.Frame(self)
        self.info_frame.pack(pady=10)
        self.placeholders = [tk.Label(self.info_frame, text="", width=22, height=3, relief="ridge", padx=5, pady=5, font=('Arial', 10, 'bold')) for _ in range(4)]
        for i, placeholder in enumerate(self.placeholders):
            placeholder.grid(row=i // 2, column=(i % 2) * 2, columnspan=2, padx=5, pady=5, sticky="ew")
            placeholder.grid_remove()

        self.update_harmony(self.current_harmony.get())

    def create_colour_wheel(self, size):
        """Creates a colour wheel image based on HSV values, caching it for faster access."""
        image = Image.new("RGB", (size, size))
        draw = ImageDraw.Draw(image)
        center = size // 2
        radius = size // 2

        # Precompute wheel
        for x in range(size):
            for y in range(size):
                dx, dy = x - center, y - center
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= radius:
                    angle = math.atan2(dy, dx)
                    hue = (angle + math.pi) / (2 * math.pi) * 360
                    hue = hue % 360  # Ensure hue is within [0, 360) range
                    saturation = distance / radius * 100
                    rgb = hsv_to_rgb(hue, saturation, 100)
                    draw.point((x, y), fill=rgb)
        return image

    def on_motion(self, event):
        """Handles colour selection as the mouse moves."""
        self.handle_selection(event)

    def on_click(self, event):
        """Handles colour selection on click."""
        self.handle_selection(event)

    def handle_selection(self, event):
        x, y = event.x, event.y
        if 0 <= x < self.size and 0 <= y < self.size:
            rgb = self.colour_wheel.getpixel((x, y))
            hex_colour = '#{:02x}{:02x}{:02x}'.format(*rgb)
            text_colour = self.get_text_colour(rgb)
            self.selected_colour_label.config(text=f"Selected colour: {hex_colour}", bg=hex_colour, fg=text_colour)
            self.clear_circles()
            self.draw_selection_circle(x, y)

            # Update harmony based on current selection
            harmony = self.current_harmony.get()
            self.display_harmony(harmony, x, y)

    def display_harmony(self, harmony, x, y):
        """Shows appropriate colour harmony based on the selected mode."""
        if harmony == "Complementary":
            self.show_complementary(x, y)
        elif harmony == "Analogous":
            self.show_analogous(x, y)
        elif harmony == "Triadic":
            self.show_triadic(x, y)
        elif harmony == "Tetradic":
            self.show_tetradic(x, y)
        elif harmony == "Split-Complementary":
            self.show_split_complementary(x, y)

    def clear_circles(self):
        self.canvas.delete("selection_circle")
        self.canvas.delete("complementary_circle")
        for i in range(2):
            self.canvas.delete(f"analogous_circle_{i}")
            self.canvas.delete(f"triadic_circle_{i}")
            self.canvas.delete(f"split_complementary_circle_{i}")
        for i in range(3):
            self.canvas.delete(f"tetradic_circle_{i}")

    def draw_selection_circle(self, x, y):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, tags="selection_circle")

    def create_harmony_buttons(self):
        harmony_types = ["Complementary", "Analogous", "Triadic", "Split-Complementary", "Tetradic"]
        self.harmony_buttons = {}
        for harmony in harmony_types:
            button = tk.Button(self.harmony_buttons_frame, text=harmony, command=lambda h=harmony: self.update_harmony(h))
            button.pack(side=tk.LEFT, padx=5)
            self.harmony_buttons[harmony] = button

    def update_harmony(self, harmony_type):
        self.current_harmony.set(harmony_type)
        self.clear_circles()
        self.highlight_selected_harmony_button()

    def highlight_selected_harmony_button(self):
        for harmony, button in self.harmony_buttons.items():
            if harmony == self.current_harmony.get():
                button.config(relief="sunken", bg="lightblue", fg="black")
            else:
                button.config(relief="raised", bg="gray", fg="black")

    def get_complementary_colour(self, x, y):
        center = self.size // 2
        dx = x - center
        dy = y - center
        comp_x = center - dx
        comp_y = center - dy

        # Ensure that the complementary coordinates are within the bounds of the image
        if 0 <= comp_x < self.size and 0 <= comp_y < self.size:
            comp_rgb = self.colour_wheel.getpixel((comp_x, comp_y))
            return comp_x, comp_y, comp_rgb
        else:
            # If out of bounds, return None or a default value
            return None, None, None

    def show_complementary(self, x, y):
        self.clear_harmony_labels()
        comp_x, comp_y, comp_rgb = self.get_complementary_colour(x, y)

        if comp_rgb is not None:
            hex_colour = '#{:02x}{:02x}{:02x}'.format(*comp_rgb)
            text_colour = self.get_text_colour(comp_rgb)
            self.placeholders[0].config(text=f"Colour: {hex_colour}", bg=hex_colour, fg=text_colour)
            self.placeholders[0].grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
            self.draw_complementary_circle(comp_x, comp_y, comp_rgb)
        else:
            # Handle case when complementary colour is out of bounds (no update)
            pass

    def draw_complementary_circle(self, x, y, colour):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % colour, tags="complementary_circle")

    def get_analogous_colours(self, x, y):
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        analog_angles = [angle - math.radians(30), angle + math.radians(30)]
        analog_colours = []
        for ang in analog_angles:
            ax = center + int(distance * math.cos(ang))
            ay = center + int(distance * math.sin(ang))
            if 0 <= ax < self.size and 0 <= ay < self.size:
                colour = self.colour_wheel.getpixel((ax, ay))
                analog_colours.append((ax, ay, colour))
        return analog_colours

    def show_analogous(self, x, y):
        self.clear_harmony_labels()
        colours = self.get_analogous_colours(x, y)
        for i, (ax, ay, colour) in enumerate(colours):
            hex_colour = '#{:02x}{:02x}{:02x}'.format(*colour)
            text_colour = self.get_text_colour(colour)
            self.placeholders[i].config(text=f"Colour {i + 1}: {hex_colour}", bg=hex_colour, fg=text_colour)
            self.placeholders[i].grid(row=i // 2, column=(i % 2) * 2, columnspan=2, padx=5, pady=5, sticky="ew")
            self.draw_analogous_circle(ax, ay, colour, i)

    def draw_analogous_circle(self, x, y, colour, index):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % colour, tags=f"analogous_circle_{index}")

    def get_triadic_colours(self, x, y):
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        triadic_angles = [angle + math.radians(120), angle - math.radians(120)]
        triadic_colours = []
        for ang in triadic_angles:
            tx = center + int(distance * math.cos(ang))
            ty = center + int(distance * math.sin(ang))
            if 0 <= tx < self.size and 0 <= ty < self.size:
                colour = self.colour_wheel.getpixel((tx, ty))
                triadic_colours.append((tx, ty, colour))
        return triadic_colours

    def show_triadic(self, x, y):
        self.clear_harmony_labels()
        colours = self.get_triadic_colours(x, y)
        for i, (tx, ty, colour) in enumerate(colours):
            hex_colour = '#{:02x}{:02x}{:02x}'.format(*colour)
            text_colour = self.get_text_colour(colour)
            self.placeholders[i].config(text=f"Colour {i + 1}: {hex_colour}", bg=hex_colour, fg=text_colour)
            self.placeholders[i].grid(row=i // 2, column=(i % 2) * 2, columnspan=2, padx=5, pady=5, sticky="ew")
            self.draw_triadic_circle(tx, ty, colour, i)

    def draw_triadic_circle(self, x, y, colour, index):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % colour, tags=f"triadic_circle_{index}")

    def get_tetradic_colours(self, x, y):
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        tetradic_angles = [angle + math.radians(90), angle + math.radians(180), angle + math.radians(270)]
        tetradic_colours = []
        for ang in tetradic_angles:
            tx = center + int(distance * math.cos(ang))
            ty = center + int(distance * math.sin(ang))
            if 0 <= tx < self.size and 0 <= ty < self.size:
                colour = self.colour_wheel.getpixel((tx, ty))
                tetradic_colours.append((tx, ty, colour))
        return tetradic_colours

    def show_tetradic(self, x, y):
        self.clear_harmony_labels()
        colours = self.get_tetradic_colours(x, y)
        for i, (tx, ty, colour) in enumerate(colours):
            hex_colour = '#{:02x}{:02x}{:02x}'.format(*colour)
            text_colour = self.get_text_colour(colour)
            self.placeholders[i].config(text=f"Colour {i + 1}: {hex_colour}", bg=hex_colour, fg=text_colour)
            self.placeholders[i].grid(row=i // 2, column=(i % 2) * 2, columnspan=2, padx=5, pady=5, sticky="ew")
            self.draw_tetradic_circle(tx, ty, colour, i)

    def draw_tetradic_circle(self, x, y, colour, index):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % colour, tags=f"tetradic_circle_{index}")

    def get_split_complementary_colours(self, x, y):
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        split_comp_angles = [angle + math.radians(150), angle - math.radians(150)]
        split_comp_colours = []
        for ang in split_comp_angles:
            sx = center + int(distance * math.cos(ang))
            sy = center + int(distance * math.sin(ang))
            if 0 <= sx < self.size and 0 <= sy < self.size:
                colour = self.colour_wheel.getpixel((sx, sy))
                split_comp_colours.append((sx, sy, colour))
        return split_comp_colours

    def show_split_complementary(self, x, y):
        self.clear_harmony_labels()
        colours = self.get_split_complementary_colours(x, y)
        for i, (sx, sy, colour) in enumerate(colours):
            hex_colour = '#{:02x}{:02x}{:02x}'.format(*colour)
            text_colour = self.get_text_colour(colour)
            self.placeholders[i].config(text=f"Colour {i + 1}: {hex_colour}", bg=hex_colour, fg=text_colour)
            self.placeholders[i].grid(row=i // 2, column=(i % 2) * 2, columnspan=2, padx=5, pady=5, sticky="ew")
            self.draw_split_complementary_circle(sx, sy, colour, i)

    def draw_split_complementary_circle(self, x, y, colour, index):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % colour, tags=f"split_complementary_circle_{index}")

    def clear_harmony_labels(self):
        for placeholder in self.placeholders:
            placeholder.grid_remove()

    def get_text_colour(self, rgb):
        brightness = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        return "black" if brightness > 0.5 else "white"
