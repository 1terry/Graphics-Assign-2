from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricPlane(parametricObject):

    def __init__(self,T=matrix(np.identity(4)), width=1.0, length=5.0, color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,1.0),vRange=(0.0,1),uvDelta=(1.0/10.0,1.0/10.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__width = width
        self.__length = length

    def getPoint(self,u,v):
        P = matrix(np.ones((4,1)))
        P.set(0,0, u * self.__width)
        P.set(1,0, v * self.__length)
        P.set(2,0, 0)
        P.set(3,0, 1)
        return P

    def setWidth(self,width):
        self.__width = width

    def getWidth(self):
        return self.__width

    def setLength(self,length):
        self.__length = length

    def getLength(self):
        return self.__length