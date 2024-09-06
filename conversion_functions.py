# Helper Functions for Validation
def validate_rgb(r, g, b):
    """
    Validate RGB values to ensure they are between 0 and 255.

    Parameters:
    r, g, b (int): Red, green, and blue values.

    Raises:
    ValueError: If any of the RGB values are out of the valid range.
    """
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(f"Invalid RGB value: ({r}, {g}, {b}). Each value must be between 0 and 255.")

def validate_hsl(h, s, l):
    """
    Validate HSL values to ensure hue is between 0 and 360, and saturation and lightness are between 0 and 100.

    Parameters:
    h (float): Hue value.
    s, l (float): Saturation and lightness values.

    Raises:
    ValueError: If any of the HSL values are out of range.
    """
    if not (0 <= h < 360):
        raise ValueError(f"Invalid hue value: {h}. Must be in the range [0, 360).")
    if not (0 <= s <= 100):
        raise ValueError(f"Invalid saturation value: {s}. Must be in the range [0, 100].")
    if not (0 <= l <= 100):
        raise ValueError(f"Invalid lightness value: {l}. Must be in the range [0, 100].")

def validate_hsv(h, s, v):
    """
    Validate HSV values to ensure hue is between 0 and 360, and saturation and value are between 0 and 100.

    Parameters:
    h (float): Hue value.
    s, v (float): Saturation and value values.

    Raises:
    ValueError: If any of the HSV values are out of range.
    """
    if not (0 <= h < 360):
        raise ValueError(f"Invalid hue value: {h}. Must be in the range [0, 360).")
    if not (0 <= s <= 100):
        raise ValueError(f"Invalid saturation value: {s}. Must be in the range [0, 100].")
    if not (0 <= v <= 100):
        raise ValueError(f"Invalid value: {v}. Must be in the range [0, 100].")

def validate_cmyk(c, m, y, k):
    """
    Validate CMYK values to ensure all values are between 0 and 1.

    Parameters:
    c, m, y, k (float): Cyan, magenta, yellow, and black values.

    Raises:
    ValueError: If any of the CMYK values are out of range or non-numeric.
    """
    if not all(isinstance(i, (int, float)) for i in [c, m, y, k]):
        raise ValueError(f"Invalid CMYK value: ({c}, {m}, {y}, {k}). All values must be numeric.")
    if not (0 <= c <= 1 and 0 <= m <= 1 and 0 <= y <= 1 and 0 <= k <= 1):
        raise ValueError(f"Invalid CMYK value: ({c}, {m}, {y}, {k}). Each value must be between 0 and 1.")

# RGB to HEX
def rgb_to_hex(r, g, b):
    """
    Convert RGB to hex.

    Parameters:
    r, g, b (int): RGB values (0-255).

    Returns:
    str: Hexadecimal color string in the format #RRGGBB.
    """
    validate_rgb(r, g, b)
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

# HEX to RGB
def hex_to_rgb(hex_value):
    """
    Convert hex to RGB.

    Parameters:
    hex_value (str): Hexadecimal string (#RRGGBB).

    Returns:
    tuple: Corresponding RGB values (0-255).
    """
    hex_value = hex_value.lstrip('#')
    if len(hex_value) != 6:
        raise ValueError(f"Invalid hex color: {hex_value}. Must be 6 characters long.")
    try:
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_value}. Contains non-hexadecimal characters.")

# CMYK to RGB
def cmyk_to_rgb(c, m, y, k):
    """
    Convert CMYK to RGB.

    Parameters:
    c, m, y, k (float): CMYK values (0-1).

    Returns:
    tuple: Corresponding RGB values (0-255).
    """
    validate_cmyk(c, m, y, k)
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(round(r)), int(round(g)), int(round(b))

# HSL to RGB
def hsl_to_rgb(h, s, l):
    """
    Convert HSL to RGB.

    Parameters:
    h (float): Hue value (0-360).
    s, l (float): Saturation and lightness values (0-100).

    Returns:
    tuple: Corresponding RGB values (0-255).
    """
    validate_hsl(h, s, l)
    s /= 100
    l /= 100
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    rgb_base = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)]
    rgb = rgb_base[int(h // 60)]
    r, g, b = [(val + m) * 255 for val in rgb]
    return int(round(r)), int(round(g)), int(round(b))

# HSV to RGB
def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB.

    Parameters:
    h (float): Hue value (0-360).
    s, v (float): Saturation and value values (0-100).

    Returns:
    tuple: Corresponding RGB values (0-255).
    """
    validate_hsv(h, s, v)
    s /= 100
    v /= 100
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    rgb_base = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)]
    rgb = rgb_base[int(h // 60)]
    r, g, b = [(val + m) * 255 for val in rgb]
    return int(round(r)), int(round(g)), int(round(b))

# RGB to CMYK
def rgb_to_cmyk(r, g, b):
    """
    Convert RGB to CMYK.

    Parameters:
    r, g, b (int): RGB values (0-255).

    Returns:
    tuple: Corresponding CMYK values (0-1).
    """
    validate_rgb(r, g, b)
    r_prime, g_prime, b_prime = r / 255.0, g / 255.0, b / 255.0
    k = 1 - max(r_prime, g_prime, b_prime)
    if k == 1:
        return 0, 0, 0, 1
    c = (1 - r_prime - k) / (1 - k)
    m = (1 - g_prime - k) / (1 - k)
    y = (1 - b_prime - k) / (1 - k)
    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)

# RGB to HSL
def rgb_to_hsl(r, g, b):
    """
    Convert RGB to HSL.

    Parameters:
    r, g, b (int): RGB values (0-255).

    Returns:
    tuple: Corresponding HSL values (0-360, 0-100, 0-100).
    """
    validate_rgb(r, g, b)
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_color, min_color = max(r, g, b), min(r, g, b)
    l = (max_color + min_color) / 2
    if max_color == min_color:
        h = s = 0
    else:
        d = max_color - min_color
        s = d / (2 - max_color - min_color) if l > 0.5 else d / (max_color + min_color)
        if max_color == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_color == g:
            h = (b - r) / d + 2
        elif max_color == b:
            h = (r - g) / d + 4
        h /= 6
    return round(h * 360), round(s * 100), round(l * 100)

# RGB to HSV
def rgb_to_hsv(r, g, b):
    """
    Convert RGB to HSV.

    Parameters:
    r, g, b (int): RGB values (0-255).

    Returns:
    tuple: Corresponding HSV values (0-360, 0-100, 0-100).
    """
    validate_rgb(r, g, b)
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_color, min_color = max(r, g, b), min(r, g, b)
    v = max_color
    d = max_color - min_color
    s = 0 if max_color == 0 else d / max_color
    if max_color == min_color:
        h = 0
    else:
        if max_color == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_color == g:
            h = (b - r) / d + 2
        elif max_color == b:
            h = (r - g) / d + 4
        h /= 6
    return round(h * 360), round(s * 100), round(v * 100)
