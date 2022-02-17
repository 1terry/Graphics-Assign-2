from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCylinder(parametricObject):

    def __init__(self,T=matrix(np.identity(4)), height=1, radius=5.0, color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,1.0),vRange=(0.0,2.0*pi),uvDelta=(pi/18.0,pi/9.0)):
        super().__init__(T,height,radius)
        self.__radius = radius
        self.__height = height

    def getPoint(self,u,v):
        P = matrix(np.ones((4,1)))
        P.set(0,0, self.__radius * sin(v))
        P.set(1,0, self.__radius * cos(v))
        P.set(2,0, self.__height * u)
        P.set(3,0, 1)
        return P

    def setHeight(self,height):
        self.__height = height

    def getHeight(self):
        return self.__height

    def setRadius(self,radius):
        self.__radius = radius

    def getRadius(self):
        return self.__radius