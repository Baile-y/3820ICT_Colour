import pytest
from unittest import mock
from tkinter import Tk
from colour_grab import ColourGrabPage
import numpy as np


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

    assert app.image_path_label.winfo_ismapped() == 1


def test_switch_mode_to_webcam(app, mocker):
    mock_cap = mocker.Mock()
    mock_cap.read.return_value = (True, np.zeros((100, 100, 3), dtype=np.uint8))  # Return a valid image frame
    mocker.patch('cv2.VideoCapture', return_value=mock_cap)

    app.mode.set("webcam")
    app.switch_mode()

    app.update()  # Force Tkinter to update the UI

    assert app.webcam_canvas.winfo_ismapped() == 1  # Ensure the webcam canvas is visible


def test_image_submit_valid_image(app, mocker):
    mock_image = mocker.Mock()
    mock_image_array = np.zeros((100, 100, 3), dtype=np.uint8)

    # Mock Image.open and np.array
    mocker.patch('PIL.Image.open', return_value=mock_image)
    mocker.patch('numpy.array', return_value=mock_image_array)

    # Mock extract_colour_palette to test the call
    mocker.patch.object(app, 'extract_colour_palette', return_value=[[255, 0, 0], [0, 255, 0], [0, 0, 255]])

    app.file_path.set('valid_image_path.jpg')
    app.imageSubmit()

    # Ensure that the extract_colour_palette was called once
    app.extract_colour_palette.assert_called_once()


def test_image_submit_invalid_image(app, mocker):
    # Mock PIL.Image.open to raise an exception when trying to open an invalid image
    mocker.patch('PIL.Image.open', side_effect=Exception)

    # Set an invalid image path and call the imageSubmit function
    app.file_path.set('invalid_image_path.jpg')
    app.imageSubmit()

    # Ensure that an error message was displayed
    assert app.error_label.cget('text') == "Please enter a valid image file path."


def test_webcam_submit_valid_frame(app, mocker):
    # Mock the cv2.VideoCapture class to return a mocked cap object with a valid read() method
    mock_cap = mocker.Mock()
    mock_cap.read.return_value = (True, np.zeros((100, 100, 3), dtype=np.uint8))  # Ensure dtype is uint8
    app.cap = mock_cap  # Set the mocked cap object as the webcam capture

    # Mock extract_colour_palette
    mocker.patch.object(app, 'extract_colour_palette', return_value=[[255, 0, 0], [0, 255, 0], [0, 0, 255]])

    # Call the webcamSubmit function
    app.webcamSubmit()

    # Ensure that extract_colour_palette was called
    app.extract_colour_palette.assert_called_once()
    assert app.error_label.cget('text') == ""  # No error


def test_webcam_submit_invalid_frame(app, mocker):
    # Mock the cv2.VideoCapture class to return a mocked cap object with an invalid read() method
    mock_cap = mocker.Mock()
    mock_cap.read.return_value = (False, None)
    app.cap = mock_cap  # Set the mocked cap object as the webcam capture

    # Call the webcamSubmit function
    app.webcamSubmit()

    # Ensure that an error message was displayed
    assert app.error_label.cget('text') == "Failed to capture image from webcam."


def test_extract_colour_palette(app, mocker):
    mock_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

    # Mock KMeans and make it return fixed clusters
    mock_kmeans = mocker.Mock()
    mock_kmeans.cluster_centers_ = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255]])
    mocker.patch('sklearn.cluster.KMeans', return_value=mock_kmeans)

    colours = app.extract_colour_palette(mock_image)

    # Use numpy's assert_array_equal to compare arrays
    np.testing.assert_array_equal(colours, np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255]]))


def test_display_colour_palette(app):
    colours = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

    # Call the display_colour_palette function
    app.display_colour_palette(colours)

    # Check that the palette canvas was updated correctly (3 rectangles, one for each colour)
    assert len(app.palette_canvas.find_all()) == 3  # Ensure three rectangles are drawn
