#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : GolfVision.py
@CreateTime :2021/7/20 11:17 
@Author : 许嘉凯
@Version  : 1.0
@Description : 
"""

import math
import os
import sys
import time

import almath
import cv2
import motion
import numpy as np
import vision_definitions as vd
from naoqi import ALProxy

# sys.path.append("/home/meringue/Softwares/pynaoqi-sdk/") #naoqi directory
sys.path.append("./")

cv_version = cv2.__version__.split(".")[0]
if cv_version == "2":  # for OpenCV 2
    import cv2.cv as cv


class NaoConfig(object):
    """
	当前类属于Nao的配置类,是其他类的基类
	这个基类中主要包含了一些基本配置信息，
	如IP，端口号，并且创建了一些需要用到的NAO库中自带的类的对象（视觉、语音、运动等）。
	定义视觉类的时候，可以直接这个类继承
	"""

    def __init__(self, IP, PORT=9559):
        self._IP = IP
        self._PORT = PORT
        try:
            self.cameraProxy = ALProxy("ALVideoDevice", self._IP, self._PORT)
            self.motionProxy = ALProxy("ALMotion", self._IP, self._PORT)
            self.postureProxy = ALProxy("ALRobotPosture", self._IP, self._PORT)
            self.tts = ALProxy("ALTextToSpeech", self._IP, self._PORT)
            self.memoryProxy = ALProxy("ALMemory", self._IP, self._PORT)
            self.landMarkProxy = ALProxy("ALLandMarkDetection", self._IP, self._PORT)
        except Exception, e:
            print("Error when configuring the NAO!")
            print(str(e))
            exit(1)


class VisualBasis(NaoConfig):
    """
    可视化任务的基本类。
    视觉基类中除了定义了一些默认的摄像头参数，
    还定义了一些
    基本的成员函数:
        从指定摄像头获取一帧图像
        返回当前存储的图像数据
        显示当前图像
        保存当前图像到本地，还有一些以后用到再定义的函数，先预留接口在这里。
    """

    def __init__(self, IP, PORT=9559, cameraId=vd.kBottomCamera, resolution=vd.kVGA):
        """
        由于视觉任务中（红球检测、黄杆检测）都需要共用一些基本功能（如从摄像头获取数据），
        因此再定义一个视觉基类VisualBasis供使用，这个类是从NaoConfig继承出来的。
        """
        super(VisualBasis, self).__init__(IP, PORT)
        self.cameraId = cameraId
        self.cameraName = "CameraBottom" if self.cameraId == vd.kBottomCamera else "CameraTop"
        self.resolution = resolution
        self.colorSpace = vd.kBGRColorSpace
        self.fps = 20
        self.frameHeight = 0
        self.frameWidth = 0
        self.frameChannels = 0
        self.frameArray = None
        # 顶部摄像头中心光轴与水平线的偏角，第二是底部摄像头
        self.bottomCameraDirection = [1.2, 39.7]
        # 摄像头垂直张角
        self.cameraPitchRange = 47.64 / 180 * np.pi
        # 摄像头水平张角
        self.cameraYawRange = 60.97 / 180 * np.pi
        self.cameraProxy.setActiveCamera(self.cameraId)

    def updateFrame(self, client="python_client"):
        """
        从指定的相机获取一个新的图像，并将其保存在self.frame中。

        :param client:
        :return:
        """
        if self.cameraProxy.getActiveCamera() != self.cameraId:
            self.cameraProxy.setActiveCamera(self.cameraId)
            time.sleep(1)

        videoClient = self.cameraProxy.subscribe(client, self.resolution, self.colorSpace, self.fps)
        frame = self.cameraProxy.getImageRemote(videoClient)
        self.cameraProxy.unsubscribe(videoClient)
        try:
            self.frameWidth = frame[0]
            self.frameHeight = frame[1]
            self.frameChannels = frame[2]
            self.frameArray = np.frombuffer(frame[6], dtype=np.uint8).reshape([frame[1], frame[0], frame[2]])
        except IndexError:
            print "get image failed!"
        except TypeError:
            print frame
    def getFrameArray(self):
        """
        得到当前帧

        :return:
        """
        if self.frameArray is None:
            return np.array([])
        return self.frameArray

    def showFrame(self):
        """
        显示当前帧图像。
        """
        if self.frameArray is None:
            print "please get an image from Nao with the method updateFrame()"
        else:
            cv2.imshow("current frame", self.frameArray)

    def printFrameData(self):
        """
        打印当前帧数据。
        """
        print "frame height = ", self.frameHeight
        print "frame width = ", self.frameWidth
        print "frame channels = ", self.frameChannels
        print "frame shape = ", self.frameArray.shape

    def saveFrame(self, framePath):
        """
        当前帧数据保存在指定位置

        :param framePath:
        :return:
        """
        cv2.imwrite(framePath, self.frameArray)
        print "当前帧图像已保存在", framePath

    def setParam(self, paramName=None, paramValue=None):
        raise NotImplementedError

    def setAllParamsToDefault(self):
        raise NotImplementedError


class DetectRedBall(VisualBasis):
    """
    派生自 VisualBasics，用于检测球。
    """

    def setParam(self, paramName=None, paramValue=None):
        raise NotImplementedError

    def setAllParamsToDefault(self):
        raise NotImplementedError

    def __init__(self, IP, PORT=9559, cameraId=vd.kBottomCamera, resolution=vd.kVGA,
                 writeFrame=False):
        """
        初始化各种参数
        需要保存的红球相关的信息有两块：（1）红球在图像中的位置信息；（2）红球相对于机器人坐标系的位置信息。

        :param IP:
        :param PORT:
        :param cameraId:
        :param resolution:
        :param writeFrame:
        """
        super(DetectRedBall, self).__init__(IP, PORT, cameraId, resolution)
        # 图像中的位置信息
        self.ballData = {"centerX": 0, "centerY": 0, "radius": 0}
        # 实际位置信息
        self.ballPosition = {"disX": 0, "disY": 0, "angle": 0}
        self.ballRadius = 0.025
        self.writeFrame = writeFrame

    def __getChannelAndBlur(self, color):
        """
        该函数功能是对图像进行特定通道的分离和滤波，
        分别针对RGB空间和HSV空间都写了预处理函数供调用.

        :param color: 要拆分的颜色通道，仅支持红、绿、蓝三种颜色。
        :return:
        """
        try:
            channelB = self.frameArray[:, :, 0]
            channelG = self.frameArray[:, :, 1]
            channelR = self.frameArray[:, :, 2]
        except:
            print("no image detected!")
        Hm = 6
        if color == "red":
            channelB = channelB * 0.1 * Hm
            channelG = channelG * 0.1 * Hm
            channelR = channelR - channelB - channelG
            channelR = 3 * channelR
            channelR = cv2.GaussianBlur(channelR, (9, 9), 1.5)
            channelR[channelR < 0] = 0
            channelR[channelR > 255] = 255
            return np.uint8(np.round(channelR))
        elif color == "blue":
            channelR = channelR * 0.1 * Hm
            channelG = channelG * 0.1 * Hm
            channelB = channelB - channelG - channelR
            channelB = 3 * channelB
            channelB = cv2.GaussianBlur(channelB, (9, 9), 1.5)
            channelB[channelB < 0] = 0
            channelB[channelB > 255] = 255
            return np.uint8(np.round(channelB))
        elif color == "green":
            channelB = channelB * 0.1 * Hm
            channelR = channelR * 0.1 * Hm
            channelG = channelG - channelB - channelR
            channelG = 3 * channelG
            channelG = cv2.GaussianBlur(channelG, (9, 9), 1.5)
            channelG[channelG < 0] = 0
            channelG[channelG > 255] = 255
            return np.uint8(np.round(channelG))
        else:
            print "这尼玛啥子颜色！"
            print "给老子用RGB 红 绿 蓝!!"
            return None

    def __binImageHSV(self, minHSV1, maxHSV1, minHSV2, maxHSV2):
        """
        从 HSV 图像中获取二值图像（从 BGR 图像转换而来）
        参数 [np.array] 用于红球检测

        :param minHSV1:
        :param maxHSV1:
        :param minHSV2:
        :param maxHSV2:
        :return: 二进制图像。
        """
        try:
            frameArray = self.frameArray.copy()
            imgHSV = cv2.cvtColor(frameArray, cv2.COLOR_BGR2HSV)
        except:
            print "no image detected!"
        else:
            frameBin1 = cv2.inRange(imgHSV, minHSV1, maxHSV1)
            frameBin2 = cv2.inRange(imgHSV, minHSV2, maxHSV2)
            frameBin = np.maximum(frameBin1, frameBin2)
            frameBin = cv2.GaussianBlur(frameBin, (9, 9), 1.5)
            return frameBin

    def __findCircles(self, img, minDist, minRadius, maxRadius):
        """
        从图像中检测圆圈。
        图像预处理后，图像上会分割出红球所在区域和其他的一些噪声。
        理想情况下，红球所在的区域分割结果应该是一个圆（椭圆），直接通过OpenCV库中的霍夫圆检测函数实现

        根据比赛用球的大小要求可以大概限制一下红球在图像中的半径范围（和分辨率有关），代码中的参数是基于640×480的分辨率设置的。
        需要注意的是，经过上述霍夫圆检测到的球可能有多个（可能包含了一些噪声），因此还应该对结果进一步的判断。

        :param img:要检测的图像。
        :param minDist:检测到的圆的中心之间的最小距离。
        :param minRadius:最小圆半径。
        :param maxRadius:最大圆半径。
        :return:一个 uint16 numpy 数组形状的 circleNum3 如果 circleNum>0，([[circleX, circleY,radius]]) 否则返回 None。
        """
        cv_version = cv2.__version__.split(".")[0]
        if cv_version == "3":  # for OpenCV >= 3.0.0
            gradient_name = cv2.HOUGH_GRADIENT
        else:
            gradient_name = cv.CV_HOUGH_GRADIENT
        circles = cv2.HoughCircles(np.uint8(img), gradient_name, 1, minDist, param1=150, param2=15,
                                   minRadius=minRadius, maxRadius=maxRadius)
        if circles is None:
            return np.uint16([])
        else:
            return np.uint16(np.around(circles[0,]))

    def __selectCircle(self, circles):
        """
        从检测到的所有圈子中选择一个列表类型的圈子。
        经过红球识别的结果可能有如下2种情况：

        图像中没有检测到球。
        图像中检测到一个或者多个球。
        第一种情况不需要讨论，只需要返回没有球的信息即可。对于第二种情况，我们需要对每一个检测出的红球进行二次判断。
        因为在比赛现场，NAO机器人最多只应该检测到一个球。因此，针对第二种情况，我给出的筛选方法如下：

        对于每一个检测出的红球，以红球圆心为中心，以红球的4倍半径为边长画一个外围正方形，计算外接正方形区域内红色和绿色像素点所占的比值。

        :param circles:numpy 数组形 (N, 3)， N 是圈数。
        :return:选择圆或无（未选择圆）。
        """
        if circles.shape[0] == 0:
            return circles
        if circles.shape[0] == 1:
            centerX = circles[0][0]
            centerY = circles[0][1]
            radius = circles[0][2]
            initX = centerX - 2 * radius
            initY = centerY - 2 * radius
            if (initX < 0 or initY < 0 or (initX + 4 * radius) > self.frameWidth or
                    (initY + 4 * radius) > self.frameHeight or radius < 1):
                return circles
        channelB = self.frameArray[:, :, 0]
        channelG = self.frameArray[:, :, 1]
        channelR = self.frameArray[:, :, 2]
        rRatioMin = 1.0
        circleSelected = np.uint16([])
        for circle in circles:
            centerX = circle[0]
            centerY = circle[1]
            radius = circle[2]
            initX = centerX - 2 * radius
            initY = centerY - 2 * radius
            if initX < 0 or initY < 0 or (initX + 4 * radius) > self.frameWidth or \
                    (initY + 4 * radius) > self.frameHeight or radius < 1:
                continue
            rectBallArea = self.frameArray[initY:initY + 4 * radius + 1, initX:initX + 4 * radius + 1, :]
            bFlat = np.float16(rectBallArea[:, :, 0].flatten())
            gFlat = np.float16(rectBallArea[:, :, 1].flatten())
            rFlat = np.float16(rectBallArea[:, :, 2].flatten())
            rScore1 = np.uint8(rFlat > 1.0 * gFlat)
            rScore2 = np.uint8(rFlat > 1.0 * bFlat)
            rScore = float(np.sum(rScore1 * rScore2))
            gScore = float(np.sum(np.uint8(gFlat > 1.0 * rFlat)))
            rRatio = rScore / len(rFlat)
            gRatio = gScore / len(gFlat)
            if rRatio >= 0.12 and gRatio >= 0.1 and abs(rRatio - 0.19625) < abs(rRatioMin - 0.19625):
                circleSelected = circle
                rRatioMin = rRatio
        return circleSelected

    def __updateBallPositionFitting(self, standState, cameraID=0):
        """
        计算并更新、补偿的球位置。

        :param standState: “standInit”或“standUp”。
        :return:
        """
        bottomCameraDirection = {"standInit": 49.2, "standUp": 39.7}
        ballRadius = self.ballRadius
        try:
            cameraDirection = bottomCameraDirection[standState]
        except KeyError:
            print "错误！未知的standState，请检查standState的值！"
        else:
            if self.ballData["radius"] == 0:
                self.ballPosition = {"disX": 0, "disY": 0, "angle": 0}
            else:
                centerX = self.ballData["centerX"]
                centerY = self.ballData["centerY"]
                radius = self.ballData["radius"]
                cameraPosition = self.motionProxy.getPosition("CameraBottom", 2, True)
                cameraX = cameraPosition[0]
                cameraY = cameraPosition[1]
                cameraHeight = cameraPosition[2]
                headPitches = self.motionProxy.getAngles("HeadPitch", True)
                headPitch = headPitches[0]
                headYaws = self.motionProxy.getAngles("HeadYaw", True)
                headYaw = headYaws[0]
                ballPitch = (centerY - 240.0) * self.cameraPitchRange / 480.0  # y (pitch angle)
                ballYaw = (320.0 - centerX) * self.cameraYawRange / 640.0  # x (yaw angle)
                dPitch = (cameraHeight - ballRadius) / np.tan(cameraDirection / 180 * np.pi + headPitch + ballPitch)
                dYaw = dPitch / np.cos(ballYaw)
                ballX = dYaw * np.cos(ballYaw + headYaw) + cameraX
                ballY = dYaw * np.sin(ballYaw + headYaw) + cameraY
                ballYaw = np.arctan2(ballY, ballX)
                self.ballPosition["disX"] = ballX
                if standState == "standInit":
                    ky = 42.513 * ballX ** 4 - 109.66 * ballX ** 3 + 104.2 * ballX ** 2 - 44.218 * ballX + 8.5526
                    # ky = 12.604*ballX**4 - 37.962*ballX**3 + 43.163*ballX**2 - 22.688*ballX + 6.0526
                    ballY = ky * ballY
                    ballYaw = np.arctan2(ballY, ballX)
                self.ballPosition["disY"] = ballY
                self.ballPosition["angle"] = ballYaw

    def __updateBallPosition(self, standState):  # 测试阶段
        """
        使用帧中的球数据计算和更新球位置。
        我们通过采集视野中的不同位置信息（采集多次数据取平均），统计各个离散位置的误差信息，最后用多项式对误差进行补偿。
        在测试的时候发现补偿的结果可以把误差缩小到1厘米左右。

        :param standState:
        :return:
        """

        bottomCameraDirection = {"standInit": 49.2 / 180 * np.pi, "standUp": 39.7 / 180 * np.pi}
        try:
            cameraDirection = bottomCameraDirection[standState]
        except KeyError:
            print("Error! unknown standState, please check the value of stand state!")
        else:
            if self.ballData["radius"] == 0:
                self.ballPosition = {"disX": 0, "disY": 0, "angle": 0}
            else:
                centerX = self.ballData["centerX"]
                centerY = self.ballData["centerY"]
                radius = self.ballData["radius"]
                cameraPos = self.motionProxy.getPosition(self.cameraName, motion.FRAME_WORLD, True)
                cameraX, cameraY, cameraHeight = cameraPos[:3]
                headYaw, headPitch = self.motionProxy.getAngles("Head", True)
                cameraPitch = headPitch + cameraDirection
                imgCenterX = self.frameWidth / 2
                imgCenterY = self.frameHeight / 2
                centerX = self.ballData["centerX"]
                centerY = self.ballData["centerY"]
                imgPitch = (centerY - imgCenterY) / self.frameHeight * self.cameraPitchRange
                imgYaw = (imgCenterX - centerX) / self.frameWidth * self.cameraYawRange
                ballPitch = cameraPitch + imgPitch
                # ballPitch = 38/180.0*3.14
                ballYaw = imgYaw + headYaw
                # ballYaw = 31/180.0*3.14
                dist = (cameraHeight - self.ballRadius) / np.tan(ballPitch) + np.sqrt(cameraX ** 2 + cameraY ** 2)
                # print("height = ", cameraHeight)
                # print("cameraPitch = ", cameraPitch*180/3.14)
                # print("imgYaw = ", imgYaw/3.14*180)
                # print("headYaw = ", headYaw/3.14*180)
                # print("ballYaw = ",ballYaw/3.14*180)
                # print("ballPitch = ", ballPitch/3.14*180)
                disX = dist * np.cos(ballYaw)
                disY = dist * np.sin(ballYaw)
                # print("disX = ", disX)
                # print("disY = ", disY)
                self.ballPosition["disX"] = disX
                self.ballPosition["disY"] = disY
                self.ballPosition["angle"] = ballYaw

    def __writeFrame(self, saveDir="./ballData"):
        """
        将当前帧写入特定目录。

        :param saveDir:
        :return:
        """
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
        saveName = str(int(time.time()))
        saveImgPath = os.path.join(saveDir, saveName + ".jpg")
        try:
            cv2.imwrite(saveImgPath, self.frameArray)
        except:
            print("Error when saveing current frame!")

    def updateBallData(self, client="python_client", standState="standInit", color="red",
                       colorSpace="BGR", fitting=False, minS1=134, minV1=50, maxH1=4, minH2=166,
                       cameraID=1, saveFrameBin=False):
        """
        使用从相机获取的帧更新球数据。
        最后要实现上面的所有功能，在类中再定义一个函数，把之前实现的各个模块封装在一起

        :param minS1:
        :param cameraID:
        :param client:
        :param standState: ("standInit", default), "standInit" or "standUp".
        :param color:（“红色”，默认）要检测的球的颜色。
        :param colorSpace: "BGR", "HSV".
        :param fitting:本地化的方法。
        :param saveFrameBin:是否将预处理的帧保存在类中。
        :return:带有球数据的字典。例如：{"centerX":0, "centerY":0, "radius":0} 保存在当前类之中。
        """
        minHSV1 = np.array([0, minS1, minV1])
        maxHSV1 = np.array([maxH1, 255, 255])
        minHSV2 = np.array([minH2, minS1, minV1])
        maxHSV2 = np.array([180, 255, 255])
        self.updateFrame(client)
        minDist = int(self.frameHeight / 20.0)
        # minRadius = 5
        maxRadius = int(self.frameHeight / 12.0)
        if colorSpace == "BGR":
            grayFrame = self.__getChannelAndBlur(color)
        else:
            grayFrame = self.__binImageHSV(minHSV1, maxHSV1, minHSV2, maxHSV2)
        if saveFrameBin:
            self._frameBin = grayFrame.copy()
        # cv2.imshow("bin frame", grayFrame)
        # cv2.imwrite("bin_frame.jpg", grayFrame)
        # cv2.waitKey(20)
        circles = self.__findCircles(grayFrame, minDist, 5, maxRadius)
        circle = self.__selectCircle(circles)
        # print("circle = ", circle.shape)
        if circle.shape[0] == 0:
            # print("no ball")
            self.ballData = {"centerX": 0, "centerY": 0, "radius": 0}
            self.ballPosition = {"disX": 0, "disY": 0, "angle": 0}
        else:
            circle = circle.reshape([-1, 3])
            self.ballData = {"centerX": circle[0][0], "centerY": circle[0][1], "radius": circle[0][2]}
            if fitting:
                self.__updateBallPositionFitting(standState=standState)
            else:
                self.__updateBallPosition(standState=standState)

            if self.writeFrame:
                self.__writeFrame()

    def getBallPosition(self):
        """
        get ball position.

        Return:
            distance in x axis, distance in y axis and direction related to Nao.
        """
        disX = self.ballPosition["disX"]
        disY = self.ballPosition["disY"]
        angle = self.ballPosition["angle"]
        return [disX, disY, angle]

    def getBallInfoInImage(self):
        """
        获取图像中的球信息。

        Return:
            a list of centerX, centerY and radius of the red ball.
        """
        centerX = self.ballData["centerX"]
        centerY = self.ballData["centerY"]
        radius = self.ballData["radius"]
        return [centerX, centerY, radius]

    def showBallPosition(self):
        """
        show and save ball data in the current frame.
        """
        if self.ballData["radius"] == 0:
            # print("no ball found.")
            print("ball postion = ", (self.ballPosition["disX"], self.ballPosition["disY"]))
            cv2.imshow("ball position", self.frameArray)
        else:
            # print("ballX = ", self.ballData["centerX"])
            # print("ballY = ", self.ballData["centerY"])
            # print("ball postion = ", (self.ballPosition["disX"], self.ballPosition["disY"]))
            # print("ball direction = ", self.ballPosition["angle"]*180/3.14)
            frameArray = self.frameArray.copy()
            cv2.circle(frameArray, (self.ballData["centerX"], self.ballData["centerY"]),
                       self.ballData["radius"], (250, 150, 150), 2)
            cv2.circle(frameArray, (self.ballData["centerX"], self.ballData["centerY"]),
                       2, (50, 250, 50), 3)
            # print frameArray
            cv2.imshow("ball position", frameArray)

    def sliderHSV(self, client):
        """
        slider for ball detection in HSV color space.

        Args:
            client: client name.
        """

        def __nothing():
            pass

        windowName = "ball detection"
        cv2.namedWindow(windowName)
        cv2.createTrackbar("minS1", windowName, 145, 180, __nothing)
        cv2.createTrackbar("minV1", windowName, 50, 180, __nothing)
        cv2.createTrackbar("maxH1", windowName, 4, 20, __nothing)
        cv2.createTrackbar("minH2", windowName, 166, 190, __nothing)
        while 1:
            self.updateFrame(client)
            minS1 = cv2.getTrackbarPos("minS1", windowName)
            minV1 = cv2.getTrackbarPos("minV1", windowName)
            maxH1 = cv2.getTrackbarPos("maxH1", windowName)
            minH2 = cv2.getTrackbarPos("minH2", windowName)
            minHSV1 = np.array([0, minS1, minV1])
            maxHSV1 = np.array([maxH1, 255, 255])
            minHSV2 = np.array([minH2, minS1, minV1])
            maxHSV2 = np.array([180, 255, 255])
            self.updateBallData(client, colorSpace="HSV", fitting=True, minS1=minS1, minV1=minV1, maxH1=maxH1,
                                minH2=minH2, saveFrameBin=True)
            print self.ballPosition
            cv2.imshow(windowName, self._frameBin)
            self.showBallPosition()
            k = cv2.waitKey(10) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()


class StickDetect(VisualBasis):
    """
    自 VisualBasics，用于检测黄杆。
    """

    def setParam(self, paramName=None, paramValue=None):
        pass

    def setAllParamsToDefault(self):
        pass

    def __init__(self, IP, PORT=9559, cameraId=vd.kTopCamera, resolution=vd.kVGA,
                 writeFrame=False):
        super(StickDetect, self).__init__(IP, PORT, cameraId, resolution)
        self.boundRect = []
        self.cropKeep = 1
        self.stickAngle = 0.0  # 弧度制
        self.writeFrame = writeFrame

    def __preprocess(self, minHSV, maxHSV, cropKeep, morphology):
        """
        预处理当前帧以进行杆检测。（二值化、裁剪等）

        Args:
            minHSV: the lower limit for binalization.
            maxHSV: the upper limit for binalization.
            cropKeep: crop ratio (>=0.5).
            morphology: erosion and dilation.
        Return:
            preprocessed image for stick detection.
        """
        self.cropKeep = cropKeep
        frameArray = self.frameArray
        height = self.frameHeight
        width = self.frameWidth
        try:
            frameArray = frameArray[int((1 - cropKeep) * height):, :]
        except IndexError:
            print("error happened when crop the image!")
        frameHSV = cv2.cvtColor(frameArray, cv2.COLOR_BGR2HSV)
        frameBin = cv2.inRange(frameHSV, minHSV, maxHSV)
        kernelErosion = np.ones((5, 5), np.uint8)
        kernelDilation = np.ones((5, 5), np.uint8)
        frameBin = cv2.erode(frameBin, kernelErosion, iterations=1)
        frameBin = cv2.dilate(frameBin, kernelDilation, iterations=1)
        frameBin = cv2.GaussianBlur(frameBin, (9, 9), 0)
        # cv2.imshow("stick bin", frameBin)
        # cv2.waitKey(20)
        return frameBin

    def __findStick(self, frameBin, minPerimeter, minArea):
        """
        在预处理的框架中找到黄杆。

        Args:
            frameBin: preprocessed frame.
            minPerimeter: minimum perimeter of detected stick.
            minArea: minimum area of detected stick.
        Return: detected stick marked with rectangle or [].
        """
        rects = []
        if cv2.__version__.split(".")[0] == "3":  # for OpenCV >= 3.0.0
            _, contours, _ = cv2.findContours(frameBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else:
            contours, _ = cv2.findContours(frameBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) == 0:
            return rects
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            area = cv2.contourArea(contour)
            if perimeter > minPerimeter and area > minArea:
                x, y, w, h = cv2.boundingRect(contour)
                rects.append([x, y, w, h])
        if len(rects) == 0:
            return rects
        rects = [rect for rect in rects if (1.0 * rect[3] / rect[2]) > 0.8]
        if len(rects) == 0:
            return rects
        rects = np.array(rects)
        rect = rects[np.argmax(1.0 * (rects[:, -1]) / rects[:, -2]),]
        rect[1] += int(self.frameHeight * (1 - self.cropKeep))
        return rect

    def __writeFrame(self, saveDir="./stickData"):
        """
        write current frame to specifid directory.
        """
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
        saveName = str(int(time.time()))
        saveImgPath = os.path.join(saveDir, saveName + ".jpg")
        try:
            cv2.imwrite(saveImgPath, self.frameArray)
        except:
            print("Error when saveing current frame!")

    def updateStickData(self, client="test", minH=27, minS=55, minV=115,
                        maxH=45, cropKeep=0.75,
                        morphology=True, savePreprocessImg=False):
        """
        更新来自指定相机的黄杆数据。

        :param client: client name
        :param minH:
        :param minS:
        :param minV:
        :param maxH:
        :param cropKeep:修剪比例(> = 0.5)
        :param morphology:(True, default) 腐蚀 and 膨胀
        :param savePreprocessImg:保存不保存预处理的图像
        :return:
        """
        minHSV = np.array([minH, minS, minV])
        maxHSV = np.array([maxH, 255, 255])
        self.updateFrame(client)
        minPerimeter = self.frameHeight / 8.0
        minArea = self.frameHeight * self.frameWidth / 1000.0
        frameBin = self.__preprocess(minHSV, maxHSV, cropKeep, morphology)
        if savePreprocessImg:
            self._frameBin = frameBin.copy()
        rect = self.__findStick(frameBin, minPerimeter, minArea)
        if rect == []:
            self.boundRect = []
            self.stickAngle = 0.0
        else:
            self.boundRect = rect
            centerX = rect[0] + rect[2] / 2
            width = self.frameWidth * 1.0
            self.stickAngle = (width / 2 - centerX) / width * self.cameraYawRange
            cameraPosition = self.motionProxy.getPosition("Head", 2, True)
            cameraY = cameraPosition[5]
            self.stickAngle += cameraY
            if self.writeFrame:
                self.__writeFrame()

    def showStickPosition(self):
        """
        显示当前帧中的杆位置。
        """
        if self.boundRect == []:
            # print("no stick detected.")
            cv2.imshow("stick position", self.frameArray)
        else:
            [x, y, w, h] = self.boundRect
            frame = self.frameArray.copy()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imshow("stick position", frame)

    def slider(self, client):
        """
        用于在 HSV 颜色空间中检测棒的滑块。

        Args:
            client: client name.
        """

        def __nothing():
            pass

        windowName = "slider for stick detection"
        cv2.namedWindow(windowName)
        cv2.createTrackbar("minH", windowName, 20, 150, __nothing)
        cv2.createTrackbar("minS", windowName, 30, 180, __nothing)
        cv2.createTrackbar("minV", windowName, 35, 150, __nothing)
        cv2.createTrackbar("maxH", windowName, 30, 100, __nothing)
        while 1:
            self.updateFrame(client)
            minH = cv2.getTrackbarPos("minH", windowName)
            minS = cv2.getTrackbarPos("minS", windowName)
            minV = cv2.getTrackbarPos("minV", windowName)
            maxH = cv2.getTrackbarPos("maxH", windowName)
            minHSV = np.array([minH, minS, minV])
            maxHSV = np.array([maxH, 255, 255])
            self.updateStickData(client, minH=minH, minS=minS, minV=minV, maxH=maxH, cropKeep=1, savePreprocessImg=True)
            cv2.imshow(windowName, self._frameBin)
            self.showStickPosition()
            print self.stickAngle * 180 / math.pi
            k = cv2.waitKey(10) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()


class LandMarkDetect(NaoConfig):
    """
    detect the landMark.
    """

    def __init__(self, IP, PORT=9559, cameraId=vd.kTopCamera, landMarkSize=0.105):
        super(LandMarkDetect, self).__init__(IP, PORT)
        self.cameraId = cameraId
        self.cameraName = "CameraTop" if cameraId == vd.kTopCamera else "CameraBottom"
        self.landMarkSize = landMarkSize
        self.disX = 0
        self.disY = 0
        self.dist = 0
        self.yawAngle = 0
        self.cameraProxy.setActiveCamera(self.cameraId)

    def updateLandMarkData(self, client="landMark"):
        """
        更新地标信息

        Args:
            client: client name
        Return:
            None.
        """
        if self.cameraProxy.getActiveCamera() != self.cameraId:
            self.cameraProxy.setActiveCamera(self.cameraId)
            time.sleep(1)
        self.landMarkProxy.subscribe(client)
        markData = self.memoryProxy.getData("LandmarkDetected")
        self.cameraProxy.unsubscribe(client)
        if markData is None or len(markData) == 0:
            self.disX = 0
            self.disY = 0
            self.dist = 0
            self.yawAngle = 0
        else:
            wzCamera = markData[1][0][0][1]
            wyCamera = markData[1][0][0][2]
            angularSize = markData[1][0][0][3]
            distCameraToLandmark = self.landMarkSize / (2 * math.tan(angularSize / 2))
            transform = self.motionProxy.getTransform(self.cameraName, 2, True)
            transformList = almath.vectorFloat(transform)
            robotToCamera = almath.Transform(transformList)
            cameraToLandmarkRotTrans = almath.Transform_from3DRotation(0, wyCamera, wzCamera)
            cameraToLandmarkTranslationTrans = almath.Transform(distCameraToLandmark, 0, 0)
            robotToLandmark = robotToCamera * \
                              cameraToLandmarkRotTrans * \
                              cameraToLandmarkTranslationTrans
            self.disX = robotToLandmark.r1_c4
            self.disY = robotToLandmark.r2_c4
            self.dist = np.sqrt(self.disX ** 2 + self.disY ** 2)
            self.yawAngle = math.atan2(self.disY, self.disX)

    def getLandMarkData(self):
        """
        获取地标信息。

        Return:
            a list of disX, disY, dis, and yaw angle.
        """
        return [self.disX, self.disY, self.dist, self.yawAngle]

    def showLandMarkData(self):
        """
        show landmark information detected.
        """
        print("disX = ", self.disX)
        print("disY = ", self.disY)
        print("dis = ", self.dist)
        print("yaw angle = ", self.yawAngle * 180.0 / np.pi)


if __name__ == '__main__':
    from BasicData import IP

    PORT = 9559
    # IP = "169.254.67.213"
    # IP = "169.254.143.164"

    visualBasis = VisualBasis(IP, cameraId=vd.kTopCamera, resolution=vd.kVGA)
    ballDetect = DetectRedBall(IP, cameraId=vd.kBottomCamera, resolution=vd.kVGA, writeFrame=True)
    stickDetect = StickDetect(IP, cameraId=vd.kTopCamera, resolution=vd.kVGA, writeFrame=True)
    landMarkDetect = LandMarkDetect(IP)
    motionProxy = ALProxy("ALMotion", IP, PORT)

    # test code
    # """
    # visualBasis.updateFrame()
    # visualBasis.showFrame()
    # visualBasis.printFrameData()
    # cv2.waitKey(1000)
    #

    # posture initialization
    # motionProxy = ALProxy("ALMotion", IP, 9559)
    # postureProxy = ALProxy("ALRobotPosture", IP, 9559)
    # motionProxy.wakeUp()
    # postureProxy.goToPosture("StandInit", 0.5)

    # visualBasis.motionProxy.wakeUp()
    # visualBasis.postureProxy.goToPosture("StandInit", 0.5)

    motionProxy.wakeUp()
    import publicApi
    publicApi.close_pole()
    # motionProxy.angleInterpolationWithSpeed("HeadPitch", 0.5, 0.5)
    stickDetect.slider("qwe")
    # ballDetect.sliderHSV("wer")
    #

    # while True:
    #     landMarkDetect.updateLandMarkData("123")
    #     print landMarkDetect.getLandMarkData()
    # # while 1:
    # #     time1 = time.time()
    #     ballDetect.updateBallData(client="mm2", colorSpace="HSV", fitting=True, minS1=159, minV1=79, maxH1=2, minH2=172)
    # #     # print(ballDetect.getBallInfoInImage())
    # #     time2 = time.time()
    # #     # print("update data time = ", time2-time1)
    # #     print ballDetect.ballData
    #     print ballDetect.ballPosition
    #
    # # while 1:
    # #     time1 = time.time()
    #     stickDetect.updateStickData(client="str1",minH=5,minS=60,minV=48,maxH=42,cropKeep=0.45)
    # #     # print(ballDetect.getBallInfoInImage())
    # #     time2 = time.time()
    # #     # print("update data time = ", time2-time1)
    #     print stickDetect.stickAngle*180/math.pi

    # while 1:
    #     stickDetect.updateStickData(client="xxx")
    #     stickDetect.showStickPosition()

    # """
    # while 1:
    # 	landMarkDetect.updateLandMarkData(client="xxx")
    # 	landMarkDetect.showLandMarkData()
    # 	time.sleep(1)
    # """
    #
    # """
    # print "start collecting..."
    # for i in range(10):
    # 	imgName = "stick_" + str(i+127) + ".jpg"
    # 	imgDir = os.path.join("stick_images", imgName)
    # 	visualBasis.updateFrame()
    # 	visualBasis.showFrame(timeMs=1000)
    # 	visualBasis.saveFrame(imgDir)
    # 	print "saved in ", imgDir
    # 	time.sleep(5)
    # """
    #
    # """
    # visualBasis._tts.say("hello world")
    # """
    #
    # """
    # visualBasis._motionProxy.wakeUp()
    # """
    #
    # """
    # dataList = visualBasis._memoryProxy.getDataList("camera")
    # print dataList
    # """
    #
    # """
    # visualBasis._motionProxy.setStiffnesses("Body", 1.0)
    # visualBasis._motionProxy.moveInit()
    # """
    #
    # # motionProxy = ALProxy("ALMotion", IP, 9559)
    # # postureProxy = ALProxy("ALRobotPosture", IP, 9559)
    #
    # # motionProxy.wakeUp()
    # # postureProxy.goToPosture("StandInit", 0.5)
    #
    # # motionProxy.wakeUp()
    # # motionProxy.goToPosture("StandInit", 0.5)
    # # motionProxy.moveToward(0.1, 0.1, 0, [["Frequency", 1.0]])
    # # motionProxy.moveTo(0.3, 0.2, 0)
    # """
    # """
