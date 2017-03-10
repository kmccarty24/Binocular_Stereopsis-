from psychopy import visual, event, core, data, gui 
from psychopy.tools import monitorunittools
from psychopy.iohub import launchHubServer
import numpy as np
import os, random


## To Do ##

# Add Splash Screen Pre Trial
# Check DataFiles
# Build a Data Aggregator

 
## -- ## Set Options ##--##

info = {}
info['Participant No'] = 99
info['Age'] = 99
info['Gender'] = ['Male', 'Female', ' Other', 'Prefer Not To Say']
info['Max Dots'] = 5000
info['dotSteps'] = 125
dlg = gui.DlgFromDict(info) #dialog box
if not dlg.OK: #did they push ok?
    core.quit()

radius = 300
dotSize = 5
dotSteps = info['dotSteps']
maxDots = info['Max Dots']

## -- ## Spatial Frequency ##--##

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

dataFileName = '%s.txt' %(info['Participant No'])

dataFile = open(dataFileName, 'w')

filename = '%s\\%s' %(wd,info['Participant No'])

rivalExp = data.ExperimentHandler(name = 'Rivalry to Stable',
                                  extraInfo = info,
                                  dataFileName = filename)

conditions = data.importConditions('trials.xlsx')

trials = data.TrialHandler(trialList = conditions, nReps = 1, name = 'Main Sequence')

rivalExp.addLoop(trials)

dataFile.write('Sub\t Age\t Gender\t trialNo\t trialType\t sf\t ori\t noDots\t failedTrial\n')

# Windows 

winA = visual.Window(
        monitor = 'LeftDisplay',
        size = (1280,1024), #left_display.getPixelResolution(),
        units = 'pix', 
        fullscr = False,
        screen = 0, #(left_display.getIndex()- 1) current set 1
        color = (0,0,0))

winB = visual.Window(
        monitor = 'RightDisplay',
        size = (1280,1024), #right_display.getPixelResolution(),
        units = 'pix',
        fullscr = False,
        screen = 2, #right_display.getIndex() current set 0
        color = (0,0,0))

# Set the mouse visibility to False BECASUE ITS ANNOYING

mouse.setSystemCursorVisibility(False)

## Stimuli ##
 
splashTextRival = 'Please confirm rivalry'
splashTextStable = 'Please confirm stability'
splashText_L = visual.TextStim(winA, text = '', color = 'white', pos = (0, -350))
splashText_R = visual.TextStim(winB, text = '', color = 'white', pos = (0, -350))



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
trialCount = 0

for thisTrial in trials:
    # Setup
    trialCount +=1
    
    print 'trial No: %i' %(trialCount)
    print 'trial SF: %s' %(thisTrial['sf'])
    print 'trial ORI: %s' %(thisTrial['ori'])
    print 'trial TYPE: %s' %(thisTrial['upDown'])

    io.clearEvents('all')
    kb.clearEvents()
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
    dotArray, colorArray = dotCoords(maxDots = maxDots)

    # Set up trial or down trial
    if thisTrial['upDown'] == 'up':
        dotIndex = dotSteps # this accounts for the blank grating on spash
    elif thisTrial['upDown'] == 'down':
        dotIndex = maxDots - dotSteps

    #PUT IN A SPLASH SCREEN (TEXTSTIM)
    if thisTrial['upDown'] == 'up':
        splashText_L.text = splashTextRival[::-1]
        splashText_R.text = splashTextRival[::-1]

        grate_L.draw()
        grate_R.draw()
        splashText_L.draw()
        splashText_R.draw()

        winA.flip()
        winB.flip()
        kb.waitForPresses(keys = [' '])

    elif thisTrial['upDown'] == 'down': #Need to add element array in 

        dot_stim_L = visual.ElementArrayStim(
                                        winA,
                                        nElements = maxDots,
                                        xys = dotArray,
                                        elementTex = None,
                                        units = "pix",
                                        colors = colorArray,
                                        colorSpace = "rgb",
                                        elementMask ="circle",
                                        sizes = dotSize)

        dot_stim_R = visual.ElementArrayStim(
                                        winB,
                                        nElements = maxDots,
                                        xys = dotArray,
                                        elementTex = None,
                                        units = "pix",
                                        colorSpace = "rgb",
                                        colors = colorArray,
                                        elementMask ="circle",
                                        sizes = dotSize)

        splashText_L.text = splashTextStable[::-1]
        splashText_R.text = splashTextStable[::-1]

        grate_L.draw()
        grate_R.draw()
        dot_stim_L.draw()
        dot_stim_R.draw()
        splashText_L.draw()
        splashText_R.draw()

        winA.flip()
        winB.flip()
        
        events = kb.waitForPresses(keys = [' '])

    kb.clearEvents()
    io.clearEvents('all')

    events = []

    whileBool = True

    # While loop
    while whileBool:
        
        resp = None

        tmp_dotArray = np.array(dotArray[0:dotIndex])
        tmp_colArray = np.array(colorArray[0:dotIndex])
        dotsOnScreen = len(tmp_dotArray)
        
        # Element Array Stims

        dot_stim_L = visual.ElementArrayStim(
                                            winA,
                                            nElements = dotsOnScreen,
                                            xys = tmp_dotArray,
                                            elementTex = None,
                                            units = "pix",
                                            colors = tmp_colArray,
                                            colorSpace = "rgb",
                                            elementMask ="circle",
                                            sizes = dotSize)

        dot_stim_R = visual.ElementArrayStim(
                                            winB,
                                            nElements = dotsOnScreen,
                                            xys = tmp_dotArray,
                                            elementTex = None,
                                            units = "pix",
                                            colorSpace = "rgb",
                                            colors = tmp_colArray,
                                            elementMask ="circle",
                                            sizes = dotSize)

        for frameN in range(30): 
            events = kb.getKeys()

            for kbe in events:
                if kbe.type == 'KEYBOARD_PRESS' and kbe.key == ' ': # spacebar, need to
                    print 'pressed space'                           # be specific about it
                    trialFailed = False                             # being a press not just the
                    resp = 'space'                                  # key as it detects depresses from 
                    whileBool = False                               # initialising spacebar press
                elif kbe.type == 'KEYBOARD_PRESS' and kbe.key == 'q':
                    trialFailed = False
                    trials.addData('trialNo', trialCount)
                    trials.addData('Dots', dotsOnScreen)
                    trials.addData('TrialType', thisTrial['upDown'])
                    trials.addData('FailedTrial', 'Quitted Runtime')
                    trials.finished = True
                    dataFile.write('%s \t %s \t %s \t %i \t %s \t %s \t %s \t %i \t %s \n' %(info['Participant No'], info['Age'], 
                                                                                              info['Gender'], trialCount,
                                                                                              thisTrial['upDown'], thisTrial['sf'], 
                                                                                              thisTrial['ori'], dotsOnScreen,
                                                                                              trialFailed))
                    dataFile.close()
                    winA.close()
                    winB.close()


            grate_L.draw()
            grate_R.draw()

            dot_stim_L.draw()
            dot_stim_R.draw()

            winA.flip()
            winB.flip()

        # Increment 

        if thisTrial['upDown'] == 'up' and dotsOnScreen == maxDots:
            print 'reached upper limit'
            trialFailed = True
            break
        elif thisTrial['upDown'] == 'down' and dotsOnScreen == dotSteps:
            print 'reached lower limit'
            trialFailed = True
            break
        elif thisTrial['upDown'] == 'up' and dotsOnScreen != maxDots:
            # print 'going up'
            trialFailed = False
            dotIndex += dotSteps
        elif thisTrial['upDown'] == 'down' and dotsOnScreen != 0:
            # print 'going down'
            trailFailed = False
            dotIndex -= dotSteps

    trials.addData('TrialNo', trialCount)
    trials.addData('Dots', dotsOnScreen)
    trials.addData('TrialType', thisTrial['upDown'])
    trials.addData('FailedTrial', trialFailed)

    dataFile.write('%s \t %s \t %s \t %i \t %s \t %s \t %s \t %i \t %s \n' %(info['Participant No'], info['Age'], 
                                                                              info['Gender'], trialCount,
                                                                              thisTrial['upDown'], thisTrial['sf'], 
                                                                              thisTrial['ori'], dotsOnScreen,
                                                                              trialFailed))

    trialCount+=1

dataFile.close()

winA.close()
winB.close()
core.quit()
quit()