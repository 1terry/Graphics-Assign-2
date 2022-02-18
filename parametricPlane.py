# Terrence Ju
# Created for CS 3388
# Assignment 2, Feb 18, 2022
# Class for creating parametric plane

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

# Class takes in param of parametric object
class parametricPlane(parametricObject):

    # Constructor initializes width and length of plane using params
    def __init__(self,T=matrix(np.identity(4)), width=1.0, length=5.0, color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,1.0),vRange=(0.0,1),uvDelta=(1.0/10.0,1.0/10.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__width = width
        self.__length = length

        '''
    Terrence Ju, Feb 18, 2022
    getPoint method creates a parametric plane
    Takes in params U, V, returns a matrix
    '''
    def getPoint(self,u,v):
        # Inits matrix and sets values
        P = matrix(np.ones((4,1)))
        P.set(0,0, u * self.__width)
        P.set(1,0, v * self.__length)
        P.set(2,0, 0)
        P.set(3,0, 1)

        # Returns matrix
        return P

    # Setter methd sets width equal to param
    def setWidth(self,width):
        self.__width = width

    # Getter method gets width
    def getWidth(self):
        return self.__width

    # Setter method sets length equal to param
    def setLength(self,length):
        self.__length = length

    # Getter method gets length
    def getLength(self):
        return self.__length