import pytest
from unittest.mock import MagicMock, patch
from colour_gear import ColourGearPage
import tkinter as tk
from PIL import Image

@pytest.fixture
def tkinter_root():
    """Fixture to create a new Tkinter Toplevel window for each test."""
    root = tk.Toplevel()  # Use Toplevel to avoid interference with global state
    root.withdraw()  # Hide the window so it doesn't pop up during tests
    yield root
    root.destroy()  # Ensure the Tkinter window is destroyed after each test

@pytest.fixture
def colour_gear_page(tkinter_root):
    """Fixture to set up the ColourGearPage instance using the Toplevel window."""
    # Mock the controller since it is not relevant for the tests
    controller = MagicMock()

    # Instantiate the ColourGearPage with the Toplevel window
    page = ColourGearPage(tkinter_root, controller)

    yield page

    # Explicitly destroy the Toplevel window after the test
    tkinter_root.destroy()

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

def test_highlight_selected_harmony_button(colour_gear_page):
    """Test that the selected harmony button is highlighted correctly."""
    colour_gear_page.update_harmony("Analogous")
    assert colour_gear_page.harmony_buttons["Analogous"].cget("relief") == "sunken"
    assert colour_gear_page.harmony_buttons["Analogous"].cget("bg") == "lightblue"
    assert colour_gear_page.harmony_buttons["Complementary"].cget("relief") == "raised"

def test_display_harmony(colour_gear_page):
    """Test that the correct harmony function is called based on the current harmony."""
    x, y = 150, 150

    with patch.object(colour_gear_page, 'show_complementary') as mock_complementary:
        colour_gear_page.display_harmony("Complementary", x, y)
        mock_complementary.assert_called_once_with(x, y)

    with patch.object(colour_gear_page, 'show_analogous') as mock_analogous:
        colour_gear_page.display_harmony("Analogous", x, y)
        mock_analogous.assert_called_once_with(x, y)

def test_get_text_colour(colour_gear_page):
    """Test the logic for determining if text colour should be black or white based on background."""
    dark_rgb = (10, 10, 10)  # Very dark colour
    light_rgb = (240, 240, 240)  # Very light colour
    assert colour_gear_page.get_text_colour(dark_rgb) == "white"
    assert colour_gear_page.get_text_colour(light_rgb) == "black"

@patch.object(ColourGearPage, 'handle_selection')
def test_on_click(mock_handle_selection, colour_gear_page):
    """Test that on_click calls handle_selection."""
    mock_event = MagicMock()
    colour_gear_page.on_click(mock_event)
    mock_handle_selection.assert_called_once_with(mock_event)

@patch.object(ColourGearPage, 'handle_selection')
def test_on_motion(mock_handle_selection, colour_gear_page):
    """Test that on_motion calls handle_selection."""
    mock_event = MagicMock()
    colour_gear_page.on_motion(mock_event)
    mock_handle_selection.assert_called_once_with(mock_event)

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

def test_handle_selection_out_of_bounds(colour_gear_page):
    """Test that handle_selection doesn't fail when clicking outside the colour wheel."""
    mock_event = MagicMock(x=400, y=400)  # Coordinates outside the wheel
    colour_gear_page.handle_selection(mock_event)
    # Ensure no changes are made to selected colour
    assert colour_gear_page.selected_colour_label.cget("text") == "Selected colour"
