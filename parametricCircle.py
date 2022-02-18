# Terrence Ju
# Created for CS 3388
# Assignment 2, Feb 18, 2022
# Class for creating parametric circle

from math import *
import numpy as np
from pyparsing import col
from matrix import matrix
from parametricObject import parametricObject

# Class takes in param of parametric object
class parametricCircle(parametricObject):

    # Constructor for circle with radius set to parameter
    def __init__(self,T=matrix(np.identity(4)),radius=5.0, color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,1.0),vRange=(0.0,2.0*pi),uvDelta=(1.0/10.0,pi/18.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__radius = radius

    '''
    Terrence Ju, Feb 18, 2022
    getPoint method creates a parametric circle
    Takes in params U, V, returns a matrix
    '''
    def getPoint(self,u,v):
        # Inits matrix and sets vals
        P = matrix(np.ones((4,1)))
        P.set(0,0, (self.__radius * u *cos(v)))
        P.set(1,0, (self.__radius * u *sin(v)))
        P.set(2,0, 0)
        P.set(3,0, 1)
        
        # Returns matrix
        return P

    # Setter method sets the circle's radius given a parameter
    def setRadius(self,radius):
        self.__radius = radius

    # Getter method gets the circle's radius given a parameter
    def getRadius(self):
        return self.__radius

  