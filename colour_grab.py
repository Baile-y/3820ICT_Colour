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
        self.mode = tk.StringVar(value="Image")  # Default mode is image
        mode_label = ttk.Label(self, text="Mode:")
        mode_label.grid(column=0, row=0, sticky=tk.W)

        mode_selector = ttkb.Combobox(
            self,
            textvariable=self.mode,
            values=["Webcam", "Image"],
            bootstyle="info",
            width=50
        )
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

        num_colour_label = tk.Label(
            self,
            text="Select Number of Colours: ",
            font=('Arial', 12, 'bold'),
            fg="white",
            bg="gray"
        )
        num_colour_label.grid(column=0, row=11, columnspan=2, sticky=(tk.W, tk.E))

        num_colour_selector = ttkb.Combobox(
            self,
            textvariable=self.num_colours,
            values=list(range(1, 11)),
            bootstyle="info",
            width=50
        )
        num_colour_selector.grid(column=0, row=12, columnspan=2, sticky=(tk.W, tk.E))
        num_colour_selector.set("5")

        self.webcam_submit_button = ttk.Button(self, text="Go", command=self.webcamSubmit)
        self.webcam_submit_button.grid(column=0, row=13, columnspan=2, pady=(0, 10), sticky=tk.EW)

        self.updating_frame = False  # Flag to prevent multiple update_frame calls

        self.switch_mode()  # Initialize the UI to match the default mode

    def switch_mode(self, event=None):
        """Switches between webcam and image modes, adjusting the UI accordingly."""
        # Clear the error message when switching modes
        self.error_label.config(text="")

        if self.mode.get().lower() == "webcam":
            self._activate_webcam_mode()
        else:
            self._activate_image_mode()

        # Trigger UI updates to ensure the visibility changes are applied
        self.update_idletasks()

    def _activate_webcam_mode(self):
        """Activates webcam mode and prepares the UI."""
        self._hide_image_widgets()  # Hide image mode-specific widgets
        self._show_webcam_widgets()  # Show webcam mode-specific widgets

        if not self.cap:
            self.cap = cv2.VideoCapture(0)  # Start the webcam capture
            if not self.cap.isOpened():
                self.error_label.config(text="Webcam is not detected or cannot be opened.")
                self.cap = None
            else:
                self.error_label.config(text="")
                if not self.updating_frame:
                    self.update_frame()  # Start updating the webcam feed

    def _activate_image_mode(self):
        """Activates image mode and prepares the UI."""
        self._hide_webcam_widgets()  # Hide webcam mode-specific widgets
        self._show_image_widgets()  # Show image mode-specific widgets

        # Clear the error message when switching to image mode
        self.error_label.config(text="")

        if self.cap and self.cap.isOpened():
            self.cap.release()  # Stop the webcam feed
        self.updating_frame = False

    def _hide_image_widgets(self):
        """Hides widgets related to the image input mode."""
        self.image_path_label.grid_remove()
        self.image_path_entry.grid_remove()
        self.image_submit_button.grid_remove()

    def _show_image_widgets(self):
        """Shows widgets related to the image input mode."""
        self.image_path_label.grid()
        self.image_path_entry.grid()
        self.image_submit_button.grid()

    def _hide_webcam_widgets(self):
        """Hides widgets related to the webcam input mode."""
        self.webcam_canvas.grid_remove()
        self.webcam_submit_button.grid_remove()

    def _show_webcam_widgets(self):
        """Shows widgets related to the webcam input mode."""
        self.webcam_canvas.grid()
        self.webcam_submit_button.grid()

    def update_frame(self):
        """Updates the webcam frame on the canvas."""
        if not self.cap:
            return

        ret, frame = self.cap.read()
        if ret and self.mode.get().lower() == "webcam":
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (self.canvas_width, self.canvas_height))
            img = Image.fromarray(frame_resized)
            img_tk = ImageTk.PhotoImage(image=img)

            self.webcam_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.webcam_canvas.img_tk = img_tk  # Keep a reference to avoid garbage collection

        if self.mode.get().lower() == "webcam" and self.cap:
            self.after(30, self.update_frame)
        else:
            self.updating_frame = False

    def imageSubmit(self):
        """Handles image submission and processes it."""
        file_path = self.file_path.get()

        if not file_path:  # Check for empty path
            self.error_label.config(text="File not found. Please check the path.")
            return

        try:
            image = Image.open(file_path)
            image = self._resize_image(image)
            image_array = np.array(image)
            colours = self.extract_colour_palette(image_array)
            self.error_label.config(text="")
            self.display_colour_palette(colours)
        except FileNotFoundError:
            self.error_label.config(text="File not found. Please check the path.")
        except Exception as e:
            self.error_label.config(text=f"An error occurred: {str(e)}")

    def _resize_image(self, image):
        """Resizes the image to improve processing speed."""
        return image.resize((image.width // 2, image.height // 2))

    def webcamSubmit(self):
        """Captures a frame from the webcam and processes it."""
        if not self.cap:
            self.error_label.config(text="Webcam is not initialized.")
            return

        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (frame_rgb.shape[1] // 2, frame_rgb.shape[0] // 2))
            colours = self.extract_colour_palette(frame_resized)
            self.palette_canvas.delete("all")
            self.display_colour_palette(colours)
            self.error_label.config(text="")
        else:
            self.error_label.config(text="Failed to capture image from webcam.")

    def extract_colour_palette(self, image):
        """Extracts a colour palette using KMeans clustering."""
        pixels = image.reshape(-1, 3)
        n_clusters = max(1, self.num_colours.get())  # Ensure at least 1 cluster
        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)  # Set random_state for deterministic results
            kmeans.fit(pixels)
            return kmeans.cluster_centers_.astype(int)
        except Exception as e:
            self.error_label.config(text=f"Error during colour extraction: {str(e)}")
            return []

    def display_colour_palette(self, colours):
        """Displays the extracted colour palette on the canvas."""
        block_width = self.canvas_width // len(colours)
        for i, colour in enumerate(colours):
            colour = np.clip(colour, 0, 255)
            hex_colour = f'#{int(colour[0]):02x}{int(colour[1]):02x}{int(colour[2]):02x}'
            self.palette_canvas.create_rectangle(
                i * block_width, 0, (i + 1) * block_width, 50, fill=hex_colour, outline=""
            )

    def __del__(self):
        """Releases the webcam when the object is destroyed."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
