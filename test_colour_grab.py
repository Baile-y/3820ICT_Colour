import pytest
from unittest import mock
import tkinter as tk
from PIL import Image
import numpy as np
from colour_grab import ColourGrabPage
from sklearn.cluster import KMeans

@pytest.fixture(scope="session")
def tkinter_root():
    """Fixture to create a single Tkinter root window for all tests in the session."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window so it doesn't pop up
    yield root
    root.quit()  # Ensure the Tkinter main loop quits at the end of the session
    root.destroy()  # Destroy the root window after all tests have run

@pytest.fixture
def setup_colour_grab_page(mocker, tkinter_root):
    """Fixture to set up the ColourGrabPage instance using the shared Tkinter root."""
    # Mock the controller since it is not relevant for this test
    controller = mock.Mock()

    # Mock the __del__ method to avoid issues during teardown
    mocker.patch.object(ColourGrabPage, '__del__', lambda x: None)

    # Instantiate the ColourGrabPage with the shared root window
    page = ColourGrabPage(tkinter_root, controller)

    yield page

def test_initial_state(setup_colour_grab_page):
    """Test initial state of ColourGrabPage."""
    page = setup_colour_grab_page
    assert page.mode.get() == "Image"
    assert page.num_colours.get() == 5
    assert page.cap is None
    assert page.error_label.cget("text") in ["", " "]

def test_switch_mode_to_webcam(setup_colour_grab_page, mocker):
    """Test switching mode to 'Webcam'."""
    page = setup_colour_grab_page

    # Mock the webcam initialization (with no webcam connected)
    mock_capture = mocker.patch("cv2.VideoCapture", return_value=mock.Mock(isOpened=lambda: False))

    page.mode.set("Webcam")
    page.switch_mode()

    # Call update_idletasks to ensure the GUI updates
    page.update_idletasks()

    # Test the logic after mode switch
    assert page.mode.get() == "Webcam"
    assert page.cap is None or not page.cap.isOpened()  # Webcam shouldn't open in the mock setup

def test_switch_mode_to_image(setup_colour_grab_page):
    """Test switching mode to 'Image'."""
    page = setup_colour_grab_page

    page.mode.set("Image")
    page.switch_mode()

    # Call update_idletasks to ensure the GUI updates
    page.update_idletasks()

    # Test the logic after mode switch
    assert page.mode.get() == "Image"
    assert page.cap is None  # No webcam should be active in image mode

def test_image_submit_valid(setup_colour_grab_page, mocker):
    """Test submitting a valid image."""
    page = setup_colour_grab_page

    # Mock an image path and valid image
    page.file_path.set("test_image.png")
    mock_image = Image.new('RGB', (100, 100))  # Create a mock image
    mock_open = mocker.patch("PIL.Image.open", return_value=mock_image)

    # Mock ImageTk behavior to avoid actual image display
    mocker.patch("PIL.ImageTk.PhotoImage")

    page.imageSubmit()

    # Ensure that the image is processed and the palette is displayed
    mock_open.assert_called_once_with("test_image.png")
    assert page.error_label.cget("text") == ""
    assert page.palette_canvas.find_all()  # Palette is drawn on the canvas

def test_image_submit_invalid(setup_colour_grab_page, mocker):
    """Test submitting an invalid image path."""
    page = setup_colour_grab_page

    # Mock an invalid image path
    page.file_path.set("invalid_image_path.png")
    mock_open = mocker.patch("PIL.Image.open", side_effect=FileNotFoundError)

    page.imageSubmit()

    # Ensure the error message is set
    assert page.error_label.cget("text") == "File not found. Please check the path."

def test_image_submit_empty_path(setup_colour_grab_page):
    """Test submitting an empty file path."""
    page = setup_colour_grab_page
    page.file_path.set("")
    page.imageSubmit()
    assert page.error_label.cget("text") == "File not found. Please check the path."

def test_image_resizing(setup_colour_grab_page):
    """Test the image resizing functionality."""
    page = setup_colour_grab_page
    mock_image = Image.new('RGB', (1000, 1000))  # Create a large mock image
    resized_image = page._resize_image(mock_image)
    assert resized_image.size == (500, 500)  # Check that the image is resized correctly

def test_webcam_submit_with_webcam(setup_colour_grab_page, mocker):
    """Test submitting a valid frame from the webcam."""
    page = setup_colour_grab_page

    # Mock the cv2.VideoCapture object and its methods
    mock_capture = mocker.patch("cv2.VideoCapture")

    # Create a mock for the VideoCapture object, mocking the read method
    mock_cap_instance = mock_capture.return_value
    mock_cap_instance.isOpened.return_value = True
    mock_cap_instance.read.return_value = (True, np.zeros((100, 100, 3), dtype=np.uint8))  # Mock a valid frame

    # Patch update_frame to prevent recursive calls to read()
    mocker.patch.object(page, 'update_frame')

    # Set the mode to Webcam and trigger the mode switch
    page.mode.set("Webcam")
    page.switch_mode()

    # Submit the frame from the webcam
    page.webcamSubmit()

    # Assert the mocked read method was called once
    assert mock_capture.return_value.isOpened.call_count == 1
    assert mock_capture.return_value.read.call_count == 1
    assert page.error_label.cget("text") == ""  # Ensure no error occurred

def test_webcam_submit_no_webcam(setup_colour_grab_page, mocker):
    """Test webcam submission when no webcam is available."""
    page = setup_colour_grab_page

    # Mock no webcam connected
    mock_capture = mocker.patch("cv2.VideoCapture", return_value=mock.Mock(isOpened=lambda: False))

    page.mode.set("Webcam")
    page.switch_mode()
    page.webcamSubmit()

    # Ensure the appropriate error is displayed when webcam is not available
    assert page.error_label.cget("text") == "Webcam is not initialized."

def test_webcam_submit_failed_frame(setup_colour_grab_page, mocker):
    """Test webcam submission failure when frame reading fails."""
    page = setup_colour_grab_page
    mock_capture = mocker.patch("cv2.VideoCapture")
    mock_cap_instance = mock_capture.return_value
    mock_cap_instance.isOpened.return_value = True
    mock_cap_instance.read.return_value = (False, None)  # Simulate failure to read a frame

    page.mode.set("Webcam")
    page.switch_mode()
    page.webcamSubmit()

    assert page.error_label.cget("text") == "Failed to capture image from webcam."

def test_colour_extraction(setup_colour_grab_page, mocker):
    """Test the colour extraction logic."""
    page = setup_colour_grab_page

    # Create a mock image with random pixels (it doesn't affect the result)
    mock_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

    # Mock the KMeans instance with cluster_centers_ set to return 5 colors
    mock_kmeans_instance = mocker.Mock()
    # Set 5 random colors to simulate the KMeans result
    mock_kmeans_instance.cluster_centers_ = np.random.randint(0, 255, (page.num_colours.get(), 3), dtype=np.uint8)

    # Patch the KMeans class as it's imported in colour_grab.py
    mock_kmeans = mocker.patch("colour_grab.KMeans", return_value=mock_kmeans_instance)

    # Call the extract_colour_palette method to test it
    colours = page.extract_colour_palette(mock_image)

    # Assert that KMeans fit was called
    mock_kmeans_instance.fit.assert_called_once()

    # Assert the correct number of colours were returned (should match page.num_colours.get())
    assert len(colours) == page.num_colours.get()

def test_colour_extraction_failure(setup_colour_grab_page, mocker):
    """Test KMeans failure during colour extraction."""
    page = setup_colour_grab_page
    mock_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    mock_kmeans = mocker.patch("sklearn.cluster.KMeans.fit", side_effect=Exception("Clustering error"))

    colours = page.extract_colour_palette(mock_image)

    assert page.error_label.cget("text") == "Error during colour extraction: Clustering error"
    assert colours == []  # Ensure no colours are returned in case of error

def test_display_palette(setup_colour_grab_page, mocker):
    """Test that the colour palette is displayed correctly."""
    page = setup_colour_grab_page

    # Create mock colours
    colours = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])

    page.display_colour_palette(colours)

    # Ensure that the palette was drawn on the canvas
    assert page.palette_canvas.find_all()  # Check if shapes are drawn on the canvas

def test_copy_to_clipboard(setup_colour_grab_page, mocker):
    """Test that the hex code is copied to the clipboard."""
    page = setup_colour_grab_page
    mock_clipboard_clear = mocker.patch.object(page, "clipboard_clear")
    mock_clipboard_append = mocker.patch.object(page, "clipboard_append")

    hex_code = "#ff5733"
    page.copy_to_clipboard(hex_code)

    # Assert clipboard functions were called with the correct hex code
    mock_clipboard_clear.assert_called_once()
    mock_clipboard_append.assert_called_once_with(hex_code)

    # Assert that the error label reflects the correct copied message
    assert page.error_label.cget("text") == f"Copied {hex_code} to clipboard!"
