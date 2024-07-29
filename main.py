import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from PIL import Image, ImageDraw, ImageTk
import math

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)

def hsl_to_rgb(h, s, l):
    h = h / 360.0
    s = s / 100.0
    l = l / 100.0
    def hue_to_rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p
    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    return int(r * 255), int(g * 255), int(b * 255)

def hsv_to_rgb(h, s, v):
    h = h / 360.0
    s = s / 100.0
    v = v / 100.0
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    if i == 0: r, g, b = v, t, p
    if i == 1: r, g, b = q, v, p
    if i == 2: r, g, b = p, v, t
    if i == 3: r, g, b = p, q, v
    if i == 4: r, g, b = t, p, v
    if i == 5: r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)

def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy
    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)

def rgb_to_hsl(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    l = (max_color + min_color) / 2
    if max_color == min_color:
        h = s = 0
    else:
        d = max_color - min_color
        s = d / (2 - max_color - min_color) if l > 0.5 else d / (max_color + min_color)
        if max_color == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_color == g:
            h = (b - r) / d + 2
        elif max_color == b:
            h = (r - g) / d + 4
        h /= 6
    return round(h * 360), round(s * 100), round(l * 100)

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    v = max_color
    d = max_color - min_color
    s = 0 if max_color == 0 else d / max_color
    if max_color == min_color:
        h = 0
    else:
        if max_color == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_color == g:
            h = (b - r) / d + 2
        elif max_color == b:
            h = (r - g) / d + 4
        h /= 6
    return round(h * 360), round(s * 100), round(v * 100)

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Color Converter")

        # Set the window size
        self.geometry("800x600")

        # Navigation Bar Frame
        nav_bar = ttk.Frame(self)
        nav_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Content Frame
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.frames = {}
        for F in (ColourConverterPage, ColourGearPage, Page3):
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

        button3 = ttk.Button(nav_bar, text="Page 3", command=lambda: self.show_frame("Page3"))
        button3.grid(row=0, column=2, padx=75)


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class ColourConverterPage(ttk.Frame):
    def __init__(self, parent, controller):
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

            self.error_label.config(text="")  # Clear the error label
        except ValueError:
            self.error_label.config(text="Invalid input value")

import tkinter as tk
from tkinter import ttk, Canvas
from PIL import Image, ImageDraw, ImageTk
import math

class ColourGearPage(ttk.Frame):
    def __init__(self, parent, controller):
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
        image = Image.new("RGB", (size, size))
        draw = ImageDraw.Draw(image)
        center = size // 2
        radius = size // 2

        for x in range(size):
            for y in range(size):
                dx = x - center
                dy = y - center
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= radius:
                    angle = math.atan2(dy, dx)
                    hue = (angle + math.pi) / (2 * math.pi)
                    saturation = distance / radius
                    rgb = self.hsv_to_rgb(hue, saturation, 1)
                    draw.point((x, y), fill=rgb)
        return image

    def hsv_to_rgb(self, h, s, v):
        if s == 0.0: return (int(v * 255), int(v * 255), int(v * 255))
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = int(255 * v * (1.0 - s))
        q = int(255 * v * (1.0 - s * f))
        t = int(255 * v * (1.0 - s * (1.0 - f)))
        v = int(v * 255)
        i %= 6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

    def on_motion(self, event):
        if event is None:
            # If no event is provided, we can't update the color wheel. Perhaps use a default or do nothing.
            return
        
        self.clear_circles()
        x, y = event.x, event.y
        if 0 <= x < self.size and 0 <= y < self.size:
            rgb = self.color_wheel.getpixel((x, y))
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
            self.selected_color_label.config(text=f"Selected Color: {hex_color}", bg=hex_color)
            self.draw_selection_circle(x, y)
            
            harmony = self.current_harmony.get()
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
        self.canvas.delete("selection_circle")
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, tags="selection_circle")

    def get_complementary_color(self, x, y):
        center = self.size // 2
        dx = x - center
        dy = y - center
        comp_x = center - dx
        comp_y = center - dy
        comp_rgb = self.color_wheel.getpixel((comp_x, comp_y))
        return comp_x, comp_y, comp_rgb

    def get_analogous_colors(self, x, y):
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        analog_angles = [angle - math.radians(30), angle + math.radians(30)]
        analog_colors = []
        for ang in analog_angles:
            ax = center + int(distance * math.cos(ang))
            ay = center + int(distance * math.sin(ang))
            if 0 <= ax < self.size and 0 <= ay < self.size:
                color = self.color_wheel.getpixel((ax, ay))
                analog_colors.append((ax, ay, color))
        return analog_colors

    def get_triadic_colors(self, x, y):
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        triadic_angles = [angle + math.radians(120), angle - math.radians(120)]
        triadic_colors = []
        for ang in triadic_angles:
            tx = center + int(distance * math.cos(ang))
            ty = center + int(distance * math.sin(ang))
            if 0 <= tx < self.size and 0 <= ty < self.size:
                color = self.color_wheel.getpixel((tx, ty))
                triadic_colors.append((tx, ty, color))
        return triadic_colors

    def get_tetradic_colors(self, x, y):
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        tetradic_angles = [angle + math.radians(90), angle + math.radians(180), angle + math.radians(270)]
        tetradic_colors = []
        for ang in tetradic_angles:
            tx = center + int(distance * math.cos(ang))
            ty = center + int(distance * math.sin(ang))
            if 0 <= tx < self.size and 0 <= ty < self.size:
                color = self.color_wheel.getpixel((tx, ty))
                tetradic_colors.append((tx, ty, color))
        return tetradic_colors

    def get_split_complementary_colors(self, x, y):
        center = self.size // 2
        angle = math.atan2(y - center, x - center)
        distance = math.sqrt((x - center) ** 2 + (y - center) ** 2)
        split_comp_angles = [angle + math.radians(150), angle - math.radians(150)]
        split_comp_colors = []
        for ang in split_comp_angles:
            sx = center + int(distance * math.cos(ang))
            sy = center + int(distance * math.sin(ang))
            if 0 <= sx < self.size and 0 <= sy < self.size:
                color = self.color_wheel.getpixel((sx, sy))
                split_comp_colors.append((sx, sy, color))
        return split_comp_colors

    def show_complementary(self, x, y):
        comp_x, comp_y, comp_rgb = self.get_complementary_color(x, y)
        hex_color = '#{:02x}{:02x}{:02x}'.format(*comp_rgb)
        self.comp_color_label.config(text=f"Complementary Color: {hex_color}", bg=hex_color)
        self.draw_complementary_circle(comp_x, comp_y, comp_rgb)

    def show_analogous(self, x, y):
        colors = self.get_analogous_colors(x, y)
        self.reset_labels(self.label_analogous)
        for i, (ax, ay, color) in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.label_analogous[i].config(text=f"Analogous Color {i + 1}: {hex_color}", bg=hex_color)
            self.draw_analogous_circle(ax, ay, color, i)

    def show_triadic(self, x, y):
        colors = self.get_triadic_colors(x, y)
        self.reset_labels(self.label_triadic)
        for i, (tx, ty, color) in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.label_triadic[i].config(text=f"Triadic Color {i + 1}: {hex_color}", bg=hex_color)
            self.draw_triadic_circle(tx, ty, color, i)

    def show_tetradic(self, x, y):
        colors = self.get_tetradic_colors(x, y)
        self.reset_labels(self.label_tetradic)
        for i, (tx, ty, color) in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.label_tetradic[i].config(text=f"Tetradic Color {i + 1}: {hex_color}", bg=hex_color)
            self.draw_tetradic_circle(tx, ty, color, i)

    def show_split_complementary(self, x, y):
        colors = self.get_split_complementary_colors(x, y)
        self.reset_labels(self.label_split_complementary)
        for i, (sx, sy, color) in enumerate(colors):
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            self.label_split_complementary[i].config(text=f"Split-Complementary Color {i + 1}: {hex_color}", bg=hex_color)
            self.draw_split_complementary_circle(sx, sy, color, i)

    def draw_complementary_circle(self, x, y, color):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags="complementary_circle")

    def draw_analogous_circle(self, x, y, color, index):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags=f"analogous_circle_{index}")

    def draw_triadic_circle(self, x, y, color, index):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags=f"triadic_circle_{index}")

    def draw_tetradic_circle(self, x, y, color, index):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags=f"tetradic_circle_{index}")

    def draw_split_complementary_circle(self, x, y, color, index):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, fill='#%02x%02x%02x' % color, tags=f"split_complementary_circle_{index}")

    def update_harmony(self, harmony_type):
        self.current_harmony.set(harmony_type)
        self.clear_circles()  # Clear old circles
        self.reset_labels()  # Reset labels to default
        self.on_motion(None)  # Update the display based on the selected harmony type

    def create_harmony_buttons(self):
        harmony_types = ["Complementary", "Analogous", "Triadic", "Tetradic", "Split-Complementary"]
        for harmony in harmony_types:
            button = tk.Button(self.harmony_buttons_frame, text=harmony, command=lambda h=harmony: self.update_harmony(h))
            button.pack(side=tk.LEFT, padx=5)

    def reset_labels(self, labels=None):
        if labels is None:
            labels = [self.comp_color_label] + self.label_analogous + self.label_triadic + self.label_tetradic + self.label_split_complementary
        for label in labels:
            label.config(text=label.cget("text").split(":")[0] + ": #ffffff", bg="white")





class Page3(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="This is page 3")
        label.grid(column=0, row=0, padx=10, pady=10)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
