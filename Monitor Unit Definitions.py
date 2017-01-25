# Some unit definitions #

'''
Height units
With ‘height’ units everything is specified relative to the height of the window 
(note the window, not the screen). As a result, the dimensions of a screen with 
standard 4:3 aspect ratio will range (-0.6667,-0.5) in the bottom left to (+0.6667,+0.5) 
in the top right. For a standard widescreen (16:10 aspect ratio) the bottom left of the 
screen is (-0.8,-0.5) and top-right is (+0.8,+0.5). Obviously it has the disadvantage 
that the location of the right and left edges of the screen have to be determined from a 
knowledge of the screen dimensions. (These can be determined at any point by the Window.size attribute.)

Spatial frequency: cycles per stimulus (so will scale with the size of the stimulus).

Requires : No monitor information
'''

'''

Normalised units
In normalised (‘norm’) units the window ranges in both x and y from -1 to +1. That is, 
the top right of the window has coordinates (1,1), the bottom left is (-1,-1). Note that, 
in this scheme, setting the height of the stimulus to be 1.0, will make it half the 
height of the window, not the full height (because the window has a total height of 1:-1 = 2!). 
Also note that specifying the width and height to be equal will not result in a square stimulus 
if your window is not square - the image will have the same aspect ratio as your window. e.g. 
on a 1024x768 window the size=(0.75,1) will be square.

Spatial frequency: cycles per stimulus (so will scale with the size of the stimulus).

Requires : No monitor information
'''

'''
Centimeters on screen
Set the size and location of the stimulus in centimeters on the screen.

Spatial frequency: cycles per cm

Requires : information about the screen width in cm and size in pixels

Assumes : pixels are square. Can be verified by drawing a stimulus with 
matching width and height and verifying that it is in fact square. 
For a CRT this can be controlled by setting the size of the viewable screen 
(settings on the monitor itself).

'''

'''
Degrees of visual angle
Use degrees of visual angle to set the size and location of the stimulus. 
This is, of course, dependent on the distance that the participant sits 
from the screen as well as the screen itself, so make sure that this is controlled, 
and remember to change the setting in Monitor Center if the viewing distance changes.

Spatial frequency: cycles per degree

Requires : information about the screen width in cm and pixels and the viewing distance in cm


'''

'''

Pixels on screen
You can also specify the size and location of your stimulus in pixels. 
Obviously this has the disadvantage that sizes are specific to your monitor 
(because all monitors differ in pixel size).

Spatial frequency: `cycles per pixel` 
(this catches people out but is used to be in keeping with the other units. 
If using pixels as your units you probably want a spatial frequency in the range 0.2-0.001 
i.e. from 1 cycle every 5 pixels to one every 100 pixels).

Requires : information about the size of the screen (not window) 
in pixels, although this can often be deduce from the operating system if it has been set correctly there.

Assumes: nothing
'''
