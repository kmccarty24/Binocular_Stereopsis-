import numpy as np
import os
from random import shuffle
from itertools import izip 

# def dot_coords(incDots = 125, maxDots = 5000, radius = 300):
#     ''' a function that generates coordinates of a circle 
#         and pairs them with a color, either black or white
#     '''
#     noChunksReq = int(maxDots / incDots)
#     count = 0
#     coords = []
#     while len(coords) != noChunksReq:
#         print count
#         # Define some random coordinates and convert to x and y coordinates
#         rad = radius
#         t = np.random.uniform(0.0, 2.0*np.pi, incDots) # Angle between 0 and 2Pi (in radians)
#         r = rad * np.sqrt(np.random.uniform(0.0, 1.0, incDots)) # sqrt gets rid of clustering 
#         x = r * np.cos(t)                                       # by making smaller numbers more 
#         y = r * np.sin(t) #these convert to x,y from rads       # sparsely spaced, this technically 
#                                                                 # creates the opposite in that there 
#                                                                 # are more larger numbers but this 
#                                                                 # equates to an equlibiriam 
#         coords.append([[x[i], y[i]] for i in range(incDots)])
#         count+=1

#     # Now create a list of them 

#     # Define a list of colors and shuffle them 
#     # color_lists = []
#     # for i in range(maxDots/2):
#     #     color_lists.append([-1,-1,-1])
#     # for i in range(maxDots/2):
#     #     color_lists.append([1,1,1])

#     # shuffle(color_lists)

#     yield coords # tup[0] = color, tup[1] = coord

# def dot_coords2(incDots = 125, maxDots = 5000, radius = 300):
#     ''' a function that generates coordinates of a circle 
#         and pairs them with a color, either black or white
#     '''
#     # noChunksReq = int(maxDots / incDots)
#     # count = 0
#     # coords = []
#     # while len(coords) != noChunksReq:
#     #print count
    
#     # Define some random coordinates and convert to x and y coordinates
#     rad = radius
#     t = np.random.uniform(0.0, 2.0*np.pi, incDots) # Angle between 0 and 2Pi (in radians)
#     r = rad * np.sqrt(np.random.uniform(0.0, 1.0, incDots)) # sqrt gets rid of clustering 
#     x = r * np.cos(t)                                       # by making smaller numbers more 
#     y = r * np.sin(t) #these convert to x,y from rads       # sparsely spaced, this technically 
#                                                             # creates the opposite in that there 
#                                                             # are more larger numbers but this 
#                                                             # equates to an equlibiriam 
#     coords = np.array([[x[i], y[i]] for i in range(incDots)])

#     return coords 

def dot_coords3(maxDots = 5000, radius = 300):
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


# def chunkdot_coords(increments = 125, radius = 300, maxDots = 5000):
#     ''' a function that generates coordinates of a circle 
#         and pairs them with a color, either black or white
#     '''

#     # Define some random coordinates and convert to x and y coordinates
#     rad = radius
#     t = np.random.uniform(0.0, 2.0*np.pi, increments) # Angle between 0 and 2Pi (in radians)
#     r = rad * np.sqrt(np.random.uniform(0.0, 1.0, increments)) # sqrt gets rid of clustering 
#     x = r * np.cos(t)                                       # by making smaller numbers more 
#     y = r * np.sin(t) #these convert to x,y from rads       # sparsely spaced, this technically 
#                                                             # creates the opposite in that there 
#                                                             # are more larger numbers but this 
#                                                             # equates to an equlibiriam 
#     # Now create a list of them 
#     coords = [[x[i], y[i]] for i in range(increments)]
#     shuffle(coords)

#     # Define a list of colors and shuffle them 
#     color_lists = []
#     for i in range(increments/2):
#         color_lists.append([-1,-1,-1])
#     for i in range(increments/2):
#         color_lists.append([1,1,1])

#     shuffle(color_lists)

#     combined = zip(coords, color_lists)

#     repeats = (item for item coords)

#     return izip(color_lists, coords) # tup[0] = color, tup[1] = coord