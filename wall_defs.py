from .worldmap import *

# Disabled ArUco ids: 17 and 37.  Don't use them.

def make_walls():

    # side +1 measures x from the left edge rightward
    # side -1 measures x from the right edge leftward

    w1 = WallSpec(length=300, height=189,
                  marker_specs = { 14 : {'side': +1, 'x':  28, 'y': 29},
                                   18 : {'side': +1, 'x':  80, 'y': 28},
                                   19 : {'side': +1, 'x': 213, 'y': 28},
                                   20 : {'side': +1, 'x': 268, 'y': 28},

                                   16 : {'side': -1, 'x': 272, 'y': 29},
                                   15 : {'side': -1, 'x': 218, 'y': 30},
                                   13 : {'side': -1, 'x':  85, 'y': 28},
                                   12 : {'side': -1, 'x':  33, 'y': 28}, },
                  doorways = { 'd1' : {'x': 150, 'width': 78, 'height': 114} }
                  )

    w2 = WallSpec(length=293, height=187, 
                  marker_specs = { 1 : {'side': +1, 'x':  28, 'y': 26},
                                  2 : {'side': +1, 'x':  78, 'y': 27},
                                  3 : {'side': +1, 'x': 207, 'y': 26},
                                  4 : {'side': +1, 'x': 259, 'y': 26},

                                  5 : {'side': -1, 'x': 265, 'y': 27},
                                  6 : {'side': -1, 'x': 215, 'y': 28},
                                  7 : {'side': -1, 'x':  83, 'y': 26},
                                  8 : {'side': -1, 'x':  34, 'y': 26}, }, 

                  doorways = { '0' : {'x': 145, 'width': 77, 'height': 111} }
                  )

    w3 = WallSpec() #Middle wall aruco unknown yet

make_walls()
