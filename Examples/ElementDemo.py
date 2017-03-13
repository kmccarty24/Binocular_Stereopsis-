from psychopy import visual, event, core, data, gui 
from psychopy.tools import monitorunittools
from psychopy.iohub import launchHubServer
import numpy as np
import os, random

winA = visual.Window(
        monitor = 'LeftDisplay',
        size = (1280,1024), #left_display.getPixelResolution(),
        units = 'pix', 
        fullscr = False,
        screen = 2, #(left_display.getIndex()- 1) current set 1
        color = (0,0,0))

grate_L = visual.GratingStim(winA, 
                            ori=45,
                            tex ='sin',
                            mask = 'circle', 
                            size= 600, 
                            sf=1, # Dont need to change this
                            contrast = 0.25, #Chosen 0.25
                            color= (1,1,1),
                            colorSpace = 'rgb',
                            units = 'pix',
                            autoLog=False)

def dotCoords(maxDots = 5000, radius = 300):
    ''' a function that generates coordinates of a circle 
        and pairs them with a color, either black or white
    '''

    # Define some random coordinates and convert to x and y coordinates
    rad = radius
    t = np.random.uniform(0.0, 2.0*np.pi, maxDots) # Angle between 0 and 2Pi (in radians)
    r = rad * np.sqrt(np.random.uniform(0.0, 1.0, maxDots)) # sqrt gets rid of clustering 
    x = r * np.cos(t)                                       # by making smaller numbers more 
    y = r * np.sin(t) #these convert to x,y from rads       # sparsely spaced, this technically 
                                                            # creates the opposite in that there 
                                                            # are more larger numbers but this 
                                                            # equates to an equlibiriam 
    
    coords = np.stack((x,y), axis = 1) # stack the two arrays horizontally (column wise)
    
    np.random.shuffle(coords)
    
    # Define a list of colors and shuffle them 
    color_lists = []
    for i in range(maxDots/2):
        color_lists.append([-1,-1,-1])
    for i in range(maxDots/2):
        color_lists.append([1,1,1])

    np.random.shuffle(color_lists)

    return coords, color_lists


dots, colors = dotCoords()



dot_stim_L = visual.ElementArrayStim(
                                    winA,
                                    nElements = 100,
                                    xys = dots,
                                    elementTex = None,
                                    units="pix",
                                    colorSpace = "rgb",
                                    elementMask="circle",
                                    sizes= 5)

for i in range(60):
	grate_L.draw()
	#dot_stim_L.draw()
	winA.flip()