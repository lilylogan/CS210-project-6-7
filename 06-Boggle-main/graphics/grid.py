"""
Grid display.  

Displays a rectangular grid of cells, organized in rows and columns
with row 0 at the top and growing down, column 0 at the left and 
growing to the right.  A sequence of unique colors for cells can 
be chosen from a color wheel, in addition to colors 'black' and 'white'
which do not appear in the color wheel. 

Michal Young (michal@cs.uoregon.edu), October 2012, 
for CIS 210 at University of Oregon

2022-10-28 Modify to return created graphic objects so that they can be
modified rather than abandoned.  Although the prior version was working,
it could create a large number of invisible (obscured) rectangles and texts
as filling or re-labeling a tile just drew a new one atop it.

Uses the simple graphics module provided by Zelle, which in turn 
is built on the Tk graphics package (and which should therefore be 
available on all major Python platforms, including Linux, Mac, and 
all flavors of Windows at least back to XP). 
"""
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.WARN)

from graphics.graphics import *    # Zelle's simple OO graphics

global win  # The window we are drawing the grid in
global cell_width, cell_height  # The size of a cell in the grid

global color_wheel
color_wheel = [  color_rgb(255,0,0), color_rgb(0,255,0), color_rgb(0,0,255),
                        color_rgb(255,255,0), color_rgb(255,0,255), color_rgb(0,255,255),
                        color_rgb(127,255,0), color_rgb(0,127,255), color_rgb(127,0,255),
                        color_rgb(255,127,0), color_rgb(0,255,127), color_rgb(255,0,127),
                        color_rgb(127,127,0), color_rgb(127,0,127), color_rgb(0,127,127),
                        color_rgb(255,255,127), color_rgb(255,127,255), color_rgb(127,255,255) ]
global cur_color
cur_color = 0
global black, white, red, green, blue
black = color_rgb(0,0,0)
white = color_rgb(255,255,255)
red = color_rgb(200,0,0)
green = color_rgb(0,200,0)
blue = color_rgb(0,0,200)
tile_background = color_rgb(165, 205, 255)
tile_accent_background = color_rgb(255, 255, 11)
global nrows
nrows = 1

class Grid:
    """Visual display of the grid"""

    def __init__(self, rows: int, cols: int, width_px: int = 500, height_px: int = 500,
                 title: str = "Grid", cell_margin_px: int = 5) :
        """Create and show the grid display, initially all white.
        rows, cols are the grid size in rows and columns.
        width, height are the window size in pixels.
        """
        log.debug("Creating grid")
        self.win = GraphWin("Grid", width_px, height_px)
        self.bkgrnd = Rectangle( Point(0,0), Point(width_px,height_px) )
        self.bkgrnd.setFill( color_rgb(231,231,231) ) # Grey background
        self.cell_width = width_px / cols
        self.cell_height = height_px / rows
        self.bkgrnd.draw(self.win)
        # Representation of each cell in the grid, and its label
        self._make_cells(rows, cols, cell_margin_px)
        log.debug('Created grid')

    def _make_cells(self, rows: int, cols: int, margin_px: int):
        """Create self.cells, depiction of each cell in the grid.
        Each cell is (rect, label), but label is initially None.
        Initially white cell with black boarder and no label.
        """
        self.cells = []
        for row_i in range(rows):
            row = []
            for col_i in range(cols):
                # Keep coordinates in pixels so that we can pad the margins
                left = col_i * self.cell_width
                right = (col_i + 1) * self.cell_width
                top = row_i * self.cell_height
                bottom = top + self.cell_height
                cell = Rectangle(Point(left + margin_px, bottom - margin_px),
                                 Point(right - margin_px, top + margin_px))
                cell.setFill(white)
                cell.setOutline(black)
                cell.draw(self.win)
                row.append((cell, None))
            self.cells.append(row)

    def fill_cell(self, row: int, col: int, color=white):
        """Fill cell[row,col] with color."""
        tile, label = self.cells[row][col]
        tile.setFill(color)
        # tile.draw(self.win)
        # if label:
        #    label.draw(self.win)

    def label_cell(self, row: int, col: int, text: str, color=black):
        """Place text label on cell[row,col]."""
        tile, _ = self.cells[row][col]
        ll, ur = tile.p1, tile.p2
        x_center = (ll.x + ur.x) / 2.0
        y_center = (ll.y + ur.y) / 2.0
        label = Text(Point(x_center, y_center), text)
        label.setFace("helvetica")
        label.setSize(20)  ## Is there a better way to choose text size?
        label.setFill(color)
        label.draw(self.win)
        self.cells[row][col] = (tile, label)

def get_cur_color():
    """Return the currently chosen color in the color wheel.  
    
    The color wheel is a list of colors selected to be contrast with each other. 
    The first few entries are bright primary colors; as we cycle through the color
    wheel, contrast becomes less, but colors should remain distinct to those with 
    normal color vision until the color wheel cycles all the way around in 18 
    choices and starts recycling previously used colors.   The color wheel starts
    out in position 0, so get_cur_color() may be called before get_next_color() has 
    been called. 
    
    Args:  none
    Returns:  
        a 'color' that can be passed to fill_cell
        
    FIXME: The color wheel should produce colors of contrasting brightness
    as well as hue, to maximize distinctness for dichromats (people with 
    "color blindness".  Maybe generating a good color wheel can be part of a 
    project later in CIS 210.   (This is not a required or expected change 
    for the week 4 project.) 
    """
    return color_wheel[cur_color]

def get_next_color():
    """Advance the color wheel, returning the next available color. 
    
    The color wheel is a list of colors selected to be contrast with each other. 
    The first few entries are bright primary colors; as we cycle through the color
    wheel, contrast becomes less, but colors should remain distinct to those with 
    normal color vision until the color wheel cycles all the way around in 18 
    choices and starts recycling previously used colors. 
    
    Args:  none
    Returns:  
        a 'color' that can be passed to fill_cell    
    """
    global cur_color
    cur_color += 1
    if cur_color >= len(color_wheel) :
        cur_color = 0
    return color_wheel[cur_color]





