# -*- coding: utf-8 -*-
# @Time    : 2020/9/13 22:53
# @Author  : Baokang_Xie
# @FileName: Detection_class_test.py
# @Software: PyCharm

import math, time, cv2, numpy
from naoqi import ALProxy, ALModule
from movement import standWithStick2, standWithStick5
from movement import releaseStick, catchStick, raiseStick
cv_version = cv2.__version__.split(".")[0]
if cv_version == "2": # for OpenCV 2
	import cv2.cv as cv


#------全局变量---------

naoMarkDiameter = 0.0913

class BasicNao(object):
    def __init__(self, IP):
        self.IP = IP
        self.PORT = 9559
        self.MEMORY = ALProxy("ALMemory", self.IP, self.PORT)
        self.MOTION = ALProxy("ALMotion", self.IP, self.PORT)
        self.CAMERA = ALProxy("ALVideoDevice", self.IP, self.PORT)
        self.TTS = ALProxy("ALTextToSpeech", self.IP, self.PORT)
        self.LANDMARK = ALProxy("ALLandMarkDetection", self.IP, self.PORT)


class BasicVison(BasicNao):
    def __init__(self, IP):
        super(BasicVison, self).__init__(IP)
        self.resolution = 2
        self.colorSpace = 13
        self.fps = 20
        self.frameArray = None
        self.frameWidth = 0
        self.frameHeight = 0
        self.bottomCameraDirection = [1.2, 39.7]
        self.cameraPitchRange = 47.64 / 180 * numpy.pi
        self.cameraYawRange = 60.97 / 180 * numpy.pi


    def updateFrame(self,cameraID):
        self.CAMERA.setActiveCamera(cameraID)
        self.videoClient = self.CAMERA.subscribe("python_client", self.resolution, self.colorSpace, self.fps)
        naoImage = self.CAMERA.getImageRemote(self.videoClient)
        self.CAMERA.unsubscribe(self.videoClient)
        try:
            self.frameWidth = naoImage[0]
            self.frameHeight = naoImage[1]
            self.frameChannels = naoImage[2]
            self.frameArray = numpy.frombuffer(naoImage[6], dtype=numpy.uint8).reshape([naoImage[1],naoImage[0],naoImage[2]])
        except IndexError:
            print 'There is error in updateFrame()!'


    def printFrameData(self):
        print("frame height = ", self.frameHeight)
        print("frame width = ", self.frameWidth)
        print("frame channels = ", self.frameChannels)
        print("frame shape = ", self.frameArray.shape)


    def showFrame(self):
        if self.frameArray is None:
            print 'please get an image from Nao with the method updateFrame()!'
        else:
            cv2.imshow('original_frame', self.frameArray)


class AllDistance(BasicVison):
    def __init__(self, IP):
        super(AllDistance,self).__init__(IP)
        self.kernel = numpy.ones((5, 5), numpy.uint8)
        self.minPerimeter = self.frameHeight / 8.0
        self.minArea = self.frameHeight * self.frameWidth / 1000.0
        self.kernelErosion = numpy.ones((5, 5), numpy.uint8)
        self.kernelDilation = numpy.ones((5, 5), numpy.uint8)


    def redballdispose(self, S1, V1, H1, H2, cameraID):
        minHSV1 = numpy.array([0, S1, V1])
        maxHSV1 = numpy.array([H1, 255, 255])
        minHSV2 = numpy.array([H2, S1, V1])
        maxHSV2 = numpy.array([180, 255, 255])
        self.updateFrame(cameraID)
        try:
            imgHSV = cv2.cvtColor(self.frameArray, cv2.COLOR_BGR2HSV)
        except:
            print 'no image!'
        else:
            frameBin1 = cv2.inRange(imgHSV, minHSV1, maxHSV1)
            frameBin2 = cv2.inRange(imgHSV, minHSV2, maxHSV2)
            frameBin = numpy.maximum(frameBin1, frameBin2)
            #opening = cv2.morphologyEx(frameBin, cv2.MORPH_OPEN, self.kernel)
            frameBin = cv2.GaussianBlur(frameBin, (9, 9), 1.5)
        minDist = int(self.frameHeight / 20.0)
        minRadius = 5
        maxRadius = int(self.frameHeight / 12)
        cv_version = cv2.__version__.split(".")[0]
        if cv_version >= "3":  # for OpenCV >= 3.0.0
            gradient_name = cv2.HOUGH_GRADIENT
        else:
            gradient_name = cv.CV_HOUGH_GRADIENT
        circles = cv2.HoughCircles(numpy.uint8(frameBin), gradient_name, 1, minDist,
                                   param1=150, param2=15, minRadius=minRadius, maxRadius=maxRadius)
        #cv2.imshow('sss', frameBin)
        #cv2.waitKey(0)
        if circles is None:
            circles = numpy.uint16([])
        else:
            circles = numpy.uint16(numpy.around(circles[0, ]))
        if circles.shape[0] == 0:
            return circles
        rRatioMin = 1.0
        circleSelected = numpy.uint16([])
        for circle in circles:
            centerX = circle[0]
            centerY = circle[1]
            radius = circle[2]
            initX = centerX - 2 * radius
            initY = centerY - 2 * radius
            if initX < 0 or initY < 0 or (initX + 4 * radius) > self.frameWidth or (
                    initY + 4 * radius) > self.frameHeight or radius < 1:
                continue
            rectBallArea = self.frameArray[initY:initY + 4 * radius + 1, initX:initX + 4 * radius + 1, :]
            bFlat = numpy.float16(rectBallArea[:, :, 0].flatten())
            gFlat = numpy.float16(rectBallArea[:, :, 1].flatten())
            rFlat = numpy.float16(rectBallArea[:, :, 2].flatten())
            rScore1 = numpy.uint8(rFlat > 1.0 * gFlat)
            rScore2 = numpy.uint8(rFlat > 1.0 * bFlat)
            rScore = float(numpy.sum(rScore1 * rScore2))
            gScore = float(numpy.sum(numpy.uint8(gFlat > 1.0 * rFlat)))
            rRatio = rScore / len(rFlat)
            gRatio = gScore / len(gFlat)
            if rRatio >= 0.12 and gRatio >= 0.1 and abs(rRatio - 0.19) < abs(rRatioMin - 0.19):
                circleSelected = circle
        return circleSelected


    def stickdispose(self, minH, minS, minV, maxH, cameraID):
        minHSV = numpy.array([minH, minS, minV])
        maxHSV = numpy.array([maxH, 255, 255])
        self.updateFrame(cameraID)
        rects = []
        try:
            frameHSV = cv2.cvtColor(self.frameArray, cv2.COLOR_BGR2HSV)
        except ImportError:
            print("There is error in stickdispose()!")
        frameBin = cv2.inRange(frameHSV, minHSV, maxHSV)
        frameBin = cv2.erode(frameBin, self.kernelErosion, iterations=1)
        frameBin = cv2.dilate(frameBin, self.kernelDilation, iterations=1)
        frameBin = cv2.GaussianBlur(frameBin, (9, 9), 0)
        if cv_version == "2" or cv_version == "4":
            contours, _ = cv2.findContours(frameBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else:
            _, contours, _ = cv2.findContours(frameBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) == 0:
            return rects
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            area = cv2.contourArea(contour)
            if perimeter > self.minPerimeter and area > self.minArea:
                x, y, w, h = cv2.boundingRect(contour)
                rects.append([x, y, w, h])
        if len(rects) == 0:
            return rects
        rects = [rect for rect in rects if (1.0 * rect[3] / rect[2]) > 0.8]
        if len(rects) == 0:
            return rects
        rects = numpy.array(rects)
        rect = rects[numpy.argmax(1.0 * (rects[:, -1]) / rects[:, -2]), ]
        lastrect = numpy.array([rect[0]+rect[2]/2, rect[1]+rect[3]])
        return lastrect


    def allDistance(self, location, hight, cameraID, dis):
        self.Position = []
        ballData = {"centerX": location[0], "centerY": location[1]}
        cameraDirection = self.bottomCameraDirection[cameraID]
        centerX = ballData["centerX"]
        centerY = ballData["centerY"]
        if cameraID == 0:
            cameraPosition = self.MOTION.getPosition("CameraTop", 2, True)
        else:
            cameraPosition = self.MOTION.getPosition("CameraBottom", 2, True)
        cameraHeight = cameraPosition[2]
        cameraX = cameraPosition[0]
        cameraY = cameraPosition[1]
        headPitches = self.MOTION.getAngles("HeadPitch", True)
        headPitch = headPitches[0]
        headYaws = self.MOTION.getAngles("HeadYaw", True)
        headYaw = headYaws[0]
        ballPitch = (centerY - 240.0) * self.cameraPitchRange / 480.0
        ballYaw = (320.0 - centerX) * self.cameraYawRange / 640.0
        dPitch = (cameraHeight - hight) / numpy.tan((cameraDirection+3) / 180 * numpy.pi + headPitch + ballPitch)
        dYaw = dPitch / numpy.cos(ballYaw)
        if not dis:
            #短距离补偿
            dYaw = -0.0233 * dYaw ** 4 + 0.0833 * dYaw ** 3 - 0.1188 * dYaw ** 2 + 1.0450 * dYaw - 0.0123
        else:
            #长距离补偿
            dYaw = 0.0186 * dYaw ** 4 - 0.2594 * dYaw ** 3 + 1.2442 * dYaw ** 2 - 1.7217 * dYaw + 1.8826
        ballX = dYaw * numpy.cos(ballYaw + headYaw) + cameraX
        ballY = dYaw * numpy.sin(ballYaw + headYaw) + cameraY
        ballYaw = numpy.arctan2(ballY, ballX)
        self.Position.append(dYaw)
        self.Position.append(ballYaw)


    def alignBallandStick(self):
        pass


class AllDetection(AllDistance):
    def __init__(self, IP):
        super(AllDetection, self).__init__(IP)
        self.memvalue1 = "LandmarkDetected"
        self.size = 0
        self.period = 500


    def redBallDetection(self, moveConfig2, S1, V1, H1, H2, cameraID, addAngle):
        self.MOTION.setMoveArmsEnabled(False, False)
        standWithStick5(0.5, self.IP, self.PORT)
        self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
        self.MOTION.angleInterpolation("HeadPitch", (addAngle+17) * math.pi / 180.0, 0.5, False)
        for i in range(3):
            if addAngle > 0:
                if i == 1:
                    self.MOTION.angleInterpolation("HeadPitch", -6 * math.pi / 180.0, 0.5, False)
                elif i == 2:
                    self.MOTION.angleInterpolation("HeadPitch", -6.5 * math.pi / 180.0, 0.5, False)
            else:
                if i == 1:
                    self.MOTION.angleInterpolation("HeadPitch", 6 * math.pi / 180.0, 0.5, False)
                elif i == 2:
                    self.MOTION.angleInterpolation("HeadPitch", 6.5 * math.pi / 180.0, 0.5, False)
            for j in range(3):
                time.sleep(1)
                if not j: derct = 0
                elif j % 2: derct = 1
                else: derct = -1
                self.MOTION.angleInterpolation("HeadYaw", derct*45*math.pi/180, 0.5, True)
                if cameraID == "all":#全部摄像头都用
                    circle = self.redballdispose(S1, V1, H1, H2, 0)
                    if len(circle):
                        break
                    circle = self.redballdispose(S1, V1, H1, H2, 1)
                else:#只使用顶部或者底部摄像头,左正有负
                    circle = self.redballdispose(S1, V1, H1, H2, cameraID)
                if len(circle):
                    break
            else:
                continue
            break
        if not len(circle):
            return []
        if derct != 0:
            if cameraID != 'all':
                self.allDistance(circle, 0.02, cameraID, 0)
            else:
                cameraid = self.CAMERA.getActiveCamera()
                self.allDistance(circle, 0.02, cameraid, 0)
            self.MOTION.angleInterpolation("HeadPitch", 0, 0.5, True)
            self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
            self.MOTION.moveTo(0, 0, self.Position[1], moveConfig2)
            print self.Position[0], self.Position[1]*180.0/math.pi
            return self.redBallDetection(moveConfig2, S1, V1, H1, H2, cameraID, addAngle)
        else:
            if cameraID == 'all':
                cameraid = self.CAMERA.getActiveCamera()
                self.allDistance(circle, 0.02, cameraid, 0)
                print self.Position[0], self.Position[1]*180.0/math.pi
                return self.Position
            self.allDistance(circle, 0.02, cameraID, 0)
            self.MOTION.angleInterpolation("HeadPitch", 0, 0.5, True)
            self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
            print self.Position[0], self.Position[1]*180.0/math.pi
            return self.Position


    def naoMarkDetection(self):
        alpha = 0
        pianlist = [0, -1, -2, 1, 2]
        self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
        self.MOTION.angleInterpolation("HeadPitch", 0, 0.5, True)
        time.sleep(0.5)
        for i in range(2):
            for j in pianlist:
                self.MOTION.angleInterpolation("HeadYaw", j*(45*math.pi/180.0), 0.5, True)
                time.sleep(2.5)
                self.LANDMARK.subscribe("Test_LandMark", self.period, 0.0)
                for i in range(5):
                    val = self.MEMORY.getData(self.memvalue1)
                print val
                self.LANDMARK.unsubscribe("Test_LandMark")
                if (val and isinstance(val, list) and len(val) >= 2):
                    markInfo = val[1]
                    shapeInfo = markInfo[0]
                    rshapeInfo = shapeInfo[0]
                    alpha = rshapeInfo[1]
                    self.size = rshapeInfo[4]
                    self.angleFlag = 0
                    break
            else:
                continue
            break
        if isinstance(alpha, int):
            return []
        if (j == 1):
            alpha += 45 * math.pi / 180
        elif (j == -1):
            alpha -= 45 * math.pi / 180

        elif (j == 2):
            alpha += 90 * math.pi / 180
        elif (j == -2):
            alpha -= 90 * math.pi / 180
        distMark = (naoMarkDiameter / self.size) / math.cos(alpha)
        return [distMark, alpha, 0]


    def yellowStickDetection(self, minH, minS, minV, maxH, dis):
        standWithStick5(0.5, self.IP, self.PORT)
        self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
        self.MOTION.angleInterpolation("HeadPitch", 16*math.pi/180.0, 0.5, True)
        for i in range(3):
            for j in range(3):
                time.sleep(1)
                if not j: derct = 0
                elif j % 2: derct = -1
                else: derct = 1
                self.MOTION.angleInterpolation("HeadYaw", (derct*45)*math.pi/180.0, 0.5, True)
                bottommost = self.stickdispose(minH, minS, minV, maxH, 0)
                if len(bottommost):
                    break
            else:
                continue
            break
        if not len(bottommost):
            return []
        self.allDistance(bottommost, 0, 0, dis)
        print [self.Position[0], self.Position[1]]
        return [self.Position[0], self.Position[1]]


class OptimizeData(AllDetection):
    def __init__(self, IP):
        super(OptimizeData, self).__init__(IP)


    def redBallReference(self, moveConfig2, S1, V1, H1, H2):
        self.MOTION.moveTo(0, 0, 45*math.pi/180.0, moveConfig2)
        self.MOTION.moveTo(0.30/math.cos(45*math.pi/180.0), 0, 0, moveConfig2)
        self.robotRotate(-135*math.pi/180.0, moveConfig2)
        det, angle = self.redBallDetection(moveConfig2, S1, V1, H1, H2, 1, 5)
        self.MOTION.moveTo(det-0.3, 0, angle * math.pi / 180.0, moveConfig2)


    def searchRedBall(self, moveConfig2, S1, V1, H1, H2, angle):
        self.MOTION.moveTo(0.5, 0, -5 * math.pi / 180.0, moveConfig2)
        redBallInfo = self.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', angle)
        if not len(redBallInfo):
            self.MOTION.moveTo(0, 0, 45 * math.pi / 180.0, moveConfig2)
            redBallInfo = self.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', angle)
        if not len(redBallInfo):
            self.MOTION.moveTo(0, 0, -45 * math.pi / 180.0, moveConfig2)
            time.sleep(0.5)
            self.MOTION.moveTo(0, 0, -45 * math.pi / 180.0, moveConfig2)
            redBallInfo = self.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', angle)
        self.MOTION.moveTo(0, 0, 45 * math.pi / 180.0, moveConfig2)
        return redBallInfo


    def calculation(self, redBallInfo,targetInfo):

        angleRobotAndBall = redBallInfo[1]#角度 人球
        angleRobotAndTarget = targetInfo[1]#角度 人洞
        distRobotToBall = redBallInfo[0]# 距离 人球
        distRobotToTarget = targetInfo[0]#距离人洞

        alpha = abs( angleRobotAndBall - angleRobotAndTarget)
        distBallToTarget2 = distRobotToBall**2 + distRobotToTarget**2 -2*distRobotToBall*distRobotToTarget*math.cos(alpha)
        distBallToTarget = math.sqrt(distBallToTarget2)

        theta2 = (distRobotToBall**2 + distBallToTarget2 - distRobotToTarget**2)/(2*distRobotToBall*distBallToTarget)
        theta = math.acos(theta2)     #theta ：distRobotToBall 和 distBallToTarget 夹角

        if angleRobotAndBall - angleRobotAndTarget >= 0:
            if theta >= math.pi/2:
                #angle:锐角，负;    x： 正;   y: 正
                angle = theta - math.pi + angleRobotAndBall
                x = -distRobotToBall*math.cos(theta)
                y = distRobotToBall*math.sin(theta)
            else:
                #angle:钝角, 负;    x: 负;   y: 正
                angle = theta - math.pi + angleRobotAndBall
                x = -distRobotToBall*math.cos(theta)
                y = distRobotToBall*math.sin(theta)
        else:
            if theta >= math.pi/2:
                #angle: 锐角, 正;  x: 正;   y: 负
                angle = math.pi - theta + angleRobotAndBall
                x = -distRobotToBall*math.cos(theta)
                y = -distRobotToBall*math.sin(theta)
            else:
                #angle: 钝角, 正;  x: 负;   y: 负
                angle = math.pi - theta + angleRobotAndBall
                x = -distRobotToBall*math.cos(theta)
                y = -distRobotToBall*math.sin(theta)
        print "finalx = ",x,"finaly = ",y
        print "finalAngle = ",angle
        return [angle,x,y]


    def robotRotate(self, angle, moveConfig2):
        if abs(angle) > math.pi/2:
            if angle >= 0:
                thetaz1 = angle - math.pi/2
                self.MOTION.setMoveArmsEnabled(False, False)
                self.MOTION.moveTo(0.0,0.0,math.pi/2,moveConfig2)
                time.sleep(1)
                self.MOTION.setMoveArmsEnabled(False, False)
                self.MOTION.moveTo(0.0,0.0,thetaz1,moveConfig2)
            else:
                thetaz1 = angle + math.pi/2
                self.MOTION.setMoveArmsEnabled(False, False)
                self.MOTION.moveTo(0.0,0.0,-math.pi/2,moveConfig2)
                time.sleep(1)
                self.MOTION.setMoveArmsEnabled(False, False)
                self.MOTION.moveTo(0.0,0.0,thetaz1,moveConfig2)
        else:
            self.MOTION.setMoveArmsEnabled(False, False)
            self.MOTION.moveTo(0.0,0.0,angle,moveConfig2)


    def threePointsAndOneLine(self, dictBallX, dictBallY, compensationAngle, redBallInfo, stickInfo, moveConfig):
        theta, x, y = self.calculation(redBallInfo, stickInfo)
        self.robotRotate(theta, moveConfig)
        time.sleep(0.5)
        self.MOTION.moveTo(x + dictBallX, 0.0, compensationAngle, moveConfig)
        time.sleep(0.5)
        self.MOTION.moveTo(0.0, y + dictBallY, compensationAngle, moveConfig)
        self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
        return theta




if __name__ == '__main__':
    '''robotIP = '169.254.199.32'
    red = AllDistance(robotIP)
    circle = red.redballdispose(110, 86, 4, 166, 0)
    print circlez
    red.allDistance(circle, 0.02, 0)
    print red.ballPosition'''
    #84 95 4 166






