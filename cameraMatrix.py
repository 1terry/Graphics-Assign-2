import math
import operator
from math import *
import numpy as np
from matrix import matrix

class cameraMatrix:

    def __init__(self,window,UP,E,G,nearPlane=10.0,farPlane=50.0,theta=90.0):
        self.__UP = UP.normalize()
        self.__E = E
        self.__G = G
        self.__np = nearPlane
        self.__fp = farPlane
        self.__width = window.getWidth()
        self.__height = window.getHeight()
        self.__theta = theta
        self.__aspect = self.__width/self.__height
        self.__npHeight = self.__np*(pi/180.0*self.__theta/2.0)
        self.__npWidth = self.__npHeight*self.__aspect

        Mp = self.__setMp(self.__np,farPlane)
        T1 = self.__setT1(self.__np,self.__theta,self.__aspect)
        S1 = self.__setS1(self.__np,self.__theta,self.__aspect)
        T2 = self.__setT2()
        S2 = self.__setS2(self.__width,self.__height)
        W2 = self.__setW2(self.__height)

        self.__N = (self.__E - self.__G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).crossProduct(self.__N).normalize()
        self.__V = self.__N.crossProduct(self.__U)

        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,self.__E)
        self.__C = W2*S2*T2*S1*T1*Mp
        self.__M = self.__C*self.__Mv

    def __setMv(self,U,V,N,E):
        uTranspose = U.transpose()
        vTranspose = V.transpose()
        nTranspose = N.transpose()

        # might be better to create for loop
        ux = uTranspose.get(0,0)
        uy = uTranspose.get(0,1)
        uz = uTranspose.get(0,2)

        vx = vTranspose.get(0,0)
        vy = vTranspose.get(0,1)
        vz = vTranspose.get(0,2)

        nx = nTranspose.get(0,0)
        ny = nTranspose.get(0,1)
        nz = nTranspose.get(0,2)

        # Gets the right E values
        
        U = U.insertRow(3,0)
        V = V.insertRow(3,0)
        N = N.insertRow(3,0)
        E = E.scalarMultiply(-1)
        # print(E.getNumberOfRows())
        # print(E.getNumberOfColumns())
        # print(U)
        # print(U.getNumberOfColumns())
        
        right1 = E.dotProduct(U)
        right2 = E.dotProduct(V)
        right3 = E.dotProduct(N)

        MV = matrix(np.zeros((4,4)))
        MV.set(0, 0, ux)
        MV.set(0, 1, uy)
        MV.set(0, 2, uz)
        MV.set(0, 3, right1)

        MV.set(1, 0, vx)
        MV.set(1, 1, vy)
        MV.set(1, 2, vz)
        MV.set(1, 3, right2)

        MV.set(2, 0, nx)
        MV.set(2, 1, ny)
        MV.set(2, 2, nz)
        MV.set(2, 3, right3)

        MV.set(3, 0, 0)
        MV.set(3, 1, 0)
        MV.set(3, 2, 0)
        MV.set(3, 3, 1)
        print(MV)
        return MV

    def __setMp(self,nearPlane,farPlane):
        
        varB = (-2 * farPlane * nearPlane) / (farPlane - nearPlane)
        varA = (nearPlane + varB) / nearPlane

        MP = matrix(np.zeros((4,4)))
        MP.set(0, 0, nearPlane)
        MP.set(1, 1, nearPlane)
        MP.set(2, 2, varA)
        MP.set(2, 3, varB)
        MP.set(3, -2, -1)
        
        return MP
       
    def __setT1(self,nearPlane,theta,aspect):

        varT = nearPlane * tan((math.pi/180) * (theta/2))
        varB = -varT
        varR = aspect * varT
        varL = -varR

        T1 = matrix(np.zeros((4,4)))
        T1.set(0, 0, 1)
        T1.set(0, 3, -(varR + varL)/2)
        T1.set(1, 1, 1)
        T1.set(1, 3, -(varT + varB)/2)
        T1.set(2, 2, 1)
        T1.set(3, 3, 1)

        return T1
        
    def __setS1(self,nearPlane,theta,aspect):
        
        varT = nearPlane * tan((math.pi/180) * (theta/2))
        varB = -varT
        varR = aspect * varT
        varL = -varR

        S1 = matrix(np.zeros((4,4)))
        S1.set(0, 0, 2/(varR - varL))
        S1.set(1, 1, 2/(varT - varB))
        S1.set(2, 2, 1)
        S1.set(3, 3, 1)

        return S1

    def __setT2(self):

        T2 = matrix(np.zeros((4,4)))
        T2.set(0, 0, 1)
        T2.set(0, 3, 1)
        T2.set(1, 1, 1)
        T2.set(1, 3, 1)
        T2.set(2, 2, 1)
        T2.set(3, 3, 1)

        return T2

    def __setS2(self,width,height):
        
        S2 = matrix(np.zeros((4,4)))
        S2.set(0, 0, width/2)
        S2.set(1, 1, height/2)
        S2.set(2, 2, 1)
        S2.set(3, 3, 1)

        return S2

    def __setW2(self,height):

        W2 = matrix(np.zeros((4,4)))
        W2.set(0, 0, 1)
        W2.set(1, 1, -1)
        W2.set(1, 3, height)
        W2.set(2, 2, 1)
        W2.set(3, 3, 1)

        return W2

    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def viewingToPixelCoordinates(self,P):
        return self.__C*P.scalarMultiply(1.0/(self.__C*P).get(3,0))

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getE(self):
        return self.__E

    def getG(self):
        return self.__G

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

    def getNp(self):
        return self.__np

    def getFp(self):
        return self.__fp

    def getTheta(self):
        return self.__theta

    def getAspect(self):
        return self.__aspect

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getNpHeight(self):
        return self.__npHeight

    def getNpWidth(self):
        return self.__npWidth