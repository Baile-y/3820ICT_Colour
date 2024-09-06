import pytest
from conversion_functions import (hex_to_rgb, rgb_to_hex, cmyk_to_rgb, rgb_to_cmyk, hsl_to_rgb, rgb_to_hsl,
                                  hsv_to_rgb, rgb_to_hsv)

# Testing rgb_to_hex function
def test_rgb_to_hex():
    assert rgb_to_hex(255, 255, 255) == "#FFFFFF"  # White
    assert rgb_to_hex(0, 0, 0) == "#000000"        # Black
    assert rgb_to_hex(255, 87, 51) == "#FF5733"    # Orange Shade
    assert rgb_to_hex(0, 255, 0) == "#00FF00"      # Green
    assert rgb_to_hex(186, 218, 85) == "#BADA55"   # Light Green


# Testing hex_to_rgb function
def test_hex_to_rgb():
    assert hex_to_rgb("#FFFFFF") == (255, 255, 255)  # White
    assert hex_to_rgb("#ffffff") == (255, 255, 255)  # White (Lowercase)
    assert hex_to_rgb("#000000") == (0, 0, 0)        # Black
    assert hex_to_rgb("#FF5733") == (255, 87, 51)    # Orange Shade
    assert hex_to_rgb("#00FF00") == (0, 255, 0)      # Green
    assert hex_to_rgb("#BADA55") == (186, 218, 85)   # Light Green
    assert hex_to_rgb("#bada55") == (186, 218, 85)  # Light Green (Lowercase)


# Testing cmyk_to_rgb function
def test_cmyk_to_rgb():
    assert cmyk_to_rgb(0, 1, 1, 0) == (255, 0, 0)          # Red
    assert cmyk_to_rgb(0, 0, 1, 0) == (255, 255, 0)        # Yellow
    assert cmyk_to_rgb(0.2, 0.4, 0.6, 0.1) == (184, 138, 92)  # Brownish Shade
    assert cmyk_to_rgb(0.5, 0, 0.5, 0.25) == (96, 191, 96)    # Greenish Shade
    assert cmyk_to_rgb(0.7, 0.3, 0, 0.2) == (61, 143, 204)    # Light Blue


# Testing hsl_to_rgb function
def test_hsl_to_rgb():
    assert hsl_to_rgb(0, 100, 50) == (255, 0, 0)          # Red
    assert hsl_to_rgb(120, 100, 50) == (0, 255, 0)        # Green
    assert hsl_to_rgb(240, 100, 50) == (0, 0, 255)        # Blue
    assert hsl_to_rgb(60, 100, 50) == (255, 255, 0)       # Yellow
    assert hsl_to_rgb(300, 100, 50) == (255, 0, 255)      # Magenta


# Testing hsv_to_rgb function
def test_hsv_to_rgb():
    assert hsv_to_rgb(0, 100, 100) == (255, 0, 0)         # Red
    assert hsv_to_rgb(120, 100, 100) == (0, 255, 0)       # Green
    assert hsv_to_rgb(240, 100, 100) == (0, 0, 255)       # Blue
    assert hsv_to_rgb(60, 100, 100) == (255, 255, 0)      # Yellow
    assert hsv_to_rgb(300, 100, 100) == (255, 0, 255)     # Magenta


# Testing rgb_to_cmyk function
def test_rgb_to_cmyk():
    assert rgb_to_cmyk(255, 0, 0) == (0, 1, 1, 0)             # Red
    assert rgb_to_cmyk(255, 255, 0) == (0, 0, 1, 0)           # Yellow
    assert rgb_to_cmyk(183, 137, 102) == (0.0, 0.25, 0.44, 0.28)  # Brownish Shade
    assert rgb_to_cmyk(96, 191, 96) == (0.5, 0, 0.5, 0.25)    # Greenish Shade
    assert rgb_to_cmyk(61, 143, 204) == (0.7, 0.3, 0, 0.2)    # Light Blue


# Testing rgb_to_hsl function
def test_rgb_to_hsl():
    assert rgb_to_hsl(255, 0, 0) == (0, 100, 50)          # Red
    assert rgb_to_hsl(0, 255, 0) == (120, 100, 50)        # Green
    assert rgb_to_hsl(0, 0, 255) == (240, 100, 50)        # Blue
    assert rgb_to_hsl(255, 255, 0) == (60, 100, 50)       # Yellow
    assert rgb_to_hsl(128, 0, 128) == (300, 100, 25)      # Purple


# Testing rgb_to_hsv function
def test_rgb_to_hsv():
    assert rgb_to_hsv(255, 0, 0) == (0, 100, 100)         # Red
    assert rgb_to_hsv(0, 255, 0) == (120, 100, 100)       # Green
    assert rgb_to_hsv(0, 0, 255) == (240, 100, 100)       # Blue
    assert rgb_to_hsv(255, 255, 0) == (60, 100, 100)      # Yellow
    assert rgb_to_hsv(128, 0, 128) == (300, 100, 50)      # Purple

def test_invalid_rgb():
    # Test RGB values exceeding the 0-255 range
    with pytest.raises(ValueError):
        rgb_to_hex(256, 0, 0)  # Invalid R value
    # Test negative RGB values
    with pytest.raises(ValueError):
        rgb_to_hex(255, -1, 0)  # Invalid G value
    # Test non-integer RGB values
    with pytest.raises(ValueError):
        rgb_to_hex(255, 87.5, 0)  # Invalid G value (float)


def test_invalid_hex():
    # Test invalid hex string (non-hex characters)
    with pytest.raises(ValueError):
        hex_to_rgb("#ZZZZZZ")
    # Test invalid hex string (too short)
    with pytest.raises(ValueError):
        hex_to_rgb("#FFF")
    # Test invalid hex string (too long)
    with pytest.raises(ValueError):
        hex_to_rgb("#FFFFFFFFFF")


def test_invalid_cmyk():
    # Test CMYK values exceeding 1
    with pytest.raises(ValueError):
        cmyk_to_rgb(1.5, 0, 0, 0)  # Invalid C value
    # Test negative CMYK values
    with pytest.raises(ValueError):
        cmyk_to_rgb(0, -0.5, 0, 0)  # Invalid M value
    # Test non-numeric CMYK values
    with pytest.raises(ValueError):
        cmyk_to_rgb("0", 0, 0, 0)  # Invalid C value (string)


def test_invalid_hsl():
    # Test HSL values exceeding the hue range (0-360)
    with pytest.raises(ValueError):
        hsl_to_rgb(370, 100, 50)  # Invalid hue
    # Test saturation exceeding 100%
    with pytest.raises(ValueError):
        hsl_to_rgb(120, 150, 50)  # Invalid saturation
    # Test lightness exceeding 100%
    with pytest.raises(ValueError):
        hsl_to_rgb(120, 100, 150)  # Invalid lightness


def test_invalid_hsv():
    # Test HSV values exceeding the hue range (0-360)
    with pytest.raises(ValueError):
        hsv_to_rgb(400, 100, 100)  # Invalid hue
    # Test saturation exceeding 100%
    with pytest.raises(ValueError):
        hsv_to_rgb(120, 200, 100)  # Invalid saturation
    # Test value exceeding 100%
    with pytest.raises(ValueError):
        hsv_to_rgb(120, 100, 200)  # Invalid value


def test_edge_case_colors():
    # Testing HSL to RGB edge cases
    assert hsl_to_rgb(0, 0, 0) == (0, 0, 0)  # Black
    assert hsl_to_rgb(0, 0, 100) == (255, 255, 255)  # White
    assert hsl_to_rgb(0, 0, 50) == (128, 128, 128)  # Gray
    assert hsl_to_rgb(0, 100, 50) == (255, 0, 0)  # Pure red
    assert hsl_to_rgb(120, 100, 50) == (0, 255, 0)  # Pure green
    assert hsl_to_rgb(240, 100, 50) == (0, 0, 255)  # Pure blue

    # Testing HSV to RGB edge cases
    assert hsv_to_rgb(0, 0, 0) == (0, 0, 0)  # Black
    assert hsv_to_rgb(0, 0, 100) == (255, 255, 255)  # White
    assert hsv_to_rgb(0, 0, 50) == (128, 128, 128)  # Gray
    assert hsv_to_rgb(0, 100, 100) == (255, 0, 0)  # Pure red
    assert hsv_to_rgb(120, 100, 100) == (0, 255, 0)  # Pure green
    assert hsv_to_rgb(240, 100, 100) == (0, 0, 255)  # Pure blue

    # Testing CMYK to RGB edge cases
    assert cmyk_to_rgb(0, 0, 0, 1) == (0, 0, 0)  # Black
    assert cmyk_to_rgb(0, 0, 0, 0) == (255, 255, 255)  # White
    assert cmyk_to_rgb(0, 0, 0, 0.5) == (128, 128, 128)  # Gray
    assert cmyk_to_rgb(0, 1, 1, 0) == (255, 0, 0)  # Pure red
    assert cmyk_to_rgb(1, 0, 1, 0) == (0, 255, 0)  # Pure green
    assert cmyk_to_rgb(1, 1, 0, 0) == (0, 0, 255)  # Pure blue

    # Testing RGB to HEX edge cases
    assert rgb_to_hex(0, 0, 0) == "#000000"  # Black
    assert rgb_to_hex(255, 255, 255) == "#FFFFFF"  # White
    assert rgb_to_hex(128, 128, 128) == "#808080"  # Gray
    assert rgb_to_hex(255, 0, 0) == "#FF0000"  # Pure red
    assert rgb_to_hex(0, 255, 0) == "#00FF00"  # Pure green
    assert rgb_to_hex(0, 0, 255) == "#0000FF"  # Pure blue

    # Testing HEX to RGB edge cases
    assert hex_to_rgb("#000000") == (0, 0, 0)  # Black
    assert hex_to_rgb("#FFFFFF") == (255, 255, 255)  # White
    assert hex_to_rgb("#808080") == (128, 128, 128)  # Gray
    assert hex_to_rgb("#FF0000") == (255, 0, 0)  # Pure red
    assert hex_to_rgb("#00FF00") == (0, 255, 0)  # Pure green
    assert hex_to_rgb("#0000FF") == (0, 0, 255)  # Pure blue

    # Testing RGB to HSL edge cases
    assert rgb_to_hsl(0, 0, 0) == (0, 0, 0)  # Black
    assert rgb_to_hsl(255, 255, 255) == (0, 0, 100)  # White
    assert rgb_to_hsl(128, 128, 128) == (0, 0, 50)  # Gray
    assert rgb_to_hsl(255, 0, 0) == (0, 100, 50)  # Pure red
    assert rgb_to_hsl(0, 255, 0) == (120, 100, 50)  # Pure green
    assert rgb_to_hsl(0, 0, 255) == (240, 100, 50)  # Pure blue

    # Testing RGB to HSV edge cases
    assert rgb_to_hsv(0, 0, 0) == (0, 0, 0)  # Black
    assert rgb_to_hsv(255, 255, 255) == (0, 0, 100)  # White
    assert rgb_to_hsv(128, 128, 128) == (0, 0, 50)  # Gray
    assert rgb_to_hsv(255, 0, 0) == (0, 100, 100)  # Pure red
    assert rgb_to_hsv(0, 255, 0) == (120, 100, 100)  # Pure green
    assert rgb_to_hsv(0, 0, 255) == (240, 100, 100)  # Pure blue

    # Testing RGB to CMYK edge cases
    assert rgb_to_cmyk(0, 0, 0) == (0, 0, 0, 1)  # Black
    assert rgb_to_cmyk(255, 255, 255) == (0, 0, 0, 0)  # White
    assert rgb_to_cmyk(128, 128, 128) == (0, 0, 0, 0.5)  # Gray
    assert rgb_to_cmyk(255, 0, 0) == (0, 1, 1, 0)  # Pure red
    assert rgb_to_cmyk(0, 255, 0) == (1, 0, 1, 0)  # Pure green
    assert rgb_to_cmyk(0, 0, 255) == (1, 1, 0, 0)  # Pure blue


def test_boundary_values():
    # Test RGB to CMYK boundary values
    assert rgb_to_cmyk(0, 0, 0) == (0, 0, 0, 1)  # Black
    assert rgb_to_cmyk(255, 255, 255) == (0, 0, 0, 0)  # White
    assert rgb_to_cmyk(255, 0, 0) == (0, 1, 1, 0)  # Red
    assert rgb_to_cmyk(0, 255, 0) == (1, 0, 1, 0)  # Green
    assert rgb_to_cmyk(0, 0, 255) == (1, 1, 0, 0)  # Blue

    # Test HSL to RGB boundary values
    assert hsl_to_rgb(0, 100, 50) == (255, 0, 0)  # Red (hue wraps around at 0)
    assert hsl_to_rgb(120, 100, 50) == (0, 255, 0)  # Green
    assert hsl_to_rgb(240, 100, 50) == (0, 0, 255)  # Blue
    assert hsl_to_rgb(60, 100, 50) == (255, 255, 0)  # Yellow
    assert hsl_to_rgb(300, 100, 50) == (255, 0, 255)  # Magenta
    assert hsl_to_rgb(180, 100, 50) == (0, 255, 255)  # Cyan

    # Test HSV to RGB boundary values
    assert hsv_to_rgb(0, 100, 100) == (255, 0, 0)  # Red
    assert hsv_to_rgb(120, 100, 100) == (0, 255, 0)  # Green
    assert hsv_to_rgb(240, 100, 100) == (0, 0, 255)  # Blue
    assert hsv_to_rgb(60, 100, 100) == (255, 255, 0)  # Yellow
    assert hsv_to_rgb(300, 100, 100) == (255, 0, 255)  # Magenta
    assert hsv_to_rgb(180, 100, 100) == (0, 255, 255)  # Cyan

    # Test RGB to HEX boundary values
    assert rgb_to_hex(0, 0, 0) == "#000000"  # Black
    assert rgb_to_hex(255, 255, 255) == "#FFFFFF"  # White
    assert rgb_to_hex(255, 0, 0) == "#FF0000"  # Red
    assert rgb_to_hex(0, 255, 0) == "#00FF00"  # Green
    assert rgb_to_hex(0, 0, 255) == "#0000FF"  # Blue

    # Test HEX to RGB boundary values
    assert hex_to_rgb("#000000") == (0, 0, 0)  # Black
    assert hex_to_rgb("#FFFFFF") == (255, 255, 255)  # White
    assert hex_to_rgb("#FF0000") == (255, 0, 0)  # Red
    assert hex_to_rgb("#00FF00") == (0, 255, 0)  # Green
    assert hex_to_rgb("#0000FF") == (0, 0, 255)  # Blue

    # Test CMYK to RGB boundary values
    assert cmyk_to_rgb(0, 0, 0, 1) == (0, 0, 0)  # Black
    assert cmyk_to_rgb(0, 0, 0, 0) == (255, 255, 255)  # White
    assert cmyk_to_rgb(0, 1, 1, 0) == (255, 0, 0)  # Red
    assert cmyk_to_rgb(1, 0, 1, 0) == (0, 255, 0)  # Green
    assert cmyk_to_rgb(1, 1, 0, 0) == (0, 0, 255)  # Blue

    # Test RGB to HSL boundary values
    assert rgb_to_hsl(0, 0, 0) == (0, 0, 0)  # Black
    assert rgb_to_hsl(255, 255, 255) == (0, 0, 100)  # White
    assert rgb_to_hsl(255, 0, 0) == (0, 100, 50)  # Red
    assert rgb_to_hsl(0, 255, 0) == (120, 100, 50)  # Green
    assert rgb_to_hsl(0, 0, 255) == (240, 100, 50)  # Blue

    # Test RGB to HSV boundary values
    assert rgb_to_hsv(0, 0, 0) == (0, 0, 0)  # Black
    assert rgb_to_hsv(255, 255, 255) == (0, 0, 100)  # White
    assert rgb_to_hsv(255, 0, 0) == (0, 100, 100)  # Red
    assert rgb_to_hsv(0, 255, 0) == (120, 100, 100)  # Green
    assert rgb_to_hsv(0, 0, 255) == (240, 100, 100)  # Blue


def test_round_trip_rgb_hsl():
    # Test for RGB -> HSL -> RGB
    test_cases_rgb_hsl = [
        (255, 87, 51),  # Orange shade
        (0, 0, 0),  # Black
        (255, 255, 255),  # White
        (128, 128, 128),  # Gray
        (0, 255, 0),  # Green
    ]

    for rgb in test_cases_rgb_hsl:
        hsl = rgb_to_hsl(*rgb)
        rgb_converted_back = hsl_to_rgb(*hsl)
        assert rgb_converted_back == pytest.approx(rgb, abs=1)


def test_round_trip_hsl_rgb():
    # Test for HSL -> RGB -> HSL
    test_cases_hsl_rgb = [
        (0, 100, 50),  # Red
        (120, 100, 50),  # Green
        (240, 100, 50),  # Blue
        (60, 100, 50),  # Yellow
        (300, 100, 50),  # Magenta
    ]

    for hsl in test_cases_hsl_rgb:
        rgb = hsl_to_rgb(*hsl)
        hsl_converted_back = rgb_to_hsl(*rgb)
        assert hsl_converted_back == pytest.approx(hsl, abs=1)


def test_round_trip_rgb_hex():
    # Test for RGB -> HEX -> RGB
    test_cases_rgb_hex = [
        (255, 87, 51),  # Orange shade
        (0, 0, 0),  # Black
        (255, 255, 255),  # White
        (128, 0, 128),  # Purple
        (0, 255, 255),  # Cyan
    ]

    for rgb in test_cases_rgb_hex:
        hex_value = rgb_to_hex(*rgb)
        rgb_converted_back = hex_to_rgb(hex_value)
        assert rgb_converted_back == pytest.approx(rgb, abs=1)


def test_round_trip_rgb_hsv():
    # Test for RGB -> HSV -> RGB
    test_cases_rgb_hsv = [
        (255, 87, 51),  # Orange shade
        (0, 0, 0),  # Black
        (255, 255, 255),  # White
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
    ]

    for rgb in test_cases_rgb_hsv:
        hsv = rgb_to_hsv(*rgb)
        rgb_converted_back = hsv_to_rgb(*hsv)
        assert rgb_converted_back == pytest.approx(rgb, abs=1)


def test_round_trip_hsv_rgb():
    # Test for HSV -> RGB -> HSV
    test_cases_hsv_rgb = [
        (0, 100, 100),  # Red
        (120, 100, 100),  # Green
        (240, 100, 100),  # Blue
        (60, 100, 100),  # Yellow
        (300, 100, 100),  # Magenta
    ]

    for hsv in test_cases_hsv_rgb:
        rgb = hsv_to_rgb(*hsv)
        hsv_converted_back = rgb_to_hsv(*rgb)
        assert hsv_converted_back == pytest.approx(hsv, abs=1)


def test_round_trip_rgb_cmyk():
    # Test for RGB -> CMYK -> RGB
    test_cases_rgb_cmyk = [
        (255, 87, 51),  # Orange shade
        (0, 0, 0),  # Black
        (255, 255, 255),  # White
        (0, 255, 0),  # Green
        (255, 255, 0),  # Yellow
    ]

    for rgb in test_cases_rgb_cmyk:
        cmyk = rgb_to_cmyk(*rgb)
        rgb_converted_back = cmyk_to_rgb(*cmyk)
        assert rgb_converted_back == pytest.approx(rgb, abs=1)


def test_round_trip_cmyk_rgb():
    # Test for CMYK -> RGB -> CMYK
    test_cases_cmyk_rgb = [
        (0, 0, 0, 1),  # Black
        (0, 0, 0, 0),  # White
        (0, 1, 1, 0),  # Red
        (1, 0, 1, 0),  # Green
        (1, 1, 0, 0),  # Blue
    ]

    for cmyk in test_cases_cmyk_rgb:
        rgb = cmyk_to_rgb(*cmyk)
        cmyk_converted_back = rgb_to_cmyk(*rgb)
        assert cmyk_converted_back == pytest.approx(cmyk, abs=0.01)


def test_round_trip_hex_rgb():
    # Test for HEX -> RGB -> HEX
    test_cases_hex_rgb = [
        "#000000",  # Black
        "#FFFFFF",  # White
        "#FF0000",  # Red
        "#00FF00",  # Green
        "#0000FF",  # Blue
    ]

    for hex_value in test_cases_hex_rgb:
        rgb = hex_to_rgb(hex_value)
        hex_converted_back = rgb_to_hex(*rgb)
        assert hex_converted_back == hex_value.upper()
