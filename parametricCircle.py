from math import *
import numpy as np
from pyparsing import col
from matrix import matrix
from parametricObject import parametricObject

class parametricCircle(parametricObject):

    def __init__(self,T=matrix(np.identity(4)),radius=5.0, color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,1.0),vRange=(0.0,2.0*pi),uvDelta=(pi/18.0,pi/9.0)):
        super().__init__(T,radius,)
        self.__radius = radius

    def getPoint(self,u,v):
        P = matrix(np.ones((4,1)))
        P.set(0,0, (self.__radius * self.__(u) *cos(v)))
        P.set(1,0, (self.__radius * self.__(u) *sin(v)))
        P.set(2,0, 0)
        P.set(3,0, 1)
        return P

    def setRadius(self,radius):
        self.__radius = radius

    def getRadius(self):
        return self.__radius

  