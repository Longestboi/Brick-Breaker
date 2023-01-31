
import pygame as pg
import numpy

_col_val = [
    # Cyan         Orange         Green        Yellow
    (0, 255, 255), (255, 133, 0), (0, 255, 0), (255, 255, 0),
    # Red        Blue          Purple         White
    (255, 0, 0), (0, 52, 255), (220, 0, 255), (255, 255, 255),
    # Black
    (0, 0, 0)
]

    # Color dictionary, is there no better way of doing this? I don't know!
COLORS = {
    # Cyan
    0: _col_val[0], "cyan": _col_val[0],
    # Orange
    1: _col_val[1], "orange": _col_val[1],
    # Green
    2: _col_val[2], "green": _col_val[2],
    # Yellow
    3: _col_val[3], "yellow": _col_val[3],
    # Red
    4: _col_val[4], "red": _col_val[4],
    # Blue
    5: _col_val[5], "blue": _col_val[5],
    # Purple
    6: _col_val[6], "purple": _col_val[6],
    # White
    7: _col_val[7], "white": _col_val[7],
    # White
    8:  _col_val[8], "black": _col_val[8]
}

def overlay_color_on_surface(surface: pg.Surface, color: tuple, intensity: float) -> pg.Surface:
    """ Overlay tuple represented RGB value over pygame surface.

        Args:
            surface (Surface): Surface to be modified.
            color (tuple): Color to be applied to the inputed surface.
            intensity (float): Intensity of the applied color.

        Returns:
            Surface: Color overlayed surface.
    """
    src = pg.surfarray.pixels3d(surface)
    # Make destination
    dst = numpy.zeros(src.shape)

    # Apply color to destinaion
    dst[:] = color

    # Get the difference between the src and dest
    diff = (dst - src) * min(max(0, intensity), 1)

    # Add diff to src to get ovelayed color
    overlayed = src + diff.astype(numpy.uint)

    # Convert numpy array to surface
    return pg.surfarray.make_surface(overlayed)
