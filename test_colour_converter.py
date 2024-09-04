import pytest
from conversion_functions import hex_to_rgb, rgb_to_hex, cmyk_to_rgb, rgb_to_cmyk, hsl_to_rgb, rgb_to_hsl, hsv_to_rgb, rgb_to_hsv

# Testing hex_to_rgb function
def test_hex_to_rgb():
    assert hex_to_rgb("#FFFFFF") == (255, 255, 255)
    assert hex_to_rgb("#000000") == (0, 0, 0)
    assert hex_to_rgb("#FF5733") == (255, 87, 51)  # Orange shade
    assert hex_to_rgb("#00FF00") == (0, 255, 0)    # Green
    assert hex_to_rgb("#BADA55") == (186, 218, 85) # Light green

# Testing rgb_to_hex function
def test_rgb_to_hex():
    assert rgb_to_hex(255, 255, 255) == "#FFFFFF"
    assert rgb_to_hex(0, 0, 0) == "#000000"
    assert rgb_to_hex(255, 87, 51) == "#FF5733"  # Orange shade
    assert rgb_to_hex(0, 255, 0) == "#00FF00"    # Green
    assert rgb_to_hex(186, 218, 85) == "#BADA55" # Light green

# Testing cmyk_to_rgb function
def test_cmyk_to_rgb():
    assert cmyk_to_rgb(0, 1, 1, 0) == (255, 0, 0)      # Red
    assert cmyk_to_rgb(0, 0, 1, 0) == (255, 255, 0)    # Yellow
    assert cmyk_to_rgb(0.2, 0.4, 0.6, 0.1) == (184, 138, 92)  # Brownish shade

# Testing rgb_to_cmyk function
def test_rgb_to_cmyk():
    assert rgb_to_cmyk(255, 0, 0) == (0, 1, 1, 0)      # Red
    assert rgb_to_cmyk(255, 255, 0) == (0, 0, 1, 0)    # Yellow
    assert rgb_to_cmyk(183, 137, 102) == (0.0, 0.25, 0.44, 0.28)  # Brownish shade

# Testing hsl_to_rgb function
def test_hsl_to_rgb():
    assert hsl_to_rgb(0, 1, 0.5) == (255, 0, 0)        # Red
    assert hsl_to_rgb(120, 1, 0.5) == (0, 255, 0)      # Green
    assert hsl_to_rgb(240, 1, 0.5) == (0, 0, 255)      # Blue

# Testing rgb_to_hsl function
def test_rgb_to_hsl():
    assert rgb_to_hsl(255, 0, 0) == (0, 1, 0.5)        # Red
    assert rgb_to_hsl(0, 255, 0) == (120, 1, 0.5)      # Green
    assert rgb_to_hsl(0, 0, 255) == (240, 1, 0.5)      # Blue

# Testing hsv_to_rgb function
def test_hsv_to_rgb():
    assert hsv_to_rgb(0, 1, 1) == (255, 0, 0)          # Red
    assert hsv_to_rgb(120, 1, 1) == (0, 255, 0)        # Green
    assert hsv_to_rgb(240, 1, 1) == (0, 0, 255)        # Blue

# Testing rgb_to_hsv function
def test_rgb_to_hsv():
    assert rgb_to_hsv(255, 0, 0) == (0, 1, 1)          # Red
    assert rgb_to_hsv(0, 255, 0) == (120, 1, 1)        # Green
    assert rgb_to_hsv(0, 0, 255) == (240, 1, 1)        # Blue
