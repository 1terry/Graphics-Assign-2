# Terrence Ju
# Created for CS 3388
# Assignment 2, Feb 18, 2022
# Class for creating parametric cone

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

# Class takes in param of parametric object
class parametricCone(parametricObject):

    # Constructor sets radius and height
    def __init__(self,T=matrix(np.identity(4)), height=1, radius=5.0, color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,1.0),vRange=(0.0,2.0*pi),uvDelta=(1.0/10.0,pi/18.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__radius = radius
        self.__height = height

    '''
    Terrence Ju, Feb 18, 2022
    getPoint method creates a parametric cone
    Takes in params U, V, returns a matrix
    '''
    def getPoint(self,u,v):
        # Inits matrix and sets vals
        P = matrix(np.ones((4,1)))
        P.set(0,0, (1-u) * self.__radius * sin(v))
        P.set(1,0, (1-u) * self.__radius * cos(v))
        P.set(2,0, self.__height * u)
        P.set(3,0, 1)
        
        # Returns matrix
        return P

    # Setter method for height sets height equal to param
    def setHeight(self,height):
        self.__height = height

    # Getter method for height returns height
    def getHeight(self):
        return self.__height

    # Setter method for radius sets radius equal to param
    def setRadius(self,radius):
        self.__radius = radius

    # Getter method for radius returns radius
    def getRadius(self):
        return self.__radius
