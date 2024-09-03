import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
import ttkbootstrap as ttkb

class ColourGrabPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.file_path = tk.StringVar()
        
        self.error_label = ttk.Label(self, text=" ")
        self.error_label.grid(column=0, row=20, sticky=tk.W)
        
        self.num_colours = tk.IntVar(value=5)
        self.canvas_width = 500
        self.canvas_height = 350
        
        # Mode selector
        self.mode = tk.StringVar(value="image")  # Default mode is webcam
        mode_label = ttk.Label(self, text="Mode:")
        mode_label.grid(column=0, row=0, sticky=tk.W)
        
        mode_selector = ttkb.Combobox(self, textvariable=self.mode, values=["webcam", "image"], bootstyle="info", width=50)
        mode_selector.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E))
        mode_selector.bind("<<ComboboxSelected>>", self.switch_mode)
        
        # Image input section
        self.image_path_label = ttk.Label(self, text="Image Path:")
        self.image_path_label.grid(column=0, row=6, sticky=tk.W)
        
        self.image_path_entry = tk.Entry(self, textvariable=self.file_path, width=25)
        self.image_path_entry.grid(column=0, row=7, columnspan=2, sticky=(tk.W, tk.E))
        
        self.image_submit_button = ttk.Button(self, text="Go", command=self.imageSubmit)
        self.image_submit_button.grid(column=0, row=14, sticky=(tk.W, tk.E))
        
        # Canvas for webcam feed
        self.webcam_canvas = Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.webcam_canvas.grid(column=0, row=10, columnspan=2, pady=10)
        
        # Canvas for color palette
        self.palette_canvas = Canvas(self, width=self.canvas_width, height=50)
        self.palette_canvas.grid(column=0, row=15, columnspan=2, pady=10)

        # Initialize webcam capture (but don't start it yet)
        self.cap = None
        
        num_colour_label = tk.Label(self, text="Select Number of Colours: ", font=('Arial', 12, 'bold'), fg="white", bg="gray")
        num_colour_label.grid(column=0, row=11, columnspan=2, sticky=(tk.W, tk.E))

        num_colour_selector = ttkb.Combobox(self, textvariable=self.num_colours, values=([*range(1,11)]), bootstyle="info", width=50)
        num_colour_selector.grid(column=0, row=12, columnspan=2, sticky=(tk.W, tk.E))
        num_colour_selector.set("5")
        
        self.webcam_submit_button = ttk.Button(self, text="Go", command=self.webcamSubmit)
        self.webcam_submit_button.grid(column=0, row=13, columnspan=2, pady=(0, 10), sticky=tk.EW)
        
        self.switch_mode()  # Initialize the UI to match the default mode

    def switch_mode(self, event=None):
        mode = self.mode.get()
        if mode == "webcam":
            self.image_path_label.grid_remove()
            self.image_path_entry.grid_remove()
            self.image_submit_button.grid_remove()
            self.webcam_canvas.grid()
            self.webcam_submit_button.grid()
            
            if self.cap is None:
                self.cap = cv2.VideoCapture(0)  # Start the webcam capture
            self.update_frame()  # Start updating the webcam feed
        elif mode == "image":
            self.webcam_canvas.grid_remove()
            self.webcam_submit_button.grid_remove()
            self.image_path_label.grid()
            self.image_path_entry.grid()
            self.image_submit_button.grid()
            
            if self.cap is not None and self.cap.isOpened():
                self.cap.release()  # Stop the webcam feed
                self.cap = None

    def update_frame(self):
        if self.cap is None:
            return

        ret, frame = self.cap.read()
        if ret and self.mode.get() == "webcam":  # Check if mode is still webcam
            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Resize the frame to fit the webcam canvas
            frame_resized = cv2.resize(frame_rgb, (self.canvas_width, self.canvas_height))
            
            # Convert to PIL Image
            img = Image.fromarray(frame_resized)
            img_tk = ImageTk.PhotoImage(image=img)
            
            # Update the webcam canvas
            self.webcam_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.webcam_canvas.img_tk = img_tk  # Keep a reference to avoid garbage collection

        # Schedule the next frame update if mode is still webcam
        if self.mode.get() == "webcam" and self.cap is not None:
            self.after(30, self.update_frame)
        
    def imageSubmit(self):
        file_path = self.file_path.get()
        try:
            # Load the image
            image = Image.open(file_path)
            image = image.resize((image.width // 2, image.height // 2))  # Resize for faster processing
            image = np.array(image)
            colours = self.extract_colour_palette(image)
            self.error_label.config(text="")
            self.display_colour_palette(colours)
        except:
            self.error_label.config(text="Please enter a valid image file path.")
    
    def webcamSubmit(self):
        if self.cap is None:
            self.error_label.config(text="Webcam is not initialized.")
            return

        # Capture a still frame from the webcam
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Resize for faster processing if needed
            frame_rgb = cv2.resize(frame_rgb, (frame_rgb.shape[1] // 2, frame_rgb.shape[0] // 2))
            
            # Extract the color palette from the captured frame
            colours = self.extract_colour_palette(frame_rgb)
            
            # Clear previous content and display new color palette
            self.palette_canvas.delete("all")
            self.display_colour_palette(colours)
            self.error_label.config(text="")
        else:
            self.error_label.config(text="Failed to capture image from webcam.")
    
    def extract_colour_palette(self, image):
        # Reshape the image to be a list of pixels
        pixels = image.reshape(-1, 3)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=self.num_colours.get())
        kmeans.fit(pixels)
        
        # Get the colours
        colours = kmeans.cluster_centers_.astype(int)
        
        return colours
    
    def display_colour_palette(self, colours):
        # Calculate the width of each color block
        block_width = self.canvas_width // len(colours)
        
        for i, colour in enumerate(colours):
            # Convert the RGB colour to a hex string
            hex_colour = f'#{colour[0]:02x}{colour[1]:02x}{colour[2]:02x}'
            
            # Draw a rectangle for each colour on the palette canvas
            self.palette_canvas.create_rectangle(i * block_width, 0, (i + 1) * block_width, 50, fill=hex_colour, outline="")

    def __del__(self):
        # Release the webcam when the object is destroyed
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
