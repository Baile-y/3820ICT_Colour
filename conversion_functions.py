def rgb_to_hex(r, g, b):
    """
     Convert RGB to hex. This is used to create a color string that can be used in a Gnuplot plot
     
     @param r - Red component in 0 - 255
     @param g - Green component in 0 - 255 ( inclusive )
     @param b - Blue component in 0 - 255 ( inclusive )
     
     @return Hex representation of the color in the format #RRGGB
    """
    return '#{:02x}{:02x}{:02x}'.format(r, g, b).upper()

def hex_to_rgb(hex):
    """
     Convert a hex color to RGB. This is useful for colorizing colors that are in the format #RRGGBB.
     
     @param hex - The hex color to convert. Must be in the format #RRGGBB.
     
     @return A tuple of RGB values ( 0 - 255 )
    """
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def cmyk_to_rgb(c, m, y, k):
    """
     Convert CMYK color to RGB. This is a function to convert CMYK values to RGB values
     
     @param c - Cmyk value 0 - 255
     @param m - Mmyk value 0 - 255 ( opacity )
     @param y - Yanimacro value 0 - 255 ( opacity )
     @param k - CMYK value 0 - 255 ( opacity )
     
     @return RGB values as int ( r g b ) where r g
    """
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return round(r), round(g), round(b)

def hsl_to_rgb(h, s, l):
    """
    Convert HSL to RGB color.
    
    Parameters:
    h (float): Hue value, range [0, 360).
    s (float): Saturation value, range [0, 100].
    l (float): Lightness value, range [0, 100].
    
    Returns:
    (int, int, int): Corresponding RGB values (0-255 for each channel).
    """
    s = s / 100.0
    l = l / 100.0
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x
    else:
        r, g, b = 0, 0, 0
    
    r = (r + m) * 255
    g = (g + m) * 255
    b = (b + m) * 255
    
    return int(round(r)), int(round(g)), int(round(b))

def hsv_to_rgb(h, s, v):
    """
     Convert HSV to RGB. This is based on code from pyglet.
     
     @param h - Hue as a float between 0 and 360
     @param s - Saturation as a float between 0 and 100
     @param v - Value as a float between 0 and 100 ( inclusive )
     
     @return A tuple of ( r g b ) where r g
    """
    h = h / 360.0
    s = s / 100.0
    v = v / 100.0
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    # If i is 0 return the current value.
    if i == 0: r, g, b = v, t, p
    # if i 1 return r g b q q v p
    if i == 1: r, g, b = q, v, p
    # if i 2 r g b p v t
    if i == 2: r, g, b = p, v, t
    # if i 3 return r g b q v
    if i == 3: r, g, b = p, q, v
    # if i 4 r g b p v
    if i == 4: r, g, b = t, p, v
    # if i 5 r g b q
    if i == 5: r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)


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
