import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image
from conversion_functions import *
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas


class ColourGrabPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_path = tk.StringVar()
        
        self.error_label = ttk.Label(self, text=" ")
        self.error_label.grid(column=0, row=20, sticky=tk.W)

        image_path_label = ttk.Label(self, text="Image Path:")
        image_path_label.grid(column=0, row=6, sticky=tk.W)
        
        image_path_entry = tk.Entry(self, textvariable=self.file_path, width=25)
        image_path_entry.grid(column=0, row=7, columnspan=2, sticky=(tk.W, tk.E))
        
        submit_button = ttk.Button(self, text="Go", command=self.submit)
        submit_button.grid(column=0, row=9, sticky=(tk.W, tk.E))
        
        self.canvas = Canvas(self, width=500, height=50)
        self.canvas.grid(column=0, row=10, columnspan=2, pady=10)
        
    def submit(self):
        file_path = self.file_path.get()
        try:
        # Load the image
            image = Image.open(file_path)
            image = image.resize((image.width // 2, image.height // 2))  # Resize for faster processing
            image = np.array(image)
            colours = self.extract_colour_palette(image, num_colours=5)
            self.error_label.config(text="")
            self.display_colour_palette(colours)
        except:
            self.error_label.config(text="Please enter a valid image file path.")
            print("Bad path")
    
    def extract_colour_palette(self, image, num_colours=5):
        # Reshape the image to be a list of pixels
        pixels = image.reshape(-1, 3)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=num_colours)
        kmeans.fit(pixels)
        
        # Get the colours
        colours = kmeans.cluster_centers_.astype(int)
        
        return colours
    
    def display_colour_palette(self, colours):
        
        self.canvas.delete("all")

        # Calculate the width of each color block
        block_width = 500 // len(colours)
        
        for i, colour in enumerate(colours):
            # Convert the RGB colour to a hex string
            hex_colour = f'#{colour[0]:02x}{colour[1]:02x}{colour[2]:02x}'
            
            # Draw a rectangle for each colour
            self.canvas.create_rectangle(i * block_width, 0, (i + 1) * block_width, 50, fill=hex_colour, outline="")
