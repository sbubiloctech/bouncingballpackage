import math
from ballpackage_ubiloctech.mathcorrections import convertDegtoRad, convertRadtoDeg

# Class Vector (2D)
class Vector:
    
    # Vector object initializer
    def __init__(self, a = 0, b = 0) -> None:
        self.vx = a
        self.vy = b

    # Converts radial vector to Cartesian vector
    def convertToCartesian(self, vrad, theta) -> None:
        self.vx = vrad * math.cos(convertDegtoRad(theta))
        self.vy = vrad * math.sin(convertDegtoRad(theta))

        if abs(self.vx) < 0.00001:
            self.vx = 0

        if abs(self.vy) < 0.00001:
            self.vy = 0
        


    # Get vector components
    def getComponents(self) -> ():
        return self.vx, self.vy
    
    # Set vector components
    def setComponents(self, vx, vy) -> None:
        self.vx = vx
        self.vy = vy

    # Calculates vector magnitude based on Cartesian components
    def calculateMag(self) -> int:
        return round(math.sqrt(self.vx ** 2 + self.vy ** 2))
    
    # Converts to radial vector based on Cartesian components
    def convertToRTheta(self) -> ():
        rad = self.calculateMag()

        theta = 0
        if self.vx == 0:
            if self.vy > 0:
                theta = 90
            elif self.vy < 0:
                theta = 270
            else:
                theta = 0
        else:
            theta = convertRadtoDeg(math.atan(self.vy/self.vx))
            if self.vy < 0 and self.vx < 0: 
                theta += 180
            elif self.vy > 0 and self.vx < 0:
                theta = 180 + theta
            elif self.vy < 0 and self.vx > 0:
                theta += 360
            else:
                pass

        return rad, theta
    
    # Returns a vector after adding a vector b to self
    def addVectors(self, b):
        v = Vector(self.vx + b.vx, self.vy + b.vy)
        return v
    
    # Returns a vector after subtracting self from a vector b 
    def subtVectors(self, b):
        v = Vector(b.vx - self.vx, b.vy - self.vy)
        return v
    
    def dotProduct(self, b):
        return (self.vx * b.vx + self.vy * b.vy)
    
    def calculateUnitVector(self):
        m = self.calculateMag()

        if m > 0:
            return Vector(self.vx/m, self.vy/m)
        else:
            return Vector(0,0)
    
    def calculateDirectionVector(self, b):
        bVec = Vector(*b.convertToGridPoint())
        return self.subtVectors(bVec)
    
    def calculateScaledVector(self, mag):
        return Vector(mag * self.vx, mag * self.vy)

# End class Vector
