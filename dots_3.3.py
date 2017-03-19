from psychopy import visual, event, core, data, gui
from psychopy.iohub import launchHubServer
import numpy as np
import os

## To Do ##
# Build a Data Aggregator
# Set up Monitor in ioHub_Config.yaml

# Exception Class

class DuplicateError(Exception):
    pass

## -- ## Working Directories ## -- ##

wd = os.getcwd()

if os.path.isdir('./data'):
    print 'Data Directory Exists, Passing...'
    pass
else:
    print 'Data Directory Does Not Exist, Creating...'
    os.mkdir('./data')

dataDir = os.path.join(wd, 'data')

## -- ## Participant Information ##--##

info = {}
info['VERSION'] = ['', 'SMALL', 'LARGE']
info['Participant Forename'] = ''
info['Particicpant Surname'] = ''
info['runNo'] = ''
info['Age'] = 99
info['Gender'] = ['Male', 'Female', ' Other', 'Prefer Not To Say']
dlg = gui.DlgFromDict(info) 
if not dlg.OK: #did they push ok?
    core.quit()

if len(info['runNo']) == 0 or len(info['VERSION']) == 0 or len(info['Participant Forename']) == 0:
    print "Please make sure you enter a valid runNo, VERSION and/or Participant Names"
    core.quit()
    quit()

# Create code 

pCode = '%s%s%s%s' %(info['Participant Forname'][0], info['Participant Forname'][-1], 
                     info['Participant Surname'][0], info['Participant Surname'][-1])

fileCode = '%s%s%s%s%i_v%s_RunN%i' %(info['Participant Forname'][0], info['Participant Forname'][-1], 
                                     info['Participant Surname'][0], info['Participant Surname'][-1],
                                     info['VERSION'], int(info['runNo']))

dateTime = data.getDateStr()

## Handers + Text File ##


#Data Path
dataFileName = '%s\\%s' %(dataDir, fileCode)

#Check File Exists
if os.path.isfile(dataFileName):
    raise Duplicate('Duplicate Data Filename Found, %s' %(dataFileName))

dataFile = open(dataFileName, 'w')

psychopyFilename = '%s\\%s' %(dataDir, fileCode)

rivalExp = data.ExperimentHandler(name = 'Rivalry to Stable',
                                  extraInfo = info,
                                  dataFileName = psychopyFilename)

conditions = data.importConditions('trials.xlsx')

trials = data.TrialHandler(trialList = conditions, nReps = 1, name = 'Main Sequence')

rivalExp.addLoop(trials)

dataFile.write('dateTime\tSub\tVersion\trunNo\tAge\tGender\ttrialNo\ttrialType\tsf\tori\tnoDots\tfailedTrial\n')


## -- ## Set Options / Constants ##--##

if info['VERSION'] == 'SMALL':
    maxDots = 5000
    radius = 150
    dotSteps = 50
elif info['VERSION'] == 'LARGE':
    maxDots = 10000
    radius = 300
    dotSteps = 125

dotSize = 2

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


# Windows 

winA = visual.Window(
        monitor = 'LeftDisplay',
        size = (1280, 1024), #left_display.getPixelResolution(),
        units = 'pix', 
        fullscr = True,
        screen = 1, #(left_display.getIndex()- 1) current set 1
        color = (0, 0, 0))

winB = visual.Window(
        monitor = 'RightDisplay',
        size = (1280,1024), #right_display.getPixelResolution(),
        units = 'pix',
        fullscr = True,
        screen = 0, #right_display.getIndex() current set 0
        color = (0, 0, 0))

# Set the mouse visibility to False

mouse.setSystemCursorVisibility(False)

## Stimuli ##

def dotCoords(maxDots = 5000, radius = 300):
    ''' a function that generates coordinates of a circle 
        and pairs them with a color, either black or white
    '''

    # Define some random coordinates and convert to x and y coordinates
    rad = radius
    t = np.random.uniform(0.0, 2.0 * np.pi, maxDots) # Angle between 0 and 2Pi (in radians)
    r = rad * np.sqrt(np.random.uniform(0.0, 1.0, maxDots)) # sqrt gets rid of clustering 
    x = r * np.cos(t)                                       # by making smaller numbers more 
    y = r * np.sin(t) #these convert to x,y from rads       # sparsely spaced, this technically 
                                                            # creates the opposite in that there 
                                                            # are more larger numbers but this 
                                                            # equates to an equilibrium
    coords = np.stack((x, y), axis = 1) # stack the two arrays horizontally (column wise)

    np.random.shuffle(coords)

    # Define a list of colors and shuffle them 
    color_lists = []
    for i in range(maxDots / 2):
        color_lists.append([-1, -1, -1])
    for i in range(maxDots / 2):
        color_lists.append([1, 1, 1])

    np.random.shuffle(color_lists)

    return coords, color_lists


def displayInstructions(text, acceptedKeys= None):

    instrString = reverseWords(text)

    instructA = visual.ImageStim(winA, image = 'Press Space.png')
    instructB = visual.ImageStim(winB, image = 'Press Space.png')

    instructA.draw()
    instructB.draw()
    winA.flip()
    winB.flip()
    kb.waitForPresses(keys = [' '])

    winA.flip()
    winB.flip()


# Splash Screens

splashTextRival = 'Press Rival.png'
splashTextStable = 'Press Stable.png'
splashText_L = visual.ImageStim(winA, pos = (0, -350))
splashText_R = visual.ImageStim(winB, pos = (0, -350))

# Gratings

grate_L = visual.GratingStim(winA, 
                             ori=45,
                             tex ='sin',
                             mask = 'circle', 
                             size= radius * 2, 
                             sf=1, # Dont need to change this
                             contrast = 0.25, #Chosen 0.25
                             color= (1, 1, 1),
                             colorSpace = 'rgb',
                             units = 'pix',
                             autoLog=False)

grate_R = visual.GratingStim(winB, 
                             ori=-45,
                             tex ='sin',
                             mask = 'circle', 
                             size=radius * 2, 
                             sf=1, # Dont need to change this
                             contrast = 0.25, #Chosen 0.25
                             color= (1, 1, 1),
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
        grate_R.ori = 135
    elif thisTrial['ori'] == 45 and thisTrial['leftRight'] == 0:
        grate_L.ori = 135
        grate_R.ori = 45


    # Generate new dots and colors
    dotArray, colorArray = dotCoords(maxDots = maxDots, radius = radius)

    # Set up trial or down trial
    if thisTrial['upDown'] == 'up':
        dotIndex = dotSteps # this accounts for the blank/full grating on splash
    elif thisTrial['upDown'] == 'down':
        dotIndex = maxDots - dotSteps

    #PUT IN A SPLASH SCREEN
    if thisTrial['upDown'] == 'up':
        splashText_L.image = splashTextRival
        splashText_R.image = splashTextRival

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

        splashText_L.image = splashTextStable
        splashText_R.image = splashTextStable

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

        for frameN in range(30): # 30 frames @ 120Hz = 250ms (refresh every 8.333333ms)
            events = kb.getKeys()

            for kbe in events:
                if kbe.type == 'KEYBOARD_PRESS' and kbe.key == ' ': # spacebar, need to
                    print 'pressed space'                           # be specific about it
                    trialFailed = False                             # being a press not just the
                                                                    # key as it detects depresses from 
                    whileBool = False                               # initialising spacebar press
                elif kbe.type == 'KEYBOARD_PRESS' and kbe.key == 'q':
                    trialFailed = False
                    trials.addData('trialNo', trialCount)
                    trials.addData('Dots', dotsOnScreen)
                    trials.addData('TrialType', thisTrial['upDown'])
                    trials.addData('FailedTrial', 'Quitted Runtime')
                    trials.finished = True
                    dataFile.write('%s\t%s\t%s\t%i\t%s\t%s\t%i\t%s\t%s\t%s\t%i\t%s\n' %(dateTime, pCode, 
                                                                                        info['VERSION'], int(info['runNo']),
                                                                                        info['Age'], info['Gender'],
                                                                                        trialCount,thisTrial['upDown'],
                                                                                        thisTrial['sf'],thisTrial['ori'], 
                                                                                        dotsOnScreen,trialFailed))
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
            dotsOnScreen = 0 #Fix for the incorrect data logging
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

    dataFile.write('%s\t%s\t%s\t%i\t%s\t%s\t%i\t%s\t%s\t%s\t%i\t%s\n' %(dateTime, pCode, 
                                                                        info['VERSION'], int(info['runNo']),
                                                                        info['Age'], info['Gender'],
                                                                        trialCount,thisTrial['upDown'],
                                                                        thisTrial['sf'],thisTrial['ori'], 
                                                                        dotsOnScreen,trialFailed))

dataFile.close()

winA.close()
winB.close()
quit()
