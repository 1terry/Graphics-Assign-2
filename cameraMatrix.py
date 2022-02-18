# Terrence Ju
# Created for CS 3388
# Assignment 2, Feb 18, 2022
# Camera matrix class

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


    '''
    Terrence Ju, Feb 18, 2022
    SetMV method creates a camera transformation matrix 
    Takes in params U, V, N, E and returns a matrix
    '''
    def __setMv(self,U,V,N,E):
        # Transposes matrices
        uTranspose = U.transpose()
        vTranspose = V.transpose()
        nTranspose = N.transpose()

        # Gets the x,y,z values for transposed matrices, starting with matrix u
        ux = uTranspose.get(0,0)    
        uy = uTranspose.get(0,1)
        uz = uTranspose.get(0,2)

        vx = vTranspose.get(0,0)    # Vals for matrix v
        vy = vTranspose.get(0,1)
        vz = vTranspose.get(0,2)

        nx = nTranspose.get(0,0)    # Vals for matrix n
        ny = nTranspose.get(0,1)
        nz = nTranspose.get(0,2)

        # Increases size of U V and N, so it can be dot producted by E
        U = U.insertRow(3,0)
        V = V.insertRow(3,0)
        N = N.insertRow(3,0)
        E = E.scalarMultiply(-1)
               
        right1 = E.dotProduct(U)    # Calculates the right values of the matrix
        right2 = E.dotProduct(V)
        right3 = E.dotProduct(N)

        # Creates matrix and sets values
        MV = matrix(np.zeros((4,4)))
        MV.set(0, 0, ux)    # Vals for row 1
        MV.set(0, 1, uy)
        MV.set(0, 2, uz)
        MV.set(0, 3, right1)
        
        MV.set(1, 0, vx)    # Vals for row 2
        MV.set(1, 1, vy)
        MV.set(1, 2, vz)
        MV.set(1, 3, right2)
        
        MV.set(2, 0, nx)    # Vals for row 3
        MV.set(2, 1, ny)
        MV.set(2, 2, nz)
        MV.set(2, 3, right3)

        MV.set(3, 3, 1)     # Vals for row 4, zeros are initialized already 

        # Returns completed matrix
        return MV

    '''
    Terrence Ju, Feb 18, 2022
    Method setMP sets values for pseudo-depth matrix
    Takes in params nearPlane and farPlane and returns matrix
    '''
    def __setMp(self,nearPlane,farPlane):
        
        # Inits variables A and B
        varB = (-2 * farPlane * nearPlane) / (farPlane - nearPlane)
        varA = (nearPlane + varB) / nearPlane

        # Creates and initializes matrix with zeros
        MP = matrix(np.zeros((4,4)))
        # Sets vals
        MP.set(0, 0, nearPlane)
        MP.set(1, 1, nearPlane)
        MP.set(2, 2, varA)
        MP.set(2, 3, varB)
        MP.set(3, -2, -1)
        
        # Returns matrix
        return MP
       
    '''
    Terrence Ju, Feb 18, 2022
    Method setT1 sets translation matrix for pseudo depth
    Takes in params nearplane, theta and aspect ratio and returns matrix for transformation
    '''
    def __setT1(self,nearPlane,theta,aspect):
        
        # Gets values of r, l, t and b 
        varT = nearPlane * tan((math.pi/180) * (theta/2))
        varB = -varT
        varR = aspect * varT
        varL = -varR

        # Initializes matrix with zeros
        T1 = matrix(np.zeros((4,4)))
        # Sets vals
        T1.set(0, 0, 1)
        T1.set(0, 3, -(varR + varL)/2)
        T1.set(1, 1, 1)
        T1.set(1, 3, -(varT + varB)/2)
        T1.set(2, 2, 1)
        T1.set(3, 3, 1)

        # Returns matrix
        return T1   
        
    '''
    Terrence Ju, Feb 18, 2022
    Method setS1 scales for pseudo-depth matrix
    Takes in params nearPlane, theta and aspect ratio and returns matrix for scaling
    '''
    def __setS1(self,nearPlane,theta,aspect):
        
        # Gets values of r, l, t and b 
        varT = nearPlane * tan((math.pi/180) * (theta/2))
        varB = -varT
        varR = aspect * varT
        varL = -varR

        # Initializes matrix with zeros
        S1 = matrix(np.zeros((4,4)))
        # Sets vals
        S1.set(0, 0, 2/(varR - varL))
        S1.set(1, 1, 2/(varT - varB))
        S1.set(2, 2, 1)
        S1.set(3, 3, 1)

        # Returns matrix
        return S1

    '''
    Terrence Ju, Feb 18, 2022
    Method setT2 used for translating warped viewing volume into screen coordinates
    Returns matrix for transformation
    '''
    def __setT2(self):
        
        # Creates and initializes matrix with zeros
        T2 = matrix(np.zeros((4,4)))
        # Sets vals
        T2.set(0, 0, 1)
        T2.set(0, 3, 1)
        T2.set(1, 1, 1)
        T2.set(1, 3, 1)
        T2.set(2, 2, 1)
        T2.set(3, 3, 1)

        # Returns matrix
        return T2

    '''
    Terrence Ju, Feb 18, 2022
    Method setS2 used for scaling, to fit coordinates into space given width and height
    Takes in params width and height, returns scaling matrix
    '''
    def __setS2(self,width,height):
        
        # creates and initializes matrix with zeros
        S2 = matrix(np.zeros((4,4)))
        # Sets vals
        S2.set(0, 0, width/2)
        S2.set(1, 1, height/2)
        S2.set(2, 2, 1)
        S2.set(3, 3, 1)

        # returns matrix
        return S2

    '''
    Terrence Ju, Feb 18, 2022
    Method setW2 used for transforming the origin to top left corner
    Returns matrix for transformation
    '''
    def __setW2(self,height):

        # Creates and initializes matrix with zeros
        W2 = matrix(np.zeros((4,4)))
        # Sets vals
        W2.set(0, 0, 1)
        W2.set(1, 1, -1)
        W2.set(1, 3, height)
        W2.set(2, 2, 1)
        W2.set(3, 3, 1)

        # Returns matrix
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