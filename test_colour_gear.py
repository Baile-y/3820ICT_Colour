import pytest
from unittest.mock import MagicMock, patch
from colour_gear import ColourGearPage
import tkinter as tk
from PIL import Image

@pytest.fixture
def colour_gear_page():
    """Fixture for setting up the ColourGearPage object."""
    root = tk.Tk()  # Create a root window
    controller = MagicMock()  # Mock controller
    return ColourGearPage(root, controller)

def test_create_colour_wheel(colour_gear_page):
    """Test that the colour wheel is created with the correct dimensions."""
    wheel = colour_gear_page.create_colour_wheel(300)
    assert isinstance(wheel, Image.Image)
    assert wheel.size == (300, 300)

def test_complementary_harmony(colour_gear_page):
    """Test that complementary harmony is calculated correctly."""
    x, y = 150, 150  # Centre point for the wheel
    comp_x, comp_y, comp_rgb = colour_gear_page.get_complementary_colour(x, y)
    assert (comp_x, comp_y) == (150, 150)  # In the centre, the complementary point should be the same
    assert isinstance(comp_rgb, tuple)
    assert len(comp_rgb) == 3  # Should be an RGB tuple

def test_analogous_harmony(colour_gear_page):
    """Test that analogous harmony is calculated correctly."""
    x, y = 200, 150
    analogous_colours = colour_gear_page.get_analogous_colours(x, y)
    assert len(analogous_colours) == 2
    for (ax, ay, colour) in analogous_colours:
        assert isinstance(colour, tuple)
        assert len(colour) == 3  # Should be RGB values

def test_triadic_harmony(colour_gear_page):
    """Test that triadic harmony is calculated correctly."""
    x, y = 200, 150
    triadic_colours = colour_gear_page.get_triadic_colours(x, y)
    assert len(triadic_colours) == 2
    for (tx, ty, colour) in triadic_colours:
        assert isinstance(colour, tuple)
        assert len(colour) == 3  # Should be RGB values

def test_tetradic_harmony(colour_gear_page):
    """Test that tetradic harmony is calculated correctly."""
    x, y = 200, 150
    tetradic_colours = colour_gear_page.get_tetradic_colours(x, y)
    assert len(tetradic_colours) == 3
    for (tx, ty, colour) in tetradic_colours:
        assert isinstance(colour, tuple)
        assert len(colour) == 3  # Should be RGB values

def test_split_complementary_harmony(colour_gear_page):
    """Test that split-complementary harmony is calculated correctly."""
    x, y = 200, 150
    split_comp_colours = colour_gear_page.get_split_complementary_colours(x, y)
    assert len(split_comp_colours) == 2
    for (sx, sy, colour) in split_comp_colours:
        assert isinstance(colour, tuple)
        assert len(colour) == 3  # Should be RGB values

def test_get_text_colour(colour_gear_page):
    """Test the logic for determining if text colour should be black or white based on background."""
    dark_rgb = (10, 10, 10)  # Very dark colour
    light_rgb = (240, 240, 240)  # Very light colour
    assert colour_gear_page.get_text_colour(dark_rgb) == "white"
    assert colour_gear_page.get_text_colour(light_rgb) == "black"

# Tests related to canvas and tkinter operations are generally done using mocks
@patch.object(tk.Canvas, 'create_oval')
def test_draw_selection_circle(mock_create_oval, colour_gear_page):
    """Test the selection circle drawing method."""
    x, y = 100, 100
    colour_gear_page.draw_selection_circle(x, y)
    mock_create_oval.assert_called_once_with(x - 5, y - 5, x + 5, y + 5, outline="black", width=2, tags="selection_circle")

@patch.object(tk.Canvas, 'delete')
def test_clear_circles(mock_delete, colour_gear_page):
    """Test that the clear_circles method clears the correct elements."""
    colour_gear_page.clear_circles()
    # Check that multiple delete calls were made to remove different types of circles
    mock_delete.assert_any_call("selection_circle")
    mock_delete.assert_any_call("complementary_circle")
    mock_delete.assert_any_call("analogous_circle_0")
    mock_delete.assert_any_call("analogous_circle_1")
