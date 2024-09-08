import pytest
from PIL import Image
import tkinter as tk
from unittest.mock import patch, MagicMock
from colour_gear import ColourGearPage


@pytest.fixture
def create_test_image():
    """Helper fixture to create a mock colour wheel image for testing"""
    size = 300
    image = Image.new("RGB", (size, size), "white")
    return image


@pytest.fixture
def setup_page(create_test_image):
    """Fixture to set up a basic ColourGearPage instance for testing"""
    with patch("colour_gear.ImageTk.PhotoImage") as MockPhotoImage:
        MockPhotoImage.return_value = MagicMock()  # Mock the PhotoImage

        # Mock the Canvas as well since it's tied to tkinter's internals
        with patch("tkinter.Canvas") as MockCanvas:
            root = tk.Tk()
            page = ColourGearPage(root, None)
            page.colour_wheel = create_test_image  # Mock the colour wheel image
            return page


def test_get_complementary_colour(setup_page):
    page = setup_page
    x, y = 100, 100
    comp_x, comp_y, comp_rgb = page.get_complementary_colour(x, y)

    # Assert complementary pixel coordinates are correct
    assert comp_x == page.size // 2 * 2 - x
    assert comp_y == page.size // 2 * 2 - y
    assert isinstance(comp_rgb, tuple)


def test_get_analogous_colours(setup_page):
    page = setup_page
    x, y = 100, 100
    analogous_colours = page.get_analogous_colours(x, y)

    # Assert that two analogous colours are returned
    assert len(analogous_colours) == 2
    for ax, ay, colour in analogous_colours:
        assert isinstance(colour, tuple)
        assert 0 <= ax < page.size
        assert 0 <= ay < page.size


def test_get_triadic_colours(setup_page):
    page = setup_page
    x, y = 150, 150
    triadic_colours = page.get_triadic_colours(x, y)

    # Assert that two triadic colours are returned
    assert len(triadic_colours) == 2
    for tx, ty, colour in triadic_colours:
        assert isinstance(colour, tuple)
        assert 0 <= tx < page.size
        assert 0 <= ty < page.size


def test_get_split_complementary_colours(setup_page):
    page = setup_page
    x, y = 120, 120
    split_comp_colours = page.get_split_complementary_colours(x, y)

    # Assert that two split complementary colours are returned
    assert len(split_comp_colours) == 2
    for sx, sy, colour in split_comp_colours:
        assert isinstance(colour, tuple)
        assert 0 <= sx < page.size
        assert 0 <= sy < page.size


def test_get_tetradic_colours(setup_page):
    page = setup_page
    x, y = 140, 140
    tetradic_colours = page.get_tetradic_colours(x, y)

    # Assert that three tetradic colours are returned
    assert len(tetradic_colours) == 3
    for tx, ty, colour in tetradic_colours:
        assert isinstance(colour, tuple)
        assert 0 <= tx < page.size
        assert 0 <= ty < page.size


def test_get_text_colour(setup_page):
    page = setup_page
    rgb_light = (255, 255, 255)  # White
    rgb_dark = (0, 0, 0)  # Black

    # Assert text colour for light background is black and for dark background is white
    assert page.get_text_colour(rgb_light) == "black"
    assert page.get_text_colour(rgb_dark) == "white"
