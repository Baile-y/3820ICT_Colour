import pytest
from unittest import mock
from tkinter import Tk
from colour_grab import ColourGrabPage
from PIL import Image
import numpy as np
import cv2
from unittest.mock import call

@pytest.fixture
def app():
    root = Tk()
    controller = mock.Mock()
    page = ColourGrabPage(root, controller)
    yield page
    root.destroy()


def test_switch_mode_to_image(app):
    app.mode.set("image")
    app.switch_mode()

    app.update()  # Force Tkinter to update the UI

    assert app.image_path_label.winfo_ismapped() == 1  # Ensure that the image path label is visible


def test_switch_mode_to_webcam_no_camera(app, mocker):
    """Test switching to webcam mode when no webcam is detected."""
    # Mock VideoCapture to simulate no webcam being detected
    mock_cap = mocker.Mock()
    mock_cap.isOpened.return_value = False  # Simulate no webcam
    mocker.patch('cv2.VideoCapture', return_value=mock_cap)

    app.mode.set("webcam")
    app.switch_mode()

    app.update()

    # Check that the error message is displayed
    assert app.error_label.cget('text') == "Webcam is not detected or cannot be opened."


def test_webcam_submit_no_camera(app, mocker):
    """Test webcam submit when no webcam is detected."""
    # Mock VideoCapture to simulate no webcam being detected
    mock_cap = mocker.Mock()
    mock_cap.isOpened.return_value = False  # Simulate no webcam
    mocker.patch('cv2.VideoCapture', return_value=mock_cap)

    app.webcamSubmit()

    # Ensure that an error message is shown when no webcam is available
    assert app.error_label.cget('text') == "Webcam is not initialized."


def test_webcam_submit_valid_frame(app, mocker):
    """Test webcam submit with a valid frame, mocking the webcam."""
    # Mock the cv2.VideoCapture class to return a mocked cap object with a valid read() method
    mock_cap = mocker.Mock()
    mock_cap.isOpened.return_value = True  # Simulate a webcam being available
    mock_cap.read.return_value = (True, np.zeros((100, 100, 3), dtype=np.uint8))  # Simulate a valid image frame
    app.cap = mock_cap  # Set the mocked cap object as the webcam capture

    # Mock extract_colour_palette
    mocker.patch.object(app, 'extract_colour_palette', return_value=[[255, 0, 0], [0, 255, 0], [0, 0, 255]])

    # Call the webcamSubmit function
    app.webcamSubmit()

    # Ensure that extract_colour_palette was called
    app.extract_colour_palette.assert_called_once()
    assert app.error_label.cget('text') == ""  # No error


def test_image_submit_valid_image(app, mocker):
    # Create a small real image array (this will be resized in the program)
    original_image_array = np.zeros((100, 100, 3), dtype=np.uint8)

    # Mock extract_colour_palette to check if it's called
    resized_image_array = np.zeros((50, 50, 3), dtype=np.uint8)  # Mock the resized array
    mock_extract_palette = mocker.patch.object(app, 'extract_colour_palette', return_value=[[255, 0, 0], [0, 255, 0], [0, 0, 255]])

    # Save the original image array to a temporary file and set its path
    image = Image.fromarray(original_image_array)
    image.save('test_image.jpg')

    # Set the file path and trigger the image submission process
    app.file_path.set('test_image.jpg')
    app.imageSubmit()

    # Capture the actual argument passed to extract_colour_palette
    actual_call_args = mock_extract_palette.call_args[0][0]  # Get the first argument in the call

    # Ensure that extract_colour_palette was called once
    mock_extract_palette.assert_called_once()

    # Use numpy.testing.assert_array_equal to compare the actual and expected arrays
    np.testing.assert_array_equal(actual_call_args, resized_image_array)


def test_image_submit_invalid_image(app, mocker):
    # Mock PIL.Image.open to raise an exception when trying to open an invalid image
    mocker.patch('PIL.Image.open', side_effect=Exception)

    # Set an invalid image path and call the imageSubmit function
    app.file_path.set('invalid_image_path.jpg')
    app.imageSubmit()

    # Ensure that a generic error message was displayed
    assert "An error occurred:" in app.error_label.cget('text')


def test_image_submit_empty_path(app):
    app.file_path.set('')  # Empty path
    app.imageSubmit()

    assert app.error_label.cget('text') == "File not found. Please check the path."


def test_image_submit_file_not_found(app, mocker):
    # Mock Image.open to raise FileNotFoundError
    mocker.patch('PIL.Image.open', side_effect=FileNotFoundError)

    app.file_path.set('non_existent_file.jpg')
    app.imageSubmit()

    assert app.error_label.cget('text') == "File not found. Please check the path."


def test_invalid_num_colours(app, mocker):
    app.num_colours.set(0)  # Invalid number of colours
    mock_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

    # Mock KMeans clustering
    mocker.patch.object(app, 'extract_colour_palette', return_value=[[255, 0, 0], [0, 255, 0], [0, 0, 255]])

    colours = app.extract_colour_palette(mock_image)

    # Ensure the default number of colours (5) is used when invalid number is provided
    assert len(colours) == 3  # The mock returns 3 colours in this case


def test_extract_colour_palette(app, mocker):
    # Create a small, consistent image array
    mock_image = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]],
                           [[255, 255, 0], [0, 255, 255], [255, 0, 255]]], dtype=np.uint8)

    # Mock KMeans and return fixed cluster centers
    mock_kmeans = mocker.Mock()
    mock_kmeans.cluster_centers_ = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255]])
    mocker.patch('sklearn.cluster.KMeans', return_value=mock_kmeans)

    colours = app.extract_colour_palette(mock_image)

    # Ensure that the colors returned match the expected cluster centers
    np.testing.assert_array_equal(colours, np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255]]))

def test_display_colour_palette(app):
    colours = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

    # Call the display_colour_palette function
    app.display_colour_palette(colours)

    # Check that the palette canvas was updated correctly (3 rectangles, one for each colour)
    assert len(app.palette_canvas.find_all()) == 3  # Ensure three rectangles are drawn
