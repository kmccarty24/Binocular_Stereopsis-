from psychopy import visual, event, core, data, gui 
from psychopy.tools import monitorunittools
from psychopy.iohub import launchHubServer
import numpy as np
import os, random


## To Do ##

# Add Splash Screen Pre Trial
# Check DataFiles
# Perhaps use thread if too heavy
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
    event.clearEvents(eventType ='keyboard')
    

    #PUT IN A SPLASH SCREEN (TEXTSTIM)
    
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
        dotStart = 0
        dotEnd = dotStart
    elif thisTrial['upDown'] == 'down':
        dotStart = 0
        dotEnd = maxDots

    # While loop
    while True:

        try:
        for frameN in range(30): 
            keys = kb.getKeys() 
            if len(keys) > 0:
                break


                dot_stim_L = visual.ElementArrayStim(
                                                    winA,
                                                    nElements = len(dotArray[0:dotStartIndex]),
                                                    xys = dotArray,
                                                    elementTex = None,
                                                    units="pix",
                                                    colorSpace = "rgb",
                                                    colors = colorArray,
                                                    elementMask="circle",
                                                    sizes= dotSize)

                dot_stim_R = visual.ElementArrayStim(
                                                    winB,
                                                    nElements = len(dotArray[0:dotStartIndex]),
                                                    xys = dotArray,
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
            print 'exception'
            for frameN in range(30):
                grate_L.draw()
                grate_R.draw()

                winA.flip()
                winB.flip()

        # check for key presses BEFORE increments otherwise innaccurate reporting of number of dots on screen right now

        for kbe in keys:
            if kbe.key == 'space':
                print 'pressed space'
                dotsOnScreen = len(dotArray[0:dotIndex])
                trailFailed = False
                break
            elif kbe.key == 'q':
                dotsOnScreen = len(dotArray[0:dotIndex])
                trailFailed = False
                trials.addData('trialNo', trialCount)
                trials.addData('Dots', dotsOnScreen)
                trials.addData('TrialType', thisTrial['upDown'])
                trials.addData('FailedTrial', 'Quitted Runtime')
                trials.finished = True
                dataFile.write('%s \t %s \t %s \t %i \t %s \t %f \t %i \t %i \t %s \n') %(info['Participant No'], info['Age'], 
                                                                                          info['Gender'], trialCount,
                                                                                          thisTrial['upDown'], thisTrial['sf'], 
                                                                                          thisTrial['ori'], dotsOnScreen,
                                                                                          str(trialFailed))
                dataFile.close()
            else:
                print 'Assume No Press'
        
        # Increment 

        if thisTrial['upDown'] == 'up' and len(dotArray) == maxDots:
            trialFailed = True
            dotsOnScreen = 'Up - NoKey'
            break
        elif thisTrial['upDown'] == 'down' and len(dotArray) == 0: # may casue problems if failure of having a len of 0
            trialFailed = True
            dotsOnScreen = 'Down - NoKey'
            break
        elif thisTrial['upDown'] == 'up' and len(dotArray) != maxDots:
            trialFailed = False
            dotIndex += dotSteps
            
        elif thisTrial['upDown'] == 'down' and len(dotArray) != 0:
            trailFailed = False
            dotIndex -= dotSteps

    trials.addData('TrialNo', trialCount)
    trials.addData('Dots', dotsOnScreen)
    trials.addData('TrialType', thisTrial['upDown'])
    trials.addData('FailedTrial', str(trialFailed))

    dataFile.write('%s \t %s \t %s \t %i \t %s \t %f \t %i \t %i \t %s \n') %(info['Participant No'], info['Age'], 
                                                                              info['Gender'], trialCount,
                                                                              thisTrial['upDown'], thisTrial['sf'], 
                                                                              thisTrial['ori'], dotsOnScreen,
                                                                              str(trialFailed))

# ('sub\t Age\t Gender\t trialNo\t trialType\t sf\t ori\t noDots\t failedTrial\n')
    trialCount+=1

dataFile.close()

winA.close()
winB.close()
core.quit()
quit()