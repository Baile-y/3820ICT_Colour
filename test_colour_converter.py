import pytest
from tkinter import StringVar
from conversion_functions import (hex_to_rgb, rgb_to_hex, cmyk_to_rgb, rgb_to_cmyk, hsl_to_rgb, rgb_to_hsl,
                                  hsv_to_rgb, rgb_to_hsv)
from main import ColourConverterPage


# Parameterized tests for RGB to HEX
@pytest.mark.parametrize("r, g, b, expected_hex", [
    (255, 255, 255, "#FFFFFF"),
    (0, 0, 0, "#000000"),
    (255, 87, 51, "#FF5733"),
    (0, 255, 0, "#00FF00"),
    (186, 218, 85, "#BADA55")
])
def test_rgb_to_hex(r, g, b, expected_hex):
    assert rgb_to_hex(r, g, b) == expected_hex


# Parameterized tests for HEX to RGB
@pytest.mark.parametrize("hex_value, expected_rgb", [
    ("#FFFFFF", (255, 255, 255)),
    ("#ffffff", (255, 255, 255)),  # Lowercase
    ("#000000", (0, 0, 0)),
    ("#FF5733", (255, 87, 51)),
    ("#BADA55", (186, 218, 85)),
    ("#bada55", (186, 218, 85))  # Lowercase
])
def test_hex_to_rgb(hex_value, expected_rgb):
    assert hex_to_rgb(hex_value) == expected_rgb


# Parameterized tests for CMYK to RGB
@pytest.mark.parametrize("c, m, y, k, expected_rgb", [
    (0, 1, 1, 0, (255, 0, 0)),  # Red
    (0, 0, 1, 0, (255, 255, 0)),  # Yellow
    (0.2, 0.4, 0.6, 0.1, (184, 138, 92)),  # Brownish
])
def test_cmyk_to_rgb(c, m, y, k, expected_rgb):
    assert cmyk_to_rgb(c, m, y, k) == expected_rgb


# Parameterized tests for HSL to RGB
@pytest.mark.parametrize("h, s, l, expected_rgb", [
    (0, 100, 50, (255, 0, 0)),  # Red
    (120, 100, 50, (0, 255, 0)),  # Green
    (240, 100, 50, (0, 0, 255)),  # Blue
])
def test_hsl_to_rgb(h, s, l, expected_rgb):
    assert hsl_to_rgb(h, s, l) == expected_rgb


# Parameterized tests for HSV to RGB
@pytest.mark.parametrize("h, s, v, expected_rgb", [
    (0, 100, 100, (255, 0, 0)),  # Red
    (120, 100, 100, (0, 255, 0)),  # Green
    (240, 100, 100, (0, 0, 255)),  # Blue
])
def test_hsv_to_rgb(h, s, v, expected_rgb):
    assert hsv_to_rgb(h, s, v) == expected_rgb


# Parameterized tests for RGB to CMYK
@pytest.mark.parametrize("r, g, b, expected_cmyk", [
    (255, 0, 0, (0, 1, 1, 0)),  # Red
    (0, 255, 0, (1, 0, 1, 0)),  # Green
    (0, 0, 255, (1, 1, 0, 0)),  # Blue
    (255, 255, 0, (0, 0, 1, 0)),  # Yellow
    (183, 137, 102, (0.0, 0.25, 0.44, 0.28))  # Brownish
])
def test_rgb_to_cmyk(r, g, b, expected_cmyk):
    assert rgb_to_cmyk(r, g, b) == expected_cmyk


# Parameterized tests for RGB to HSL
@pytest.mark.parametrize("r, g, b, expected_hsl", [
    (255, 0, 0, (0, 100, 50)),  # Red
    (0, 255, 0, (120, 100, 50)),  # Green
    (0, 0, 255, (240, 100, 50)),  # Blue
    (255, 255, 0, (60, 100, 50)),  # Yellow
    (128, 0, 128, (300, 100, 25))  # Purple
])
def test_rgb_to_hsl(r, g, b, expected_hsl):
    assert rgb_to_hsl(r, g, b) == expected_hsl


# Parameterized tests for RGB to HSV
@pytest.mark.parametrize("r, g, b, expected_hsv", [
    (255, 0, 0, (0, 100, 100)),  # Red
    (0, 255, 0, (120, 100, 100)),  # Green
    (0, 0, 255, (240, 100, 100)),  # Blue
    (255, 255, 0, (60, 100, 100)),  # Yellow
    (128, 0, 128, (300, 100, 50))  # Purple
])
def test_rgb_to_hsv(r, g, b, expected_hsv):
    assert rgb_to_hsv(r, g, b) == expected_hsv


# Tests for invalid inputs
def test_invalid_rgb():
    with pytest.raises(ValueError):
        rgb_to_hex(256, 0, 0)  # Invalid R value
    with pytest.raises(ValueError):
        rgb_to_hex(255, -1, 0)  # Invalid G value
    with pytest.raises(ValueError):
        rgb_to_hex(255, 87.5, 0)  # Float G value


def test_invalid_hex():
    with pytest.raises(ValueError):
        hex_to_rgb("#ZZZZZZ")  # Non-hex characters
    with pytest.raises(ValueError):
        hex_to_rgb("#FFF")  # Too short


# Testing GUI input handling
def test_convert_color_hex_to_rgb(mocker):
    page = ColourConverterPage(None, None)

    # Mock input values
    page.color_input = StringVar(value='#FF5733')
    page.color_format = StringVar(value='HEX')

    page.convert_color()

    assert page.rgb_value.get() == '255, 87, 51'
    assert page.hex_value_var.get() == '#FF5733'


def test_convert_color_rgb_to_cmyk(mocker):
    page = ColourConverterPage(None, None)

    # Mock input values
    page.color_input = StringVar(value='255,87,51')
    page.color_format = StringVar(value='RGB')

    page.convert_color()

    assert page.cmyk_value.get() == '0.0, 0.66, 0.8, 0.0'
