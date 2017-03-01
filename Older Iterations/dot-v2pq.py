from psychopy import visual
from psychopy import event, data, core

import math
from numpy import sin, pi#numeric python for doing some maths

import numpy as np
import random

import time
import datetime
import copy


"""

import serial
ser = serial.Serial(0) 


pq_timer = core.Clock()


str2 = datetime.datetime.now()


str3 = 'subj' + '-' + str(str2.hour)  + '-' + str(str2.minute)  + '-' +  str(str2.second)


outpth = '\\\\PSHome\\Home\\ptq1\\Desktop\\Piers\\'
print str3

str4 = outpth + "text1.txt"

with open (str4, "r") as myfile:
    passage1=myfile.read().replace('\n', '')
print passage1


"""
dur = core.StaticPeriod(screenHz=60)

x_cent = 0
y_cent = 0

x_off = 400
y_off = 400

text_H = 24

w_size_x = 300
w_size_y = 400

f_Size = 300

#create a window to draw in
winB = visual.Window(monitor = 'testMonitor',size = (1680,1050), fullscr=0,units='pix',colorSpace = 'rgb',color = (-.75,-.75,-.75),allowGUI=False, screen = 2)


    
myMouse = event.Mouse(win = winB)


myMouse.setVisible(False)

def draw_defaults():
    global fix_L
    global fix_R

    fix_L = visual.Circle(winB, radius = 5, pos=(x_cent -x_off, y_cent), lineWidth = 0, fillColor = 'Black')
    roi_L = visual.Circle(winB, radius = f_Size/2, pos=(x_cent -x_off, y_cent), lineWidth = 0, fillColor = (-.5,-.5,-.5))

    roi_L.draw()
    fix_L.draw()

    fix_R = visual.Circle(winB, radius = 5, pos=(x_cent +x_off, y_cent), lineWidth = 0, fillColor = 'Black')
    roi_R = visual.Circle(winB, radius = f_Size/2, pos=(x_cent +x_off, y_cent), lineWidth = 0, fillColor = (-.5,-.5,-.5))

    roi_R.draw()
    fix_R.draw()

    return

def make_dots(arr1,max_dots):
    
    for i in range(max_dots):
        
        r_dist = random.randrange(4,f_Size/2)
        r_ang  = random.randrange(0,360)
        r_ang = math.radians(r_ang)
        arr1.append([r_dist*math.cos(r_ang),r_dist*math.sin(r_ang)])
        

    return 



draw_defaults()


grate_L= visual.GratingStim(winB, ori=45,tex ='sin',mask = 'circle', size=f_Size, sf=1, pos = (x_cent -x_off, y_cent), color= 'white',colorSpace = 'rgb',
     units = 'pix', autoLog=False)
    
grate_R= visual.GratingStim(winB, ori=45,tex ='sin',mask = 'circle', size=f_Size, sf=1, pos = (x_cent +x_off, y_cent), color= 'white',colorSpace = 'rgb',
    units = 'pix',  autoLog=False)
    

winB.flip()


boo = False
while not boo:
    k_in = event.getKeys(keyList=['1', '2'])
    if k_in:
        boo = True

max_dots = 1000

dots_arr = []
make_dots(dots_arr,max_dots)
        
        
# the very start of trials


stepper = 5
start_d = 0
stop_d =start_d + stepper

for i_t in range(1,6):
    s_f = i_t
    stepper = 5
    
    ro = random.randrange(0,1)
    
    if ro :

        l_o = 45
        r_o = -45
    else:
        l_o = -45
        r_o = 45

        
    grate_L.sf = s_f
    grate_R.sf = s_f
    grate_L.setOri(l_o)
    grate_R.setOri(r_o)
     

    dots_tmp = []
    pq_boo = True
   
    while pq_boo:
        
        #now sort out dots!!!

        dots_L=[]
        dots_R = []
        dots_tmp = dots_arr[start_d:stop_d] # so does this mean he gradually expands the range? 
    
        # i think here he just applies x_off to all items in the list 
        dots_L = list (map(lambda d:[d[0]-x_off,d[1]],dots_tmp))
        dots_R = list (map(lambda d:[d[0]+x_off,d[1]],dots_tmp))
        
    
        dot_stim_L = visual.ElementArrayStim(
        win=winB,
        nElements = len(dots_L),
        xys = dots_L,
        units="pix",
        colors = 'Black',
        elementMask="circle",
        sizes=5
    )
        dot_stim_R = visual.ElementArrayStim(
        win=winB,
        nElements = len(dots_R),
        xys = dots_R,
        units="pix",
        colors = 'Black',
        elementMask="circle",
        sizes=5  
    )
        
        grate_L.draw()
        grate_R.draw()
    
        dot_stim_L.draw()
        dot_stim_R.draw()
        fix_L.draw()
        fix_R.draw()
        winB.flip()

        event.clearEvents(eventType='keyboard')

        
        k = ['']
        count = 0
        while k[0] not in ['escape', 'esc'] and count < 1:
            k = event.waitKeys()
            if k == ['space']:
                pq_boo = False
                count+=1
            elif k == ['up']:
                stop_d +=stepper
                count +=1
            elif k == ['down']:
                stop_d -= stepper
                count+=1
            if stop_d <= stepper:
                stop_d = stepper
            if stop_d >= max_dots:
                stop_d = max_dots
                
    

        
        if event.getKeys(keyList=['escape','esc']):
            myMouse.setVisible(True)
            winB.close()
            core.quit() 
    
winB.close()

winB.winHandle.set_exclusive_mouse(False)

core.quit

# Try this

#         #r_dist = random.randrange(4,f_Size/2) comment this line out
#         r_dist = random.random()
#         r_dist**2
#         r_dist = 4 + (r_dist * f_Size/2)


# oops last line 

# r_dist = 4 + (r_dist*(f_Size - 4) )
