def rgb_to_hex(r, g, b):
    """
    Convert RGB to hex.

    Parameters:
    r (int): Red value (0-255)
    g (int): Green value (0-255)
    b (int): Blue value (0-255)

    Returns:
    str: Hex representation of the color in the format #RRGGBB.

    Raises:
    ValueError: If any of the RGB values are outside the 0-255 range.
    """
    # Validate that RGB values are within the 0-255 range
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(f"Invalid RGB value: ({r}, {g}, {b}). Each value must be between 0 and 255.")

    return '#{:02x}{:02x}{:02x}'.format(r, g, b).upper()


def hex_to_rgb(hex_value):
    """
    Convert a hex color to RGB. This is useful for colorizing colors that are in the format #RRGGBB.

    Parameters:
    hex_value (str): The hex color string, must start with '#' and be 7 characters long (#RRGGBB).

    Returns:
    (int, int, int): Corresponding RGB values (0-255 for each channel).

    Raises:
    ValueError: If the input is not a valid hex color string.
    """
    hex_value = hex_value.lstrip('#')

    # Validate length (must be 6 characters for RRGGBB)
    if len(hex_value) != 6:
        raise ValueError(f"Invalid hex color: {hex_value}. Must be 6 characters long.")

    # Validate that the hex string contains only valid hexadecimal characters
    try:
        int(hex_value, 16)
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_value}. Contains non-hexadecimal characters.")

    return tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))


def cmyk_to_rgb(c, m, y, k):
    """
    Convert CMYK to RGB.

    Parameters:
    c (float): Cyan value (0-1)
    m (float): Magenta value (0-1)
    y (float): Yellow value (0-1)
    k (float): Black value (0-1)

    Returns:
    (int, int, int): Corresponding RGB values (0-255 for each channel).

    Raises:
    ValueError: If any of the CMYK values are outside the range [0, 1] or are non-numeric.
    """
    # Ensure the values are numeric
    if not all(isinstance(i, (int, float)) for i in [c, m, y, k]):
        raise ValueError(f"Invalid CMYK value: ({c}, {m}, {y}, {k}). All values must be numeric.")

    # Validate that CMYK values are between 0 and 1
    if not (0 <= c <= 1 and 0 <= m <= 1 and 0 <= y <= 1 and 0 <= k <= 1):
        raise ValueError(f"Invalid CMYK value: ({c}, {m}, {y}, {k}). Each value must be between 0 and 1.")

    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return int(round(r)), int(round(g)), int(round(b))


def hsl_to_rgb(h, s, l):
    """
    Convert HSL to RGB color.

    Parameters:
    h (float): Hue value, range [0, 360)
    s (float): Saturation value, range [0, 100]
    l (float): Lightness value, range [0, 100]

    Returns:
    (int, int, int): Corresponding RGB values (0-255 for each channel).

    Raises:
    ValueError: If HSL values are out of range.
    """
    # Validate HSL values
    if not (0 <= h < 360):
        raise ValueError(f"Invalid hue value: {h}. Hue must be in the range [0, 360).")
    if not (0 <= s <= 100):
        raise ValueError(f"Invalid saturation value: {s}. Saturation must be in the range [0, 100].")
    if not (0 <= l <= 100):
        raise ValueError(f"Invalid lightness value: {l}. Lightness must be in the range [0, 100].")

    # Normalize s and l to [0, 1]
    s /= 100
    l /= 100
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    # Lookup table for determining RGB base values based on hue
    rgb_base = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)]

    # Find the correct base values based on the hue range
    rgb = rgb_base[int(h // 60)]

    # Calculate final RGB values and convert to 0-255 range
    r, g, b = [(val + m) * 255 for val in rgb]

    return int(round(r)), int(round(g)), int(round(b))


def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB color.

    Parameters:
    h (float): Hue value, range [0, 360)
    s (float): Saturation value, range [0, 100]
    v (float): Value (brightness) value, range [0, 100]

    Returns:
    (int, int, int): Corresponding RGB values (0-255 for each channel).

    Raises:
    ValueError: If HSV values are out of range.
    """
    # Validate HSV values
    if not (0 <= h < 360):
        raise ValueError(f"Invalid hue value: {h}. Hue must be in the range [0, 360).")
    if not (0 <= s <= 100):
        raise ValueError(f"Invalid saturation value: {s}. Saturation must be in the range [0, 100].")
    if not (0 <= v <= 100):
        raise ValueError(f"Invalid value (brightness) value: {v}. Value must be in the range [0, 100].")

    # Normalize s and v to [0, 1]
    s /= 100
    v /= 100
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    # Lookup table for determining RGB base values based on hue
    rgb_base = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)]

    # Find the correct base values based on the hue range
    rgb = rgb_base[int(h // 60)]

    # Calculate final RGB values and convert to 0-255 range
    r, g, b = [(val + m) * 255 for val in rgb]

    return int(round(r)), int(round(g)), int(round(b))


def rgb_to_cmyk(r, g, b):
    # Normalize RGB values to the range 0-1
    r_prime = r / 255.0
    g_prime = g / 255.0
    b_prime = b / 255.0

    # Calculate K (black key)
    k = 1 - max(r_prime, g_prime, b_prime)

    if k == 1:  # If black is 100%
        return 0, 0, 0, 1

    # Calculate CMY values
    c = (1 - r_prime - k) / (1 - k)
    m = (1 - g_prime - k) / (1 - k)
    y = (1 - b_prime - k) / (1 - k)

    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)

def rgb_to_hsl(r, g, b):
    """
     Convert RGB to HSL. This is a helper function for : func : ` color_to_rgb `.
     
     @param r - Red component in 0 - 255. Must be between 0 and 1.
     @param g - Green component in 0 - 255. Must be between 0 and 1.
     @param b - Blue component in 0 - 255. Must be between 0 and 1.
     
     @return Hue Saturation Luminosity ( 0 - 100
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    l = (max_color + min_color) / 2
    # Returns the color in the range 0.. 1.
    if max_color == min_color:
        h = s = 0
    else:
        d = max_color - min_color
        s = d / (2 - max_color - min_color) if l > 0.5 else d / (max_color + min_color)
        # color range in the range 0.. 1
        if max_color == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_color == g:
            h = (b - r) / d + 2
        elif max_color == b:
            h = (r - g) / d + 4
        h /= 6
    return round(h * 360), round(s * 100), round(l * 100)

def rgb_to_hsv(r, g, b):
    """
     Convert RGB to HSV. This is a helper function for : func : ` color_to_hsv `.
     
     @param r - Red component in 0 - 255. Must be between 0 and 255 inclusive.
     @param g - Green component in 0 - 255. Must be between 0 and 255 inclusive.
     @param b - Blue component in 0 - 255. Must be between 0 and 255 inclusive.
     
     @return HSV value in range 0 - 360 s -
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    v = max_color
    d = max_color - min_color
    s = 0 if max_color == 0 else d / max_color
    # Horizontally the color of the color range.
    if max_color == min_color:
        h = 0
    else:
        # color range in the range 0.. 1
        if max_color == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_color == g:
            h = (b - r) / d + 2
        elif max_color == b:
            h = (r - g) / d + 4
        h /= 6
    return round(h * 360), round(s * 100), round(v * 100)
