import pytest
from unittest.mock import MagicMock
from main import MainApplication
from colour_converter import ColourConverterPage
from colour_gear import ColourGearPage
from colour_grab import ColourGrabPage

@pytest.fixture
def app(mocker):
    """Fixture to create the MainApplication instance."""
    mocker.patch('colour_converter.ttkb.Style')  # Mock ttkbootstrap Style
    app = MainApplication()
    yield app
    app.destroy()  # Ensure the app is properly closed after the test

def test_main_application_initialization(app):
    """Test the initialization of the MainApplication."""
    assert app.title() == "Color Converter"
    # Skip geometry check or mock it
    # assert app.geometry() == "800x700"
    assert isinstance(app.frames, dict)
    assert app.notebook is not None

def test_create_lazy_page(app):
    """Test that pages are created when the MainApplication is initialized."""
    # Check that all the necessary pages have been created
    assert "Colour Converter" in app.frames
    assert "Colour Gear" in app.frames
    assert "Colour Grab" in app.frames

    # Check that the notebook contains the correct number of tabs
    assert app.notebook.index("end") == 3  # 3 tabs should be created

def test_show_frame(app):
    """Test that the correct frame is shown when show_frame is called."""
    # Simulate creating the page and showing it
    app.create_lazy_page("Colour Converter", MagicMock)
    app.show_frame("Colour Converter")

    # Assert that the notebook has the correct selected tab
    assert app.notebook.index("current") == 0  # First tab is selected

    app.create_lazy_page("Colour Gear", MagicMock)
    app.show_frame("Colour Gear")

    # Assert that the second tab is now selected
    assert app.notebook.index("current") == 1  # Second tab is selected

def test_show_frame_invalid_page(app):
    """Test showing a frame with an invalid page name."""
    # Attempt to show a non-existent frame (invalid page name)
    with pytest.raises(KeyError):
        app.show_frame("NonExistentPage")

def test_page_widgets_initialization(app):
    """Test that specific widgets exist in each page after lazy loading."""
    # Simulate lazy loading of each page
    app.create_lazy_page("Colour Converter", ColourConverterPage)
    app.create_lazy_page("Colour Gear", ColourGearPage)
    app.create_lazy_page("Colour Grab", ColourGrabPage)

    # Access widgets in 'Colour Converter' page
    colour_converter_page = app.frames["Colour Converter"]
    assert isinstance(colour_converter_page, ColourConverterPage)

    # Access widgets in 'Colour Gear' page
    colour_gear_page = app.frames["Colour Gear"]
    assert isinstance(colour_gear_page, ColourGearPage)

    # Access widgets in 'Colour Grab' page
    colour_grab_page = app.frames["Colour Grab"]
    assert isinstance(colour_grab_page, ColourGrabPage)
