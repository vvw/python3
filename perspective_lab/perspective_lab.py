
##############
# image_mat_util.py

# Copyright 2013 Philip N. Klein
""" A module for working with images in matrix format.
    An image is represented by two matrices, representing points and colors.
    The points matrix has row labels {'x', 'y', 'u'} and column labels (0,0) through (w, h), inclusive,
    where (w, h) are the width and height of the original image
    The colors matrix has row labels {'r', 'g', 'b'} and column labels (0,0) through (w-h, h-1).

    The column labels for these matrices represent "lattice points" on the original image.
    For pixel (i,j) in the original image, the (i,j) column in the colors matrix represents
    the pixel color and the (i,j), (i+1, j), (i+1, j+1), and (i, j+1) columns in the points
    matrix represent the boundary of the pixel region
    """

import mat
import png
import numbers
import collections
import webbrowser
import tempfile
import os
import atexit
import math

# Round color coordinate to nearest int and clamp to [0, 255]
def _color_int(col):
    return max(min(round(col), 255), 0)

# utility conversions, between boxed pixel and flat pixel formats
# the png library uses flat, we use boxed.
def _boxed2flat(row):
    return [_color_int(x) for box in row for x in box]

def _flat2boxed(row):
    # Note we skip every 4th element, thus eliminating the alpha channel
    return [tuple(row[i:i+3]) for i in range(0, len(row), 4)]

## Image conversions
def isgray(image):
    "tests whether the image is grayscale"
    col = image[0][0]
    if isinstance(col, numbers.Number):
        return True
    elif isinstance(col, collections.Iterable) and len(col) == 3:
        return False
    else:
        raise TypeError('Unrecognized image type')

def color2gray(image):
    """ Converts a color image to grayscale """
    # we use HDTV grayscale conversion as per https://en.wikipedia.org/wiki/Grayscale
    return [[int(0.2126*p[0] + 0.7152*p[1] + 0.0722*p[2]) for p in row]
                                                          for row in image]

def gray2color(image):
    """ Converts a grayscale image to color """
    return [[(p,p,p) for p in row] for row in image]

#extracting and combining color channels
def rgbsplit(image):
    """ Converts an RGB image to a 3-element list of grayscale images, one for each color channel"""
    return [[[pixel[i] for pixel in row] for row in image] for i in (0,1,2)]

def rgpsplice(R,G,B):
    return [[(R[row][col],G[row][col],B[row][col]) for col in range(len(R[0]))] for row in range(len(R))]

## To and from files
def file2image(path):
    """ Reads an image into a list of lists of pixel values (tuples with
        three values). This is a color image. """
    (w, h, p, m) = png.Reader(filename = path).asRGBA() # force RGB and alpha
    return [_flat2boxed(r) for r in p]


def image2file(image, path):
    """ Writes an image in list of lists format to a file. Will work with
        either color or grayscale. """
    if isgray(image):
        img = gray2color(image)
    else:
        img = image
    with open(path, 'wb') as f:
        png.Writer(width=len(image[0]), height=len(image)).write(f,
            [_boxed2flat(r) for r in img])

## Display functions
def image2display(image, browser=None):
    """ Stores an image in a temporary location and displays it on screen
        using a web browser. """
    path = _create_temp('.png')
    image2file(image, path)
    hpath = _create_temp('.html')
    with open(hpath, 'w') as h:
        h.writelines(["<html><body><img src='file://%s'/></body></html>" % path])
    openinbrowser('file://%s' % hpath, browser)
    print("Hit Enter once the image is displayed.... ", end="")
    input()

_browser = None

def setbrowser(browser=None):
    """ Registers the given browser and saves it as the module default.
        This is used to control which browser is used to display the plot.
        The argument should be a value that can be passed to webbrowser.get()
        to obtain a browser.  If no argument is given, the default is reset
        to the system default.

        webbrowser provides some predefined browser names, including:
        'firefox'
        'opera'

        If the browser string contains '%s', it is interpreted as a literal
        browser command line.  The URL will be substituted for '%s' in the command.
        For example:
        'google-chrome %s'
        'cmd "start iexplore.exe %s"'

        See the webbrowser documentation for more detailed information.

        Note: Safari does not reliably work with the webbrowser module,
        so we recommend using a different browser.
    """
    global _browser
    if browser is None:
        _browser = None  # Use system default
    else:
        webbrowser.register(browser, None, webbrowser.get(browser))
        _browser = browser

def getbrowser():
    """ Returns the module's default browser """
    return _browser

def openinbrowser(url, browser=None):
    if browser is None:
        browser = _browser
    webbrowser.get(browser).open(url)

# Create a temporary file that will be removed at exit
# Returns a path to the file
def _create_temp(suffix='', prefix='tmp', dir=None):
    _f, path = tempfile.mkstemp(suffix, prefix, dir)
    os.close(_f)
    _remove_at_exit(path)
    return path

# Register a file to be removed at exit
def _remove_at_exit(path):
    atexit.register(os.remove, path)

def file2mat(path, row_labels = ('x', 'y', 'u')):
    """input: a filepath to an image in .png format
    output: the pair (points, matrix) of matrices representing the image."""
    return image2mat(file2image(path), row_labels)

def image2mat(img, row_labels = ('x', 'y', 'u')):
    """ input: an image in list-of-lists format
        output: a pair (points, colors) of matrices representing the image.
        Note: The input list-of-lists can consist of either integers n [0, 255] for grayscale
        or 3-tuple of integers representing the rgb color coordinates
    """
    h = len(img)
    w = len(img[0])
    rx, ry, ru = row_labels
    ptsD = (set(row_labels), {(x,y) for x in range(w+1) for y in range(h+1)})
    ptsF = {}
    colorsD = ({'r', 'g', 'b'}, {(x,y) for x in range(w) for y in range(h)})
    colorsF = {}
    for y in range(h+1):
        for x in range(w+1):
            pt = (x,y)
            ptsF[(rx, pt)] = x
            ptsF[(ry, pt)] = y
            ptsF[(ru, pt)] = 1
            if x < w and y < h:
                col = img[y][x]
                if type(col) is int:
                    red, green, blue = col, col, col
                else:
                    red, green, blue = col
                colorsF[('r', pt)] = red
                colorsF[('g', pt)] = green
                colorsF[('b', pt)] = blue
    return mat.Mat(ptsD, ptsF), mat.Mat(colorsD, colorsF)

def mat2display(pts, colors, row_labels = ('x', 'y', 'u'),
                scale=1, xscale=None, yscale = None, xmin=0, ymin=0, xmax=None, ymax=None,
                crosshairs=False, browser=None):
    """ input: matrix pts and matrix colors representing an image
        result: Displays the image in a web browser

        Optional arguments:

        row_labels - A collection specifying the points matrix row labels,
        in order.  The first element of this collection is considered the x
        coordinate, the second is the y coordinate, and the third is the u
        coordinate, which is assumed to be 1 for all points.

        scale - The display scale, in pixels per image coordinate unit
        xscale, yscale - in case you want to scale differently in x and y

        xmin, ymin, xmax, ymax - The region of the image to display.  These can
        be set to None to use the minimum/maximum value of the coordinate
        instead of a fixed value.

        crosshairs - Setting this to true displays a crosshairs at (0, 0) in
        image coordinates

        browser - A browser string to be passed to webbrowser.get().
        Overrides the module default, if any has been set.
    """
    if xscale == None: xscale = scale
    if yscale == None: yscale = scale

    rx, ry, ru = row_labels
    if ymin is None:
        ymin = min(v for (k, v) in pts.f.items() if k[0] == ry)
    if xmin is None:
        xmin = min(v for (k, v) in pts.f.items() if k[0] == rx)
    if ymax is None:
        ymax = max(v for (k, v) in pts.f.items() if k[0] == ry)
    if xmax is None:
        xmax = max(v for (k, v) in pts.f.items() if k[0] == rx)

    # Include (0, 0) in the region
    if crosshairs:
        ymin = min(ymin, 0)
        xmin = min(xmin, 0)
        ymax = max(ymax, 0)
        xmax = max(xmax, 0)


    #hpath = _create_temp('.html')
    hpath = './outtttttttttttttttttttttttt.html'
    with open(hpath, 'w') as h:
        h.writelines(
            ['<!DOCTYPE html>\n',
            '<head> <title>image</title> </head>\n',
            '<body>\n',
            '<svg height="%s" width="%s" xmlns="http://www.w3.org/2000/svg">\n' % ((ymax-ymin) * yscale, (xmax-xmin) * xscale),
            '<g transform="scale(%s) translate(%s, %s) ">\n' % (scale, -xmin, -ymin)])

        pixels = sorted(colors.D[1])
        Mx, My = pixels[-1]

        # go through the quads, writing each one to canvas
        for l in pixels:
            lx, ly = l
            r = _color_int(colors[('r', l)])
            g = _color_int(colors[('g', l)])
            b = _color_int(colors[('b', l)])

            mx = min(lx+1, Mx)+1
            my = min(ly+1, My)+1

            # coords of corners
            x0 = pts[(rx, l)]
            y0 = pts[(ry, l)]
            x1 = pts[(rx, (mx, ly))]
            y1 = pts[(ry, (mx, ly))]
            x2 = pts[(rx, (mx, my))]
            y2 = pts[(ry, (mx, my))]
            x3 = pts[(rx, (lx, my))]
            y3 = pts[(ry, (lx, my))]

            h.writelines(['<polygon points="%s, %s %s, %s, %s, %s %s, %s" fill="rgb(%s, %s, %s)" stroke="none" />\n'
                         % (x0, y0, x1, y1, x2, y2, x3, y3, r, g, b)])

        # Draw crosshairs centered at (0, 0)
        if crosshairs:
            h.writelines(
                ['<line x1="-50" y1="0" x2="50" y2="0" stroke="black" />\n',
                '<line x1="0" y1="-50" x2="0" y2="50" stroke="black" />\n',
                '<circle cx="0" cy="0" r="50" style="stroke: black; fill: none;" />\n'])

        h.writelines(['</g></svg>\n', '</body>\n', '</html>\n'])

    openinbrowser('file://%s' % hpath, browser)
    #print("Hit Enter once the image is displayed.... ", end="")
    #input()

# end of image_mat_util.py
##############

##############
# perspective_lab.py

# version code 7bdbe7c95e85+
coursera = 1
# Please fill out this stencil and submit using the provided submission script.

from vec import Vec
from mat import Mat
from matutil import rowdict2mat
from solver import solve



## 1: (Task 5.12.1) Move To Board
def move2board(y): 
    '''
    Input:
        - y: a Vec with domain {'y1','y2','y3'}, the coordinate representation in whiteboard coordinates of a point q
    Output:
        - A {'y1','y2','y3'}-Vec, the coordinate representation
          in whiteboard coordinates of the point p such that the line through the 
          origin and q intersects the whiteboard plane at p.
    '''
    return Vec({'y1','y2','y3'}, {'y1':y['y1']/y['y3'], 'y2':y['y2']/y['y3'], 'y3':y['y3']/y['y3'] })



## 2: () Make domain of vector
# D should be assigned the Cartesian product of R and C
D = {('y1', 'x1'), ('y1', 'x2'), ('y1', 'x3'), ('y2', 'x1'), ('y2', 'x2'), ('y2', 'x3'), ('y3', 'x1'), ('y3', 'x2'), ('y3', 'x3')}



## 3: (Task 5.12.2) Make Equations
def make_equations(x1, x2, w1, w2): 
    '''
    Input:
        - x1, x2: pixel coordinates of a point q in the image plane
        - w1, w2: w1=y1/y3 and w=y2/y3 where y1,y2,y3 are the whiteboard coordinates of q.
    Output:
        - List [u,v] of D-vectors that define linear equations u*h = 0 and v*h = 0

    For example, suppose we have an image of the whiteboard in which
       the top-left whiteboard corner appears at pixel coordinates 9, 18
       the bottom-left whiteboard corner appears at pixel coordinates 8,25
       the top-right whiteboard corner appears at pixel coordinates 20,20
       the bottom-right whiteboard corner appears at pixel coordinates 18,23

    Let q be the point in the image plane with pixel coordinates x=8,y=25, i.e. camera coordinates (8,25,1).
    Let y1,y2,y3 be the whiteboard coordinates of the same point.  The line that goes through the
    origin and p intersects the whiteboard at a point p.  That point p is the bottom-left corner of
    the whiteboard, so its whiteboard coordinates are 1,0,1.  Therefore (y1/y3,y2/y3,y3/y3) = (1,0,1).
    We define w1=y1/y3 and w2=y2/y3, so w1 = 1 and w2 = 0.  Given this input-output pair, let's find
    two linear equations u*h=0 and v*h=0 constraining the unknown vector h whose entries are the entries
    of the matrix H. 

>>> for v in make_equations(8,25,1,0): print(v)
<BLANKLINE>
 ('y1', 'x1') ('y1', 'x2') ('y1', 'x3') ('y2', 'x1') ('y2', 'x2') ('y2', 'x3') ('y3', 'x1') ('y3', 'x2') ('y3', 'x3')
---------------------------------------------------------------------------------------------------------------------
           -8          -25           -1            0            0            0            8           25            1
<BLANKLINE>
 ('y1', 'x1') ('y1', 'x2') ('y1', 'x3') ('y2', 'x1') ('y2', 'x2') ('y2', 'x3') ('y3', 'x1') ('y3', 'x2') ('y3', 'x3')
---------------------------------------------------------------------------------------------------------------------
            0            0            0           -8          -25           -1            0            0            0

    Note that the negations of these vectors form an equally valid solution.

    Similarly, consider the point q in the image plane with pixel coordinates 18, 23.  Let y1,y2,y3 be the whiteboard
    coordinates of p.  The corresponding point p in the whiteboard plane is the bottom-right corner, and the whiteboard
    coordinates of p are 1,1,1, so (y1/y3,y2/y3,y3/y3)=(1,1,1).  We define w1=y1/y3 and w2=y2/y3, so w1=1 and w2=1.
    We obtain the vectors u and v defining equations u*h=0 and v*h=0 as follows:

>>> for v in make_equations(18,23,1,1): print(v)
<BLANKLINE>
 ('y1', 'x1') ('y1', 'x2') ('y1', 'x3') ('y2', 'x1') ('y2', 'x2') ('y2', 'x3') ('y3', 'x1') ('y3', 'x2') ('y3', 'x3')
---------------------------------------------------------------------------------------------------------------------
          -18          -23           -1            0            0            0           18           23            1
<BLANKLINE>
 ('y1', 'x1') ('y1', 'x2') ('y1', 'x3') ('y2', 'x1') ('y2', 'x2') ('y2', 'x3') ('y3', 'x1') ('y3', 'x2') ('y3', 'x3')
---------------------------------------------------------------------------------------------------------------------
            0            0            0          -18          -23           -1           18           23            1

    Again, the negations of these vectors form an equally valid solution.
    '''
    u = Vec(D, {('y3', 'x1'):w1*x1, ('y3', 'x2'):w1*x2, ('y3', 'x3'):w1, ('y1', 'x1'):(-x1), ('y1', 'x2'):(-x2), ('y1', 'x3'):(-1)})
    v = Vec(D, {('y3', 'x1'):w2*x1, ('y3', 'x2'):w2*x2, ('y3', 'x3'):w2, ('y2', 'x1'):(-x1), ('y2', 'x2'):(-x2), ('y2', 'x3'):(-1)})
    return [u, v]



## 4: () Scaling row
# This is the vector defining the scaling equation
w = Vec(D, {('y1', 'x1'):1})



## 5: () Right-hand side
# Now construct the Vec b that serves as the right-hand side for the matrix-vector equation L*hvec=b
# This is the {0, ..., 8}-Vec whose entries are all zero except for a 1 in position 8
b = Vec({0, 1, 2, 3, 4, 5, 6, 7, 8}, {8:1})



## 6: () Rows of constraint matrix
def make_nine_equations(corners):
    '''
    input: a list of four tuples:
           [(i0,j0),(i1,j1),(i2,j2),(i3,j3)]
           where i0,j0 are the pixel coordinates of the top-left corner,
                 i1,j1 are the pixel coordinates of the bottom-left corner,
                 i2,j2 are the pixel coordinates of the top-right corner,
                 i3,j3 are the pixel coordinates of the bottom-right corner,
    output: the list of Vecs u0, u1, ..., u8 that are to be the rows of the matrix.
    Vecs u0,u1 come from applying make_equations to the top-left corner,
    Vecs u2,u3 come from applying make_equations to the bottom-left corner,
    Vecs u4,u5 come from applying make_equations to the top-right corner,
    Vecs u6,u7 come from applying make_equations to the bottom-right corner,
    Vec u8 is the vector w.
    ''' 
    whiteboard = [(0,0), (0,1), (1,0), (1,1)]
    veclist = []
    for (x1,x2), (w1,w2) in zip(corners, whiteboard):
        u, v = make_equations(x1, x2, w1, w2)
        veclist.append(u)
        veclist.append(v)
    veclist.append(w)
    return veclist



## 7: (Task 5.12.4) Build linear system
# Apply make_nine_equations to the list of tuples specifying the pixel coordinates of the
# whiteboard corners in the image.  Assign the resulting list of nine vectors to veclist:
corn = [(358, 36), (329, 597), (592, 157), (580, 483)]
veclist = make_nine_equations(corn)

# Build a Mat whose rows are the Vecs in veclist
L = rowdict2mat(veclist)



## 8: () Solve linear system
# Now solve the matrix-vector equation to get a Vec hvec, and turn it into a matrix H.
#hvec = Vec(D, {('y1', 'x1'):1.0, ('y1', 'x2'):0.0516934, ('y1', 'x3'):-359.861, ('y2', 'x1'):-0.381521, ('y2', 'x2'):0.737818, ('y2', 'x3'):110.023, ('y3', 'x1'):-0.721936, ('y3', 'x2'):-0.0116907, ('y3', 'x3'):669.476})
hvec = solve(L, b)

H = Mat(({'y1','y2','y3'}, {'x1','x2','x3'}), hvec.f)



## 9: (Task 5.12.7) Y Board Comprehension
def mat_move2board(Y):
    '''
    Input:
        - Y: a Mat each column of which is a {'y1', 'y2', 'y3'}-Vec
          giving the whiteboard coordinates of a point q.
    Output:
        - a Mat each column of which is the corresponding point in the
          whiteboard plane (the point of intersection with the whiteboard plane 
          of the line through the origin and q).

    Example:
    >>> Y_in = Mat(({'y1', 'y2', 'y3'}, {0,1,2,3}),
    ...     {('y1',0):2, ('y2',0):4, ('y3',0):8,
    ...      ('y1',1):10, ('y2',1):5, ('y3',1):5,
    ...      ('y1',2):4, ('y2',2):25, ('y3',2):2,
    ...      ('y1',3):5, ('y2',3):10, ('y3',3):4})
    >>> print(Y_in)
    <BLANKLINE>
            0  1  2  3
          ------------
     y1  |  2 10  4  5
     y2  |  4  5 25 10
     y3  |  8  5  2  4
    <BLANKLINE>
    >>> print(mat_move2board(Y_in))
    <BLANKLINE>
               0 1    2    3
          ------------------
     y1  |  0.25 2    2 1.25
     y2  |   0.5 1 12.5  2.5
     y3  |     1 1    1    1
    <BLANKLINE>
    '''
    new_cols = {}
    for col in Y.D[1]:
        new_cols['y1', col] = Y['y1', col]/Y['y3', col]
        new_cols['y2', col] = Y['y2', col]/Y['y3', col]
        new_cols['y3', col] = Y['y3', col]/Y['y3', col]  
    return Mat(({'y1', 'y2', 'y3'}, Y.D[1]), new_cols)

(X_pts, colors) = file2mat('board.png', ('x1','x2','x3'))
Y_pts = H * X_pts
Y_board = mat_move2board(Y_pts)
mat2display(Y_board, colors, ('y1', 'y2', 'y3'),
                           scale=100, xmin=None, ymin=None)
# end of perspective_lab.py
