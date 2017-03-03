from psychopy import visual, event, core, data, gui 
from psychopy.tools import monitorunittools
from psychopy.iohub import launchHubServer

from math import pi, sin
from random import shuffle

import pylab as pl
import numpy as np

import math, os, random


## To Do ##

# Randomise\ SF order 
## Automate dot adds to 500ms increments
### Randomise orientation from 45/-45 to 90/0
#### 5 SF, 2 orientations, 10 up, 10 down for each 

# Test using threads

# f_Size = 600

 
## -- ## Set Options ##--##

info = {}
info['Participant No'] = ''
info['Age'] = ''
info['Gender'] = ['Male', 'Female', ' Other', 'Prefer Not To Say']
info['Max Dots'] = 5000
info['dotSteps'] = 100
dlg = gui.DlgFromDict(info) #dialog box
if not dlg.OK: #did they push ok?
    core.quit()

radius = 300
dotSize = 5
dotSteps = info['dotSteps']
maxDots = info['Max Dots']

## -- ## Spatial Frequency ##--##

# sf_range = np.ndarray.tolist(pl.frange(0.001,0.2,0.005)) # generates a list from an array of floats
# 0.001 = 1 cycle in every 100 pixels - 1% 
# 0.2 = 1 cycle every 5 pixels - 20%?


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

## Handers + Text File ##

wd = os.getcwd()

dataFile = open(('%s.txt' %(info['Participant Number']), 'w'))

filename = '%s\\%s' %(wd,info['Participant Number'])

rivalExp = data.ExperimentHandler(name = 'Rivalry to Stable',
                                  extraInfo = info,
                                  dataFileName = filename)

conditions = data.importConditions('trials.xlsx')

trials = data.TrialHandler(trialList = conditions, nReps = 1, name = 'Main Sequence')

rivalExp.addLoop(trials)

dataFile.write('PNumb\t Age\t Gender\t sf\t ori\t upDown\t noDots\n')

# Windows 

winA = visual.Window(
        monitor = 'LeftDisplay',
        size = (1280,1024), #left_display.getPixelResolution(),
        units = 'pix', 
        fullscr = False,
        screen = 2, #(left_display.getIndex()- 1) current set 1
        color = (0,0,0))

winB = visual.Window(
        monitor = 'RightDisplay',
        size = (1280,1024), #right_display.getPixelResolution(),
        units = 'pix',
        fullscr = False,
        screen = 1, #right_display.getIndex() current set 0
        color = (0,0,0))

# Set the mouse visibility to False BECASUE ITS ANNOYING

mouse.setSystemCursorVisibility(False)

## Stimuli ##

# Circles and Dot Coordinates  

fix_L = visual.Circle(winA, 
                      radius = 5,
                      lineWidth = 0,
                      fillColor = 'Black')

fix_R = visual.Circle(winB, 
                      radius = 5,
                      lineWidth = 0,
                      fillColor = 'Black')

def dotCoords(maxDots = 5000, radius = 300):
    ''' a function that generates coordinates of a circle 
        and pairs them with a color, either black or white
    '''

    #Note: Cant use a geneator as we need to access 100 items at a time rather than procedurally

    # Define some random coordinates and convert to x and y coordinates
    rad = radius #below uses arrays so operators apply to all values
    t = np.random.uniform(0.0, 2.0*np.pi, maxDots) # Angle between 0 and 2Pi (in radians)
    r = rad * np.sqrt(np.random.uniform(0.0, 1.0, maxDots)) # sqrt gets rid of clustering 
    x = r * np.cos(t)                                       # by making smaller numbers more 
    y = r * np.sin(t) #these convert to x,y from rads       # sparsely spaced, this technically 
                                                            # creates the opposite in that there 
                                                            # are more larger numbers but this 
                                                            # equates to an equlibiriam 
    # Now create a list of them 
    coords = [[x[i], y[i]] for i in range(maxDots)]
    shuffle(coords)


    return coords # tup[0] = color, tup[1] = coord


def colorLists(maxDots = 5000):

    # Define a list of colors and shuffle them 
    color_lists = []
    for i in range(maxDots/2):
        color_lists.append([-1,-1,-1])
    for i in range(maxDots/2):
        color_lists.append([1,1,1])
    shuffle(color_lists)

    return color_lists

def displayInstructions(text, acceptedKeys= None):

    reversedString = text[::-1]

    instructA = visual.TextStim(winA, text = reversedString, color = 'red')
    instructB = visual.TextStim(winB, text = reversedString, color = 'red')


    instructA.draw()
    instructB.draw()
    winA.flip()
    winB.flip()
    key = event.waitKeys(keyList = acceptedKeys)

    winA.flip()
    winB.flip()


# Gratings to be placed on top of the circles

grate_L = visual.GratingStim(winA, 
                            ori=45,
                            tex ='sin',
                            mask = 'circle', 
                            size= radius*2, 
                            sf=1, # Dont need to change this
                            contrast = 0.25, #Chosen 0.25
                            color= (1,1,1),
                            colorSpace = 'rgb',
                            units = 'pix',
                            autoLog=False)
    
grate_R = visual.GratingStim(winB, 
                            ori=-45,
                            tex ='sin',
                            mask = 'circle', 
                            size=radius*2, 
                            sf=1, # Dont need to change this
                            contrast = 0.25, #Chosen 0.25
                            color= (1,1,1),
                            colorSpace = 'rgb',
                            units = 'pix',
                            autoLog=False)

# Display Instructions
instruct = 'Press Space To Continue'
displayInstructions(text = instruct)


## -- ## Trials Draw ##-- ##

for thisTrial in trials:
    # Setup

    event.clearEvents(eventType ='keyboard')

    
    #Set sf
    grate_L.sf = thisTrial['sf']
    grate_R.sf = thisTrial['sf']

    #Set ori
    if thisTrial['ori'] == 90 and thisTrial['leftRight'] == 1:
        grate_L.ori = 0
        grate_R.ori = 90
    elif thisTrial['ori'] == 90 and thisTrial['leftRight'] == 0:
        grate_L.ori = 90
        grate_R.ori = 0
    elif thisTrial['ori'] == 45 and thisTrial['leftRight'] == 1:
        grate_L.ori = 45
        grate_R.ori = 270
    elif thisTrial['ori'] == 45 and thisTrial['leftRight'] == 0:
        grate_L.ori = 270
        grate_R.ori = 45


    # Generate new dots and colors
    dotColorArray = dotCoords(maxDots = maxDots)
    colorList = colorLists(maxDots = maxDots)


    # While loop
    while True:

        # Set up trial or down trial
        if thisTrial['upDown'] == 'up':
            dotIndex = 0
            dotsArray = []
            colorArray = []
        elif thisTrial['upDown'] == 'down'
            dotIndex = len(dotColorArray)
            dotsArray = dotColorArray
            colorArray = colorList

        try:
            for frameN in range(30) 
            dot_stim_L = visual.ElementArrayStim(
                                                winA,
                                                nElements = len(dotsArray),
                                                xys = dotsArray,
                                                elementTex = None,
                                                units="pix",
                                                colorSpace = "rgb",
                                                colors = colorArray,
                                                elementMask="circle",
                                                sizes= dotSize)

            dot_stim_R = visual.ElementArrayStim(
                                                winB,
                                                nElements = len(dotsArray),
                                                xys = dotsArray,
                                                elementTex = None,
                                                units="pix",
                                                colors = colorArray,
                                                elementMask="circle",
                                                sizes=dotSize)
            grate_L.draw()
            grate_R.draw()

            dot_stim_L.draw()
            dot_stim_R.draw()

            winA.flip()
            winB.flip()

        except:

            grate_L.draw()
            grate_R.draw()

            winA.flip()
            winB.flip()

        # Increment 





## -- OLD BELOW ## -- ##


    # Choose SF for the Grating
for thisSF in sf_range:
    # Allow dots to be Drawn

    dotIndex = 0
    dotendIndex = dotSteps  # add x dots a time (upto but not including)

    while True:
        trialCount = 0

        #No need for overshoot correction, any non-applicable index is sorted automatically to the end of the list
        dotsL = dots[dotIndex:dotendIndex]
        dotsR = dots[dotIndex:dotendIndex]
        dotsL_Col = color_lists[dotIndex:dotendIndex]
        dotsR_Col = color_lists[dotIndex:dotendIndex]


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

        event.clearEvents(eventType ='keyboard')

        keys = event.waitKeys(keyList = ['q', 'space', 'up', 'down'])

        if keys[0] == 'q':
            print 'Quitting'
            winA.close()
            winB.close()
            core.quit()
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

dataFile.close()

winA.close()
winB.close()
core.quit()



