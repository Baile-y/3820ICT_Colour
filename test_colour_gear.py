import pytest
from tkinter import Tk
from unittest.mock import Mock
from colour_gear import ColourGearPage


@pytest.fixture
def colour_gear_page():
    """Fixture to initialize ColourGearPage with a real Tkinter parent."""
    root = Tk()  # Create a Tkinter root
    root.withdraw()  # Hide the main window during tests
    root.update_idletasks()  # Ensure any pending tasks (like image handling) are processed
    controller = Mock()  # Mock the controller
    page = ColourGearPage(root, controller)

    # Process pending image operations
    root.update_idletasks()  # Ensure images are properly loaded

    return page


def test_create_colour_wheel(colour_gear_page):
    """Test if the colour wheel is created with the correct size."""
    size = 300
    colour_wheel = colour_gear_page.create_colour_wheel(size)
    assert colour_wheel.size == (size, size)  # Check the size of the created wheel


def test_get_complementary_colour(colour_gear_page, mocker):
    """Test if the complementary colour is calculated correctly."""
    mocker.patch('colour_gear.ColourGearPage.colour_wheel')  # Mock the colour wheel image
    colour_gear_page.colour_wheel.getpixel = Mock(return_value=(255, 0, 0))  # Mock red color
    x, y = 150, 150  # Center coordinates for a 300x300 image
    comp_x, comp_y, comp_rgb = colour_gear_page.get_complementary_colour(x, y)

    assert (comp_x, comp_y) == (150, 150)  # Complementary should be opposite, same here due to centering
    assert comp_rgb == (255, 0, 0)  # The mocked color should be returned


def test_get_analogous_colours(colour_gear_page, mocker):
    """Test analogous color calculation."""
    mocker.patch('colour_gear.ColourGearPage.colour_wheel')
    colour_gear_page.colour_wheel.getpixel = Mock(return_value=(0, 255, 0))  # Mock green color
    x, y = 150, 150  # Center
    analogous_colours = colour_gear_page.get_analogous_colours(x, y)

    assert len(analogous_colours) == 2  # Should return 2 analogous colours
    for ax, ay, colour in analogous_colours:
        assert colour == (0, 255, 0)  # Mocked green color should be returned


def test_get_triadic_colours(colour_gear_page, mocker):
    """Test triadic color calculation."""
    mocker.patch('colour_gear.ColourGearPage.colour_wheel')
    colour_gear_page.colour_wheel.getpixel = Mock(return_value=(0, 0, 255))  # Mock blue color
    x, y = 150, 150  # Center
    triadic_colours = colour_gear_page.get_triadic_colours(x, y)

    assert len(triadic_colours) == 2  # Should return 2 triadic colours
    for tx, ty, colour in triadic_colours:
        assert colour == (0, 0, 255)  # Mocked blue color should be returned
