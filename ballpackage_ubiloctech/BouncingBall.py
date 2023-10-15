import tkinter as tk
from tkinter import TclError
import math
import random


from ballpackage_ubiloctech.Vector import Vector
from ballpackage_ubiloctech.CustomExceptions import ThetaException, VelocityException, ResolutionException, RandomFactorException
from ballpackage_ubiloctech.mathcorrections import correctedAngle, convertDegtoRad, QuadSolution


# Exception handler wrapper function
def exceptionHandlerWrapper(func,*args):
    def wrapper(*args):
        try:
            func(*args)
        except ThetaException as e:
            if func.__name__ == 'setTheta':
                func(args[0], correctedAngle(args[1]))
                print(e.message)
        except VelocityException as e:
            if func.__name__ == 'setVelocity':
                func(args[0], 3)
                print(e.message)
                print(f'Current grid size: ({args[0].gridScreenWidth}, {args[0].gridScreenHeight})')
 
    return wrapper





class BouncingBall:
       
    # Constructor
    def __init__(self, w_w, w_h, x_partition, y_partition, s_size,t_c, t_w, t_d = 1, t_v = 2, t_theta = 60) -> None:
        self.screenWidth = w_w # Screen Width in pixels
        self.screenHeight = w_h # Screen Height in pixels
        self.gridScreenWidth = x_partition  # Screen Width in grid units
        self.gridScreenHeight = y_partition # Screen Height in grid units
        self.x_incr = round(self.screenWidth/x_partition)  # x increments of movement
        self.y_incr = round(self.screenHeight/y_partition) # y increments of movement

        if self.x_incr <= 0 or self.y_incr <= 0:
            raise ResolutionException
        
        self.x = x_partition * self.x_incr / 2
        self.y = y_partition * self.y_incr / 2
        self.velocity = t_v #in grid points per iteration
        self.theta = self.setTheta(t_theta) #in degrees
        if s_size >= 2: self.scribeSize = s_size # Size of the ball
        self.tCanvas:tk.Canvas = t_c # Canvas object
        self.tWindow:tk = t_w # Window object
        self.tdelay = t_d  # Time between each iteration


    # Bounds Function
    def isWithinBounds(self, x1, y1) -> bool:
        xCoord = x1 * self.x_incr
        yCoord = y1 * self.y_incr

        bounds = self.scribeSize/2
        

       # if xCoord >= (self.screenWidth - bounds) or xCoord <= bounds:
        if xCoord >= self.screenWidth or xCoord <= 0:
            return False
        
       # if yCoord >= (self.screenHeight - bounds) or yCoord <= bounds:
        if yCoord >= self.screenHeight or yCoord <= 0:
            return False
        
        return True

    def GUIElementsExist(self) -> bool:
        if self.tCanvas == 0 or self.tWindow == 0:
            return False
        else:
            return True
        

    # Convert to grid point
    def convertToGridPoint(self) -> ():
        return (int(self.x / self.x_incr), int(self.y / self.y_incr))
    
    # Set Theta - Set angular movement
    # Use after Terminal Scribe object initialized and initScribe(), setScribe()
    @exceptionHandlerWrapper
    def setTheta(self, angle):
        if angle < 0 or angle > 360:
            raise ThetaException(angle)
        else:
            self.theta = round(angle)

    # Set Velocity - Set absolute velocity
    # Use after Terminal Scribe object initialized and initScribe(), setScribe()
    @exceptionHandlerWrapper
    def setVelocity(self, velocity):
        if velocity <= 0:
            raise VelocityException(velocity)
        
        if velocity >= self.gridScreenWidth / 10 or velocity >= self.gridScreenHeight / 10:
            raise VelocityException(velocity)
        
        self.velocity = round(velocity)

    #Calculate Final Coordinates. Use after setDir()
    def calculateDirectionalMove(self, rlim = 0.2, rFlag = False) -> ():
        start_x, start_y = self.convertToGridPoint()

        if rFlag:
            if rlim < 0 or rlim >= 1:
                raise RandomFactorException
            
            rFactor = random.uniform(-rlim, rlim)
            self.theta += rFactor * self.theta
        
        final_x = round(start_x + self.velocity * math.cos(convertDegtoRad(self.theta)))
        final_y = round(start_y + self.velocity * math.sin(convertDegtoRad(self.theta)))
        return final_x, final_y
       

    #Define position of Scribe
    #Use after Terminal Scribe object instantiated
    def setScribe(self, x1, y1, color = 'red') -> None:
        
        xCoord = x1 * self.x_incr
        yCoord = y1 * self.y_incr

        bounds = self.scribeSize/2

        #Check if cursor will be out of bounds of canvas
        if xCoord <= self.screenWidth - bounds and xCoord >= bounds:
            self.x = xCoord
        else:
            self.x = 0

        if yCoord <= self.screenHeight - bounds and yCoord >= bounds:  
            self.y = yCoord
        else:
            self.y = 0

        self.scribeColor = color

    # Check if location is matched
    def isLocationMatched(self, ball) -> bool:
        x1, y1 = self.convertToGridPoint()
        x2, y2 = ball.convertToGridPoint()

        if x1 == x2 and y1 == y2:
            return True
        else:
            return False

    #Create the scribe object and initially show on screen
    #Use after Canvas created and setScribe()
    def initScribe(self) -> int:
        bounds = self.scribeSize / 2

        try: 
            self.scribeObj = self.tCanvas.create_oval(self.x - bounds, self.y - bounds, self.x + bounds, self.y + bounds, width = 10, fill = self.scribeColor)
        except TclError as e:
            initx = round(self.gridScreenWidth / 2)
            inity = round(self.gridScreenHeight / 2)
            self.setScribe(initx, inity,'red')
            self.scribeColor = 'red'
            self.scribeObj = self.tCanvas.create_oval(self.x - bounds, self.y - bounds, self.x + bounds, self.y + bounds, width = 10, fill = self.scribeColor)


        return self.scribeObj 
    
    # Increment scribe
    # Internal function to moveScribe()
    def incrScribe(self, x1, y1) -> bool:
        xCoord_incr = x1 * self.x_incr
        yCoord_incr = y1 * self.y_incr

        prev_x = self.x
        prev_y = self.y

        self.x = self.x + xCoord_incr
        self.y = self.y + yCoord_incr
        testx, testy = self.convertToGridPoint()

        if not self.isWithinBounds(testx, testy):
            self.x = prev_x
            self.y = prev_y
            return False
        else: return True

 
    # Move scribe
    # Use only after initScribe()
    def moveScribe(self, x1, y1) -> bool:
        prev_x = self.x
        prev_y = self.y
        
        boundsFlag = self.incrScribe(x1,y1)

        if boundsFlag == True and self.GUIElementsExist() == True:
            self.tCanvas.move(self.scribeObj, self.x - prev_x, self.y - prev_y)
        
        return boundsFlag
    

    def setTimeDelay(self, t_d = 1) -> bool:
        if t_d < 0.01:
            return False
        
        self.tdelay = t_d
        return True
        
    # Place a Dot to draw shapes/paths
    # Use after scribe/ball is fully initialized, instantiated and drawn
    def placeDot (self) -> None:
        bounds = self.scribeSize / 10

        self.tCanvas.create_oval(self.x - bounds, self.y - bounds, self.x + bounds, self.y + bounds, fill = "white")

   
    # Set scribe direction and intercepts
    # Use after initScribe() or moveScribe()
    def setDir(self,t_velocity, t_theta) -> bool:
        self.setVelocity(t_velocity)
        self.setTheta(t_theta)

        self.intercept_x = 0
        (x_g, y_g) = self.convertToGridPoint()

        if self.theta != 90 and self.theta != 270:
            slope = math.tan(convertDegtoRad(self.theta)) 
            self.intercept_y = y_g - slope * x_g
        else:
            self.intercept_y = 0
        
        return True
    
        
    # Move in given direction based on Velocity and Theta. 
    # Use after setDir()
    def moveDir(self) -> bool:
        start_x, start_y = self.convertToGridPoint()
        final_x, final_y = self.calculateDirectionalMove()

        if not self.isWithinBounds(final_x, final_y) or not self.GUIElementsExist():
            return False


        return self.moveScribe(final_x - start_x, final_y - start_y)
    
       
    # Corrects the velocity after simulating a bounce on the wall
    # Use after initScribe() or initial location set and initial setDir()
    def correctForWallBounce(self, eCoefft = 1, rLim = 0.2, rFlag = False):
        global hasLoaded

        hasChanged = False
        final_x, final_y = self.calculateDirectionalMove()
        
        velocityVector = Vector()
        velocityVector.convertToCartesian(self.velocity,self.theta)
        vx, vy = velocityVector.getComponents()

        if final_x <= 0 or final_x >= self.gridScreenWidth:
            vx = -vx * math.sqrt(eCoefft)
            hasChanged = True
          
        
        if final_y <= 0 or final_y >= self.gridScreenHeight:
            vy = -vy * math.sqrt(eCoefft)
            hasChanged = True


        if hasChanged:
            velocityVector.setComponents(vx, vy)
            self.velocity, self.theta = velocityVector.convertToRTheta()
            if rFlag:
                self.theta += random.randint(round(-rLim * self.theta), round(rLim * self.theta))

    def correctforBallCollision(self, ball, eCoefft = 1, rLim = 0.2, rFlag = False) -> bool:
        hasChanged = False
        bounds = self.scribeSize
        final_x, final_y = self.calculateDirectionalMove()
        final_x_b, final_y_b = ball.calculateDirectionalMove()
        smallestRes = self.gridScreenHeight if self.gridScreenHeight < self.gridScreenWidth else self.gridScreenWidth
        smallestRes = round(smallestRes/10)
        distVector = Vector((final_x_b - final_x) * self.x_incr, (final_y_b - final_y) * self.y_incr)
        
        if distVector.calculateMag() <= bounds:
            selfDirVector = Vector(final_x, final_y)
            ballDirVector = Vector(final_x_b, final_y_b)
            selfVelocityVector = Vector()
            selfVelocityVector.convertToCartesian(self.velocity,self.theta)
            ballVelocityVector = Vector()
            ballVelocityVector.convertToCartesian(ball.velocity, ball.theta)
            diffDirVector = selfDirVector.subtVectors(ballDirVector)
            unitCollisionVector = diffDirVector.calculateUnitVector()
            diffVelocityVector = selfVelocityVector.subtVectors(ballVelocityVector)
            elasticForceMag = unitCollisionVector.dotProduct(diffVelocityVector)
            inelasticConstant = (1 - eCoefft) * (selfVelocityVector.calculateMag() ** 2 + ballVelocityVector.calculateMag() ** 2) / 2
            r1, r2 = QuadSolution(1, -elasticForceMag, inelasticConstant)
 
            if r1 <= 0 and r2 <= 0:
                forceMag = 0
            elif r1 <= 0:
                forceMag = r2
            else:
                forceMag = r1
            forceMag = 0 if forceMag < 0 else forceMag
            forceMag = smallestRes if forceMag > smallestRes else forceMag
            forceVector = unitCollisionVector.calculateScaledVector(forceMag)
            
            selfVelocityVector = selfVelocityVector.addVectors(forceVector)
            ballVelocityVector = forceVector.subtVectors(ballVelocityVector)
          
            self.velocity, self.theta = selfVelocityVector.convertToRTheta()
            ball.velocity, ball.theta = ballVelocityVector.convertToRTheta()
            
            if rFlag:
                self.theta += random.randint(round(-rLim * self.theta), round(rLim * self.theta))
                ball.theta += random.randint(round(-rLim * ball.theta), round(rLim * ball.theta))

            hasChanged = True

        return hasChanged
    
# End of class BouncingBall
           
