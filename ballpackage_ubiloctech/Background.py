
import pandas as pd
import time
import random
from threading import Thread

from ballpackage_ubiloctech.BouncingBall import BouncingBall

# Class Background - holds a set of bouncing balls between 4 walls
class Background:

    def __init__(self, w_w, w_h, x_partition, y_partition, t_w, t_c, s_size = 2, t_d = 1, t_color = 'red',ballN = 2, eCoefft = 1) -> None:
        self.screenWidth = w_w
        self.screenHeight = w_h
        self.gridScreenWidth = x_partition
        self.gridScreenHeight = y_partition
        self.x_incr = round(self.screenWidth/x_partition)
        self.y_incr = round(self.screenHeight/y_partition)
        self.ballColor = t_color
        self.bouncingballList: BouncingBall = []

        if s_size > 2:
            self.ballSize = s_size
        else:
            raise Exception('Ball size is less than 2')
        
        if eCoefft >= 0 and eCoefft <= 1:
            self.eCoefft = eCoefft
        else:
            self.eCoefft = 1
        
        self.tCanvas = t_c
        self.tWindow = t_w
        self.tdelay = t_d
        self.prev_time = time.time()
        self.time_now = self.prev_time

        # Initialize ball list here
        [self.bouncingballList.append(BouncingBall(w_w,w_h,x_partition,y_partition,s_size, t_c, t_w,t_d)) for i in range(0,ballN)]
        [self.initRandomBallParam(self.bouncingballList[i], i) for i in range(0, ballN)]
        [ball.initScribe() for ball in self.bouncingballList]


    def initRandomBallParam(self,ball:BouncingBall, loc):
        isFirst = True
        initComplete = False

        smallestRes = round(0.09 * (self.gridScreenHeight if self.gridScreenHeight < self.gridScreenWidth else self.gridScreenWidth))
        while isFirst or not initComplete:
            initV = random.randint(2, smallestRes)
            initTheta = random.randint(10,350)
            ball.setDir(initV, initTheta)
            # Add ball location
            initx = random.randint(initV + 1, self.gridScreenWidth - initV - 1)
            inity = random.randint(initV + 1, self.gridScreenHeight - initV - 1)
            ball.setScribe(initx, inity, self.ballColor)

            # Check for same location of balls
            initComplete = True
            if loc > 0:
                for j in range(0, loc):
                    if ball.isLocationMatched(self.bouncingballList[j]):
                        initComplete = False
                        break
    
            isFirst = False

    # Multi-ball - Ball to ball collision check and correction
    def multiBallCollision(self, rLim = 0.2, rFlag = False):
        listLen = len(self.bouncingballList)

        for i in range(0,listLen-1):
            for j in range(i+1, listLen):
                ball:BouncingBall = self.bouncingballList[i]
                ball.correctforBallCollision(self.bouncingballList[j], self.eCoefft, rLim, rFlag)

    # Multi-ball - Ball to ball and wall collision and correction function
    def multiBallCorrections(self, rLim = 0.2, rFlag = False):
        self.multiBallCollision(rLim, rFlag)
        [ball.correctForWallBounce(self.eCoefft, rLim, rFlag) for ball in self.bouncingballList]
        [ball.moveDir() for ball in self.bouncingballList]
        

    # Multi-ball bounce - single iteration
    def multiBallBounce(self, rLim = 0.2, rFlag = False, thread: Thread = None, executeOnSeparateThread = False):
        
        # global prev_time, time_now
        
        self.multiBallCollision(rLim, rFlag)
        [ball.correctForWallBounce(self.eCoefft, rLim, rFlag) for ball in self.bouncingballList]
        [ball.moveDir() for ball in self.bouncingballList]
                             
        self.tCanvas.update()

        time_now = time.time()
        diff_time = self.time_now - self.prev_time
        if diff_time >= 5:
            if not executeOnSeparateThread:
                self.saveBackground()
            elif executeOnSeparateThread and not thread:
                thread = Thread(self.saveBackground())
                thread.start()
            elif executeOnSeparateThread and not thread.is_alive():
                thread = Thread(self.saveBackground())
                thread.start()
            else:
                print(f'Thread {thread.native_id} is still writing')
                pass
            
            self.prev_time = self.time_now

        self.tWindow.after(int(self.tdelay*1000), self.multiBallBounce, rLim, rFlag, thread, executeOnSeparateThread)
        time_now = time.time()
        
        
        
    def saveBackground(self):
        bg_dict = {}
        bg_dict['objectType'] = 'Background'
        bg_dict.update(vars(self).copy())

        bg_dict.pop('tWindow')
        bg_dict.pop('tCanvas')
        bg_dict.pop('bouncingballList')
        bg_dict['ballN'] = len(self.bouncingballList)
       

        ball_count = 1
        for ball in self.bouncingballList:
            ball_dict = {}
            ball_d2 = {}
            ball_d = vars(ball).copy()
            ball_d2['x'] = ball_d['x']
            ball_d2['y'] = ball_d['y']
            ball_d2['velocity'] = ball_d['velocity']
            ball_d2['theta'] = ball_d['theta']
            ball_dict['Ball' + str(ball_count)] = ball_d2

            bg_dict.update(ball_dict)
            ball_count += 1

      
        df = pd.DataFrame(bg_dict)
     
        df.to_csv('Test1.csv')

    def loadBackground(self, rLim = 0.2, rFlag = False):
        global hasLoaded

        hasLoaded = True
        df = pd.read_csv('Test1.csv')
        bg_dict = df.to_dict()
        bg_dict.pop('Unnamed: 0')
        bg_dict.pop('objectType')
        sWidth = bg_dict['screenWidth'][0]
        sHeight = bg_dict['screenHeight'][0]
        xpart = bg_dict['gridScreenWidth'][0]
        ypart = bg_dict['gridScreenHeight'][0]
        bColor = bg_dict['ballColor'][0]
        bSize = bg_dict['ballSize'][0]
        eCofft = bg_dict['eCoefft'][0]
        bNum = bg_dict['ballN'][0]
        tdelay = bg_dict['tdelay'][0]
       
        self.tCanvas.delete('all')
               
        window = self.tWindow

        window.title("Bouncing Ball Demo")

        canvas = self.tCanvas 
        self = Background(sWidth, sHeight, xpart, ypart, window, canvas, bSize,
                                 tdelay, bColor, bNum, eCofft)
        
        for num in range(1,bNum+1):
            key = 'Ball' + str(num)
            self.bouncingballList[num-1].moveScribe(bg_dict[key][0]/self.bouncingballList[num-1].x_incr, 
                                                    bg_dict[key][1]/self.bouncingballList[num-1].y_incr)
            self.bouncingballList[num-1].setDir(bg_dict[key][2], bg_dict[key][3])
        
        canvas.update()

        window.after_idle(self.multiBallBounce, rLim, rFlag)
        prev_time = time.time()

        window.mainloop()
        
                
# End class Background  