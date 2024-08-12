from conversion_functions import *
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk
import math

class ColourGearPage(ttk.Frame):
    def __init__(self, parent, controller):
        """
         Initialize the color wheel. This is where you create the canvas and bind it to the motion event
         
         @param parent - The parent window of the widget
         @param controller - The controller that manages the view of the
        """
        super().__init__(parent)
        self.controller = controller

        # Initialize variables
        self.size = 300  # Size for the color wheel
        self.current_harmony = tk.StringVar(value="Complementary")

        # Create the color wheel
        self.color_wheel = self.create_color_wheel(self.size)
        self.color_wheel_tk = ImageTk.PhotoImage(self.color_wheel)

        # Create the canvas to display the color wheel
        self.canvas = Canvas(self, width=self.size, height=self.size)
        self.canvas.create_image((self.size // 2, self.size // 2), image=self.color_wheel_tk)
        self.canvas.pack(pady=10)

        self.canvas.bind("<B1-Motion>", self.on_motion)

        # Create a frame to hold the selected color label
        self.selected_color_frame = tk.Frame(self)
        self.selected_color_frame.pack(pady=10)

        self.selected_color_label = tk.Label(self.selected_color_frame, text="Selected Color", width=18, height=2, relief="ridge", padx=5, pady=5)
        self.selected_color_label.pack()

        # Create a frame to hold the harmony color labels
        self.info_frame = tk.Frame(self)
        self.info_frame.pack(pady=10, fill=tk.X)

        self.comp_color_label = tk.Label(self.info_frame, text="Complementary Color", width=18, height=2, relief="ridge", padx=5, pady=5)
        self.comp_color_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.label_analogous = [
            tk.Label(self.info_frame, text="Analogous Color 1", width=18, height=2, relief="ridge", padx=5, pady=5),
            tk.Label(self.info_frame, text="Analogous Color 2", width=18, height=2, relief="ridge", padx=5, pady=5)
        ]
        self.label_analogous[0].grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.label_analogous[1].grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.label_triadic = [
            tk.Label(self.info_frame, text="Triadic Color 1", width=18, height=2, relief="ridge", padx=5, pady=5),
            tk.Label(self.info_frame, text="Triadic Color 2", width=18, height=2, relief="ridge", padx=5, pady=5)
        ]
        self.label_triadic[0].grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.label_triadic[1].grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.label_tetradic = [
            tk.Label(self.info_frame, text="Tetradic Color 1", width=18, height=2, relief="ridge", padx=5, pady=5),
            tk.Label(self.info_frame, text="Tetradic Color 2", width=18, height=2, relief="ridge", padx=5, pady=5),
            tk.Label(self.info_frame, text="Tetradic Color 3", width=18, height=2, relief="ridge", padx=5, pady=5)
        ]
        self.label_tetradic[0].grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.label_tetradic[1].grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.label_tetradic[2].grid(row=3, column=2, padx=5, pady=5, sticky="ew")

        self.label_split_complementary = [
            tk.Label(self.info_frame, text="Split-Complementary Color 1", width=18, height=2, relief="ridge", padx=5, pady=5),
            tk.Label(self.info_frame, text="Split-Complementary Color 2", width=18, height=2, relief="ridge", padx=5, pady=5)
        ]
        self.label_split_complementary[0].grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        self.label_split_complementary[1].grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Create a frame to hold the harmony type buttons
        self.harmony_buttons_frame = tk.Frame(self)
        self.harmony_buttons_frame.pack(pady=10)

        self.create_harmony_buttons()

        # Initialize the harmony type to update the display
        self.update_harmony(self.current_harmony.get())

    def create_color_wheel(self, size):
        """
         Creates a color wheel. It is used to draw an image with a color wheel around the center of the screen
         
         @param size - The size of the color wheel
         
         @return The image that was created and filled with color wheel
        """
        image = Image.new("RGB", (size, size))
        draw = ImageDraw.Draw(image)
        center = size // 2
        radius = size // 2

        # Draw the points on the center of the circle.
        for x in range(size):
            # Draw the points on the center of the circle.
            for y in range(size):
                dx = x - center
                dy = y - center
                distance = math.sqrt(dx * dx + dy * dy)
                # Draw the point on the x y axis.
                if distance <= radius:
                    angle = math.atan2(dy, dx)
                    hue = (angle + math.pi) / (2 * math.pi) * 360
                    saturation = distance / radius * 100
                    rgb = hsv_to_rgb(hue, saturation, 100)
                    draw.point((x, y), fill=rgb)
        return image

    def on_motion(self, event):
        """
         Handle mouse motion events. This is called every time the mouse moves over the color wheel
         
         @param event - The event that triggered this function
         
         @return None if event is None otherwise the value of event
        """
        # If no event is provided we can t update the color wheel.
        if event is None:
            # If no event is provided, we can't update the color wheel. Perhaps use a default or do nothing.
            return
        
        self.clear_circles()
        x, y = event.x, event.y
        # draw selection circle on screen
        if 0 <= x < self.size and 0 <= y < self.size:
            rgb = self.color_wheel.getpixel((x, y))
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
            self.selected_color_label.config(text=f"Selected Color: {hex_color}", bg=hex_color)
            self.draw_selection_circle(x, y)
            
            harmony = self.current_harmony.get()
            # shows the harmony of the player
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
        """
         Clear all circles from the canvas. This is useful when you want to re - draw a
        """
        self.canvas.delete("selection_circle")
        self.canvas.delete("complementary_circle")
        # Delete all the canvas files and all of them.
        for i in range(2):
            self.canvas.delete(f"analogous_circle_{i}")
            self.canvas.delete(f"triadic_circle_{i}")
            self.canvas.delete(f"split_complementary_circle_{i}")
        # Delete the circle with 3 points.
        for i in range(3):
            self.canvas.delete(f"tetradic_circle_{i}")

    def draw_selection_circle(self, x, y):
        """
         Draw a circle around the selection. It is used to select a node in the graph
         
         @param x - x coordinate of the circle
         @param y - y coordinate of the circle ( top left corner
        """
        self.canvas.delete("selection_circle")
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, tags="selection_circle")

    def get_complementary_color(self, x, y):
        """
         Get the complementary color of a pixel. This is used to determine the color of the pixel that is to be used for the color wheel
         
         @param x - X coordinate of the pixel
         @param y - Y coordinate of the pixel ( top left corner )
         
         @return Tuple of x y rgb of the complementary
        """
        center = self.size // 2
        dx = x - center
        dy = y - center
        comp_x = center - dx
        comp_y = center - dy
        comp_rgb = self.color_wheel.getpixel((comp_x, comp_y))
        return comp_x, comp_y, comp_rgb

    def get_analogous_colors(self, x, y):
        """
         Get the colors that are analogous to the pixel at x y. This is used to determine where the mouse is in the color wheel
         
         @param x - X coordinate of the pixel
         @param y - Y coordinate of the pixel ( 0 - 1 )
         
         @return A list of 3 - tuples ( x y color
        """
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        analog_angles = [angle - math.radians(30), angle + math.radians(30)]
        analog_colors = []
        # Add colors to the analog_colors list of analog colors.
        for ang in analog_angles:
            ax = center + int(distance * math.cos(ang))
            ay = center + int(distance * math.sin(ang))
            # Add color to analog_colors array.
            if 0 <= ax < self.size and 0 <= ay < self.size:
                color = self.color_wheel.getpixel((ax, ay))
                analog_colors.append((ax, ay, color))
        return analog_colors

    def get_triadic_colors(self, x, y):
        """
         Get the triadic colors at x y. This is used to determine where the mouse is in the middle of the color wheel
         
         @param x - X coordinate of the mouse
         @param y - Y coordinate of the mouse ( must be in the range [ 0 size )
         
         @return A list of 3 - tuples ( x y color
        """
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        triadic_angles = [angle + math.radians(120), angle - math.radians(120)]
        triadic_colors = []
        # Add colors to triadic_colors.
        for ang in triadic_angles:
            tx = center + int(distance * math.cos(ang))
            ty = center + int(distance * math.sin(ang))
            # Add a triadic color to triadic colors.
            if 0 <= tx < self.size and 0 <= ty < self.size:
                color = self.color_wheel.getpixel((tx, ty))
                triadic_colors.append((tx, ty, color))
        return triadic_colors

    def get_tetradic_colors(self, x, y):
        """
         Get tetradic colors at x y. This is used to determine where the mouse is in the image
         
         @param x - X coordinate of the mouse
         @param y - Y coordinate of the mouse ( 0 - 1 )
         
         @return List of ( x y color ) tuples for the
        """
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        tetradic_angles = [angle + math.radians(90), angle + math.radians(180), angle + math.radians(270)]
        tetradic_colors = []
        # Add colors to tetradic_colors.
        for ang in tetradic_angles:
            tx = center + int(distance * math.cos(ang))
            ty = center + int(distance * math.sin(ang))
            # Add color to tetradic colors.
            if 0 <= tx < self.size and 0 <= ty < self.size:
                color = self.color_wheel.getpixel((tx, ty))
                tetradic_colors.append((tx, ty, color))
        return tetradic_colors

    def get_split_complementary_colors(self, x, y):
        """
         Get the colors that should be used to split a pixel. This is a helper function for get_color_wheels ()
         
         @param x - X coordinate of the pixel
         @param y - Y coordinate of the pixel ( 0 - 1 )
         
         @return A list of ( sx sy color ) tuples for each
        """
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        split_comp_angles = [angle + math.radians(150), angle - math.radians(150)]
        split_comp_colors = []
        # Add colors to the split_comp_colors list of colors.
        for ang in split_comp_angles:
            sx = center + int(distance * math.cos(ang))
            sy = center + int(distance * math.sin(ang))
            # Add color to split_comp_colors. append color to split_comp_colors.
            if 0 <= sx < self.size and 0 <= sy < self.size:
                color = self.color_wheel.getpixel((sx, sy))
                split_comp_colors.append((sx, sy, color))
        return split_comp_colors

    def show_complementary(self, x, y):
        """
         Draw complementary circle at x y. This is a convenience method for calling
         
         @param x - X coordinate of upper left corner
         @param y - Y coordinate of upper left
        """
        comp_x, comp_y, comp_rgb = self.get_complementary_color(x, y)
        hex_color = '#{:02x}{:02x}{:02x}'.format(*comp_rgb)
        self.comp_color_label.config(text=f"Complementary Color: {hex_color}", bg=hex_color)
        self.draw_complementary_circle(comp_x, comp_y, comp_rgb)

    def show_analogous(self, x, y):
        """
         Show analogous circles. This is a wrapper around : meth : ` get_analogous_colors ` to create a list of circle labels and set the color of each circle to the hex color corresponding to the color of the corresponding axis.
         
         @param x - x - coordinate of the plot. It is assumed that the plot is centered on the x - axis.
         @param y - y - coordinate of the plot. It is assumed that the plot is centered on the y - axis
        """
        colors = self.get_analogous_colors(x, y)
        self.reset_labels(self.label_analogous)
        # draws analogous circle with color
        for i, (ax, ay, color) in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.label_analogous[i].config(text=f"Analogous Color {i + 1}: {hex_color}", bg=hex_color)
            self.draw_analogous_circle(ax, ay, color, i)

    def show_triadic(self, x, y):
        """
         Draw triadic circles at x y. This is a convenience method for the user to call : meth : ` get_triadic_colors ` and
         
         @param x - x coordinate of the circle
         @param y - y coordinate of the circle ( top left corner
        """
        colors = self.get_triadic_colors(x, y)
        self.reset_labels(self.label_triadic)
        # Draw triadic colors on the label.
        for i, (tx, ty, color) in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.label_triadic[i].config(text=f"Triadic Color {i + 1}: {hex_color}", bg=hex_color)
            self.draw_triadic_circle(tx, ty, color, i)

    def show_tetradic(self, x, y):
        """
         Draw tetradic circles. This is a convenience method for the common case where you want to draw a set of tetradic circles at a given x y position.
         
         @param x - X position in pixel coordinates. The origin is at the top left of the canvas.
         @param y - Y position in pixel coordinates. The origin is at the top left of the canvas
        """
        colors = self.get_tetradic_colors(x, y)
        self.reset_labels(self.label_tetradic)
        # Draw a circle with the given color.
        for i, (tx, ty, color) in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.label_tetradic[i].config(text=f"Tetradic Color {i + 1}: {hex_color}", bg=hex_color)
            self.draw_tetradic_circle(tx, ty, color, i)

    def show_split_complementary(self, x, y):
        """
         Draw the split complementary circles. This is a function that should be called by the user to draw the split complementary circles.
         
         @param x - X coordinate of the upper left corner of the split complementary circle
         @param y - Y coordinate of the upper left corner of the split complementary
        """
        colors = self.get_split_complementary_colors(x, y)
        self.reset_labels(self.label_split_complementary)
        # Draw a split complementary circle with colors.
        for i, (sx, sy, color) in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.label_split_complementary[i].config(text=f"Split-Complementary Color {i + 1}: {hex_color}", bg=hex_color)
            self.draw_split_complementary_circle(sx, sy, color, i)

    def draw_complementary_circle(self, x, y, color):
        """
         Draw complementary circle on canvas. Note : x and y are relative to upper left corner
         
         @param x - x coordinate of circle centre
         @param y - y coordinate of circle centre ( 0 0 )
         @param color - color of circle ( hex string e. g
        """
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags="complementary_circle")

    def draw_analogous_circle(self, x, y, color, index):
        """
         Draw an analogous circle on the canvas. This is used to draw circles that don't have a color or an index
         
         @param x - X coordinate of the circle
         @param y - Y coordinate of the circle. It's the same as x but with a number between 0 and 5
         @param color - The color of the circle. It's the same as the color of the circle
         @param index - The index of the circle in the list of
        """
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags=f"analogous_circle_{index}")

    def draw_triadic_circle(self, x, y, color, index):
        """
         Draw a triadic circle. This circle is used to indicate which part of the graph is the same as the one drawn by the graph_draw method
         
         @param x - x coordinate of the circle
         @param y - y coordinate of the circle ( top left corner )
         @param color - color of the circle ( hex string ) e. g.
         @param index - index of the triangle in the graph ( 0 - 3
        """
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags=f"triadic_circle_{index}")

    def draw_tetradic_circle(self, x, y, color, index):
        """
         Draw tetradic circle on canvas. This is used to draw circles that are part of a battle.
         
         @param x - X coordinate of circle. It is assumed to be 5 * x + 5
         @param y - Y coordinate of circle. It is assumed to be 5 * y
         @param color - Color of circle as hex string. It is assumed to be #rrggbbaa.
         @param index - Index of the circle in the list of tetradic
        """
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags=f"tetradic_circle_{index}")

    def draw_split_complementary_circle(self, x, y, color, index):
        """
         Draw split complementary circle. This circle is used to split a companion circle into two circles
         
         @param x - X coordinate of circle center
         @param y - Y coordinate of circle center ( top left corner )
         @param color - Color of circle ( hex string ) see L { draw_circle }
         @param index - Index of the circle in OCCURS
        """
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags=f"split_complementary_circle_{index}")

    def update_harmony(self, harmony_type):
        """
         Update harmony and circles. Clears old circles and resets labels
         
         @param harmony_type - Harmony type to set
        """
        self.current_harmony.set(harmony_type)
        self.clear_circles()  # Clear old circles
        self.reset_labels()  # Reset labels to default
        self.on_motion(None)  # Update the display based on the selected harmony type

    def create_harmony_buttons(self):
        """
         Create buttons to update harmony values. Harmony types are defined in self.
        """
        harmony_types = ["Complementary", "Analogous", "Triadic", "Tetradic", "Split-Complementary"]
        # Add the harmony buttons to the frame.
        for harmony in harmony_types:
            button = tk.Button(self.harmony_buttons_frame, text=harmony, command=lambda h=harmony: self.update_harmony(h))
            button.pack(side=tk.LEFT, padx=5)

    def reset_labels(self, labels=None):
        """
         Reset labels to default. This is useful for debugging and to ensure labels don't get stuck in the middle of a plot
         
         @param labels - list of labels to
        """
        # Returns a list of labels for the component
        if labels is None:
            labels = [self.comp_color_label] + self.label_analogous + self.label_triadic + self.label_tetradic + self.label_split_complementary
        # Set the background background for each label
        for label in labels:
            label.config(text=label.cget("text").split(":")[0] + ": #ffffff", bg="white")