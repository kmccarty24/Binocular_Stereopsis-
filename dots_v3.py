from psychopy import visual, event, core, data, gui 
from psychopy.tools import monitorunittools
from psychopy.iohub import launchHubServer
from math import pi, sin
from random import shuffle

import pylab as pl
import numpy as np

import math, os, random


wd = os.getcwd()

# f_Size = 600


## -- ## Set Options ##--##

info = {}
info['Units'] = ['pix', 'norm' 'deg', 'height', 'cm']
info['Max Dots'] = 1000
info['dotSteps'] = 5
dlg = gui.DlgFromDict(info) #dialog box
if not dlg.OK: #did they push ok?
    core.quit()

radius = 300
dotSize = 5
dotSteps = info['dotSteps']

## -- ## Spatial Frequency ##--##

# Set correct units
if info['Units'] == 'pix': # Cycles per pixel
    sf_range = np.ndarray.tolist(pl.frange(0.001,0.2,0.005)) # generates a list from an array of floats
    # 0.001 = 1 cycle in every 100 pixels - 1% 
    # 0.2 = 1 cycle every 5 pixels - 20%?
    radius = 300
    dotSize = 5
    dotSteps = 5

elif info['Units'] == 'deg': #cycles per degree of visual angle
    sf_range = [x for x in range(1,100)]
    radius = 300
    dotSize = 5
    dotSteps = 5

elif info['Units'] == 'height': # Cycles Per Stimulus
    sf_range = [x for x in range(1,50)]

elif info['Units'] == 'norm': #Cycles Per Stimulus
    sf_range = [x for x in range(1,100)]

elif info['Units'] == 'cm': #Cycles Per stimulus
    sf_range = [x for x in range(1,100)]


## -- ## Nuts and Bolts ##--##

# ioHub

io = launchHubServer(iohub_config_name = 'iohub_config.yaml')

## Hardware ##

kb = io.devices.keyboard
left_display = io.devices.LeftDisplay
right_display = io.devices.RightDisplay
mouse = io.devices.mouse


print left_display.getIndex()
print right_display.getIndex()

# Windows 

winA = visual.Window(
        monitor = 'LeftMonitor',
        size = (1024,768), #left_display.getPixelResolution(),
        units = info['Units'], 
        fullscr = False,
        screen = 1, #(left_display.getIndex()- 1)
        color = (-.75,-.75,-.75))

winB = visual.Window(
        monitor = 'RightMonitor',
        size = (1024,768), #right_display.getPixelResolution(),
        units = info['Units'],
        fullscr = False,
        screen = 2, #right_display.getIndex()
        color = (0,0,0))

# Set the mouse visibility to False BECASUE ITS ANNOYING

mouse.setSystemCursorVisibility(False)

## Stimuli ##

# Circles and Dot Coordinates  

fix_L = visual.Circle(winA, 
                      radius = 5,
                      lineWidth = 0,
                      fillColor = 'Black')

# roi_L = visual.Circle(winA,
                      # radius = f_Size/2, 
                      # lineWidth = 0, 
                      # fillColor = (-.5,-.5,-.5))

fix_R = visual.Circle(winB, 
                      radius = 5,
                      lineWidth = 0,
                      fillColor = 'Black')

# roi_R = visual.Circle(winB,
                      # radius = f_Size/2, 
                      # lineWidth = 0, 
                      # fillColor = (-.5,-.5,-.5))

    # pos=(x_cent +x_off, y_cent)

def dot_coords(maxDots = 1000, radius = 300):

    rad = radius
    t = np.random.uniform(0.0, 2.0*np.pi, maxDots) # Angle between 0 and 2Pi (in radians)
    r = rad * np.sqrt(np.random.uniform(0.0, 1.0, maxDots)) # sqrt gets rid of clustering 
    x = r * np.cos(t)                                       # by making smaller numbers more 
    y = r * np.sin(t) #these convert to x,y from rads       # sparsely spaced, this technically 
                                                            # creates the opposite in that there 
                                                            # are more larger numbers but this 
                                                            # equates to an equlibiriam 
    #Pair x and y into a list of lists and return
    dot_array = []
    for i in range(len(x)):
        dot_array.append([x[i], y[i]])

    return dot_array


def dot_colors(maxDots = 1000):
    '''Creates a list of 1000 values of either 1 or -1 and shuffles them '''

    color_lists = []

    for dot in range(maxDots/2):
        color_lists.append([-1,-1,-1])
    for i in range(maxDots/2):
        color_lists.append([1,1,1])

    shuffle(color_lists)
    
    return color_lists

        # Creat a list of lists with a colour in it.

def displayInstructions(text, acceptedKeys= None):

    instructA = visual.TextStim(winA, text = text, color = 'red')
    instructB = visual.TextStim(winB, text = text, color = 'red')

    instructA.draw()
    instructB.draw()
    winA.flip()
    winB.flip()
    key = event.waitKeys(keyList = acceptedKeys)

    winA.flip()
    winB.flip()


# SF Report

sf_Val = visual.TextStim(winB, text = '', pos = [300,-300])

# Gratings to be placed on top of the circles

grate_L = visual.GratingStim(winA, 
                            ori=45,
                            tex ='sin',
                            mask = 'circle', 
                            size= radius*2, 
                            sf=1, # Dont need to change this
                            #pos = (x_cent -x_off, y_cent),
                            contrast = 0.75, #Chosen 0.25
                            color= (1,1,1),
                            colorSpace = 'rgb',
                            units = info['Units'],
                            autoLog=False)
    
grate_R = visual.GratingStim(winB, 
                            ori=45,
                            tex ='sin',
                            mask = 'circle', 
                            size=radius*2, 
                            sf=1, # Dont need to change this
                            #pos = (x_cent -x_off, y_cent),
                            contrast = 0.75, #Chosen 0.25
                            color= (1,1,1),
                            colorSpace = 'rgb',
                            units = info['Units'],
                            autoLog=False)

fix_L.draw()
fix_R.draw()

# roi_L.draw()
# roi_R.draw()

grate_L.draw()
grate_R.draw()

winA.flip()
winB.flip()

# Now prepare the random dot coordinates
dots = dot_coords()
shuffle(dots)

color_lists = dot_colors()

# Display Instructions
instruct = 'Press Space To Continue'
displayInstructions(text = instruct)

# Trials Draw

    
    # Choose SF for the Grating
for thisSF in sf_range:
    sf = thisSF
    print 'this Spatial Freq is', thisSF

    sf_Val.text = thisSF

    # Choose a random orientation - always opposite 
    randOri = random.randrange(0,1)
    
    if randOri == 1:
        l_o = 0 #left ori
        r_o = 0 #right ori
    else:
        l_o = 0
        r_o = 0

    # Set these values 

    grate_L.sf = sf
    grate_R.sf = sf
    grate_L.setOri(l_o)
    grate_R.setOri(r_o)

    # Allow dots to be Drawn

    dotIndex = 0
    dotendIndex = dotSteps  # add x dots a time (upto but not including)

    while True:
        trialCount = 0

        try: # see if there is that many indicies
            dotsL = dots[dotIndex:dotendIndex]
            dotsR = dots[dotIndex:dotendIndex]
            dotsL_Col = color_lists[dotIndex:dotendIndex]
            dotsR_Col = color_lists[dotIndex:dotendIndex]
        except: #overshoot correction
            dotsL = dots[dotIndex:999]
            dotsR = dots[dotIndex:999]
            dotsL_Col = color_lists[dotIndex:999]
            dotsR_Col = color_lists[dotIndex:999]

        # needs to be additive, i.e a dot is added everytime,. not overridden 

        dot_stim_L = visual.ElementArrayStim(
        winA,
        nElements = len(dotsL),
        xys = dotsL,
        elementTex = None,
        units="pix",
        colorSpace = "rgb",
        colors = dotsL_Col,
        elementMask="circle",
        sizes= dotSize)

        dot_stim_R = visual.ElementArrayStim(
        winB,
        nElements = len(dotsR),
        xys = dotsR,
        elementTex = None,
        units="pix",
        colors = dotsL_Col,
        elementMask="circle",
        sizes=dotSize)

        sf_Val.draw()

        grate_L.draw()
        grate_R.draw()

        dot_stim_L.draw()
        dot_stim_R.draw()

        fix_L.draw()
        fix_R.draw()

        winA.flip()
        winB.flip()
        print "Flipped"

        event.clearEvents(eventType ='keyboard')

        keys = event.waitKeys(keyList = ['q', 'space', 'up', 'down'])

        if keys[0] == 'q':
            print 'Quitting'
            core.quit()
            win.close()
            quit()
        elif keys[0] == 'space':
            trialCount  +=1
            break
        elif keys[0] == 'up':
            dotendIndex += dotSteps #add more
            trialCount += 1
        elif keys[0] == 'down':
            dotendIndex -= dotSteps # take away
            trialCount += 1

winA.close()
winB.close()
core.quit()



