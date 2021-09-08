# -*- coding: utf-8 -*-
# @Time    : 2021/7/13 3:53
# @Author  : Baokang_Xie
# @FileName: Detection_class_test.py
# @Software: PyCharm

import math, time, cv2, numpy
from naoqi import ALProxy, ALModule

cv_version = cv2.__version__.split(".")[0]
if cv_version == "2":  # for OpenCV 2
    import cv2.cv as cv

# --------------------全局变量------------------------

naoMarkDiameter = 0.0913


class BasicNao(object):

    def __init__(self, IP):
        '''
        实例化各项机器人代理类
        :param IP:
        '''
        self.IP = IP
        self.PORT = 9559
        self.MEMORY = ALProxy("ALMemory", self.IP, self.PORT)
        self.MOTION = ALProxy("ALMotion", self.IP, self.PORT)
        self.CAMERA = ALProxy("ALVideoDevice", self.IP, self.PORT)
        self.TTS = ALProxy("ALTextToSpeech", self.IP, self.PORT)
        self.LANDMARK = ALProxy("ALLandMarkDetection", self.IP, self.PORT)


class BasicVison(BasicNao):
    """
    机器人视觉基础类
    包括：1.机器人视觉获取 2.输出画面各参数 3.显示机器人摄像头画面
    """

    def __init__(self, IP):
        super(BasicVison, self).__init__(IP)
        # 运行BasicNao基类构造函数

        self.resolution = 2
        self.colorSpace = 13
        self.fps = 20
        # 设置摄像头资源参数
        self.bottomCameraDirection = [1.2, 39.7]  # 顶部摄像头中心光轴与水平线的偏角，第二是底部摄像头
        self.cameraPitchRange = 47.64 / 180 * numpy.pi  # 上下摄像头竖直张角
        self.cameraYawRange = 60.97 / 180 * numpy.pi  # 上下摄像头水平张角
        self.frameChannels = 0.0
        self.frameHeight = 0.0
        self.frameWidth = 0.0

    def updateFrame(self, cameraID):
        '''
        订阅摄像头，获取画面
        :param cameraID:机器人摄像头ID
        :return:无
        '''
        self.CAMERA.setActiveCamera(cameraID)
        self.videoClient = self.CAMERA.subscribe("python_client", self.resolution, self.colorSpace, self.fps)
        naoImage = self.CAMERA.getImageRemote(self.videoClient)
        self.CAMERA.unsubscribe(self.videoClient)
        try:
            self.frameChannels = naoImage[2]  # 画面通道
            self.frameHeight = naoImage[1]  # 画面宽度
            self.frameWidth = naoImage[0]  # 画面宽度
            self.frameArray = numpy.frombuffer(naoImage[6], dtype=numpy.uint8).reshape(
                [naoImage[1], naoImage[0], naoImage[2]])
            # frombuffer将data以流的形式读入转化成ndarray对象
            # 第一参数为stream,第二参数为返回值的数据类型
        except IndexError:
            print 'There is error in updateFrame()!'

    def printFrameData(self):
        '''
        输出画面各参数
        :return:
        '''
        print("frame height = ", self.frameHeight)
        print("frame width = ", self.frameWidth)
        print("frame channels = ", self.frameChannels)
        print("frame shape = ", self.frameArray.shape)

    def showFrame(self):
        '''
        显示机器人摄像头画面
        :return:
        '''
        if self.frameArray is None:
            print 'please get an image from Nao with the method updateFrame()!'
        else:
            cv2.imshow('original_frame', self.frameArray)


class AllDistance(BasicVison):
    def __init__(self, IP):
        super(AllDistance, self).__init__(IP)
        # self.kernel = numpy.ones((5, 5), numpy.uint8)
        self.minPerimeter = self.frameHeight / 8.0  # 能识别的黄杆的最小周长（画面高度的1/8）
        self.minArea = self.frameHeight * self.frameWidth / 1000.0  # 能被识别黄杆的最小面积（画面面积的1/1000）
        self.kernelErosion = numpy.ones((5, 5), numpy.uint8)
        self.kernelDilation = numpy.ones((5, 5), numpy.uint8)

    def redballdispose(self, S1, V1, H1, H2, cameraID):
        '''
        红球画面预处理函数
        色调（H），饱和度（S），明度（V）
        :param S1:使用setHSV.py进行S1, V1, H1, H2四个值的测定
        :param V1:
        :param H1:
        :param H2:
        :param cameraID:摄像头ID
        :return:处理后的图像矩阵
        '''
        minHSV1 = numpy.array([0, S1, V1])
        maxHSV1 = numpy.array([H1, 255, 255])
        minHSV2 = numpy.array([H2, S1, V1])
        maxHSV2 = numpy.array([180, 255, 255])
        # 二值化范围，需要使用setHSV.py进行S1, V1, H1, H2四个值的测定
        self.updateFrame(cameraID)
        try:
            imgHSV = cv2.cvtColor(self.frameArray, cv2.COLOR_BGR2HSV)  # 转化为HSV色彩空间
        except:
            print 'no image!'
        else:
            frameBin1 = cv2.inRange(imgHSV, minHSV1, maxHSV1)  # 二值化1（低于minHSV1，高于maxHSV1的色彩值全部转化白色，中间设置为黑色）
            frameBin2 = cv2.inRange(imgHSV, minHSV2, maxHSV2)  # 二值化2
            frameBin = numpy.maximum(frameBin1, frameBin2)
            # opening = cv2.morphologyEx(frameBin, cv2.MORPH_OPEN, self.kernel)
            frameBin = cv2.GaussianBlur(frameBin, (9, 9), 1.5)  # 高斯滤波（高斯模糊），消除图像中的部分噪音，参数需要手动设置
        minDist = int(self.frameHeight / 20.0)  # 霍夫圆检测出的两个相近圆心的距离的最小值
        minRadius = 5  # 霍夫圆检测出的圆半径最小值
        maxRadius = int(self.frameHeight / 12)  # 霍夫圆检测出的圆半径最小值
        cv_version = cv2.__version__.split(".")[0]
        if cv_version >= "3":  # for OpenCV >= 3.0.0
            gradient_name = cv2.HOUGH_GRADIENT
        else:
            gradient_name = cv.CV_HOUGH_GRADIENT
        circles = cv2.HoughCircles(numpy.uint8(frameBin), gradient_name, 1, minDist,
                                   param1=150, param2=15, minRadius=minRadius,
                                   maxRadius=maxRadius)  # 霍夫圆检测，param2：阈值越小检测的圆越多
        # 霍夫圆检测返回的是一个包括圆心在图像中的坐标和半径的numpy数组
        # cv2.imshow('sss', frameBin)
        # cv2.waitKey(0)
        if circles is None:
            circles = numpy.uint16([])  # 未检测到圆，讲其设为空表
        else:
            circles = numpy.uint16(numpy.around(circles[0,]))  # 否则将其转化为numpy.uint16的数组
        if circles.shape[0] == 0:
            return circles
        rRatioMin = 1.0
        circleSelected = numpy.uint16([])
        for circle in circles:  # 遍历每一个圆
            centerX = circle[0]
            centerY = circle[1]
            radius = circle[2]
            # 获取圆的坐标和半径
            initX = centerX - 2 * radius
            initY = centerY - 2 * radius
            if initX < 0 or initY < 0 or (initX + 4 * radius) > self.frameWidth or (
                    initY + 4 * radius) > self.frameHeight or radius < 1:
                continue
            # 做距离圆心两倍半径做正方形，判断此举行是否超出画面边界，且检测此圆半径是否小于1，只要满足一项就淘汰此圆
            rectBallArea = self.frameArray[initY:initY + 4 * radius + 1, initX:initX + 4 * radius + 1,
                           :]  # 从图像中截取正方形画面的部分矩阵
            bFlat = numpy.float16(rectBallArea[:, :, 0].flatten())
            gFlat = numpy.float16(rectBallArea[:, :, 1].flatten())
            rFlat = numpy.float16(rectBallArea[:, :, 2].flatten())
            rScore1 = numpy.uint8(rFlat > 1.0 * gFlat)
            rScore2 = numpy.uint8(rFlat > 1.0 * bFlat)
            rScore = float(numpy.sum(rScore1 * rScore2))
            gScore = float(numpy.sum(numpy.uint8(gFlat > 1.0 * rFlat)))
            rRatio = rScore / len(rFlat)
            gRatio = gScore / len(gFlat)
            # 检测正方形中红色在正方形中的占比接近0.19652，是红球的概率就越大
            if rRatio >= 0.12 and gRatio >= 0.1 and abs(rRatio - 0.19625) < abs(rRatioMin - 0.19625):
                circleSelected = circle
        return circleSelected

    def stickdispose(self, minH, minS, minV, maxH, cameraID):
        '''
        黄杆画面预处理函数
        色调（H），饱和度（S），明度（V）
        :param minH: 使用setHSV.py进行minH, minS, minV, maxH四个值的测定
        :param minS:
        :param minV:
        :param maxH:
        :param cameraID: 摄像头ID
        :return: 黄杆底部在图像中的坐标
        注：此函数以及下面的黄杆距离检测函数的精度不高，只用于远距离大致测距，近距使用mark测距
            可使用超声波定位定位可能更加精确
        '''
        minHSV = numpy.array([minH, minS, minV])
        maxHSV = numpy.array([maxH, 255, 255])
        self.updateFrame(cameraID)
        rects = []
        try:
            frameHSV = cv2.cvtColor(self.frameArray, cv2.COLOR_BGR2HSV)
        except ImportError:
            print("There is error in stickdispose()!")
        frameBin = cv2.inRange(frameHSV, minHSV, maxHSV)  # 二值化
        frameBin = cv2.erode(frameBin, self.kernelErosion, iterations=1)  # 图像腐蚀，5*5像素点
        frameBin = cv2.dilate(frameBin, self.kernelDilation, iterations=1)  # 图像膨胀，5*5像素点
        frameBin = cv2.GaussianBlur(frameBin, (9, 9), 0)
        # 高斯滤波
        if cv_version == "2" or cv_version == "4":
            contours, _ = cv2.findContours(frameBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 轮廓检测函数，检测出黄杆的轮廓
        else:
            _, contours, _ = cv2.findContours(frameBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # 判断编译环境opencv的版本
        if len(contours) == 0:
            return rects
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)  # 获得轮廓的周长
            area = cv2.contourArea(contour)  # 获得轮廓的面积
            if perimeter > self.minPerimeter and area > self.minArea:
                x, y, w, h = cv2.boundingRect(contour)  # 获得一个将轮廓图形包围的矩形
                rects.append([x, y, w, h])  # x，y是矩阵左上点的坐标，w，h是矩阵的宽和高
        if len(rects) == 0:
            return rects
        rects = [rect for rect in rects if (1.0 * rect[3] / rect[2]) > 0.8]  # 迭代器过滤部分高/宽<0.8的矩形
        if len(rects) == 0:
            return rects
        rects = numpy.array(rects)
        rect = rects[numpy.argmax(1.0 * (rects[:, -1]) / rects[:, -2]),]  # 获取所有数据的高/宽值最大的那一组数据
        lastrect = numpy.array([rect[0] + rect[2] / 2, rect[1] + rect[3]])  # 计算出矩形底边的中心点坐标
        return lastrect

    def allDistance(self, location, hight, cameraID, dis):
        '''
        距离计算，使用单目测距算法
        :param location: 红球或者黄杆的返回值
        :param hight: 次坐标距离地面的高度，红球为红球半径，黄杆为0
        :param cameraID: 摄像头ID
        :param dis: 距离标记，若为1则使用远距离的补偿，若为0使用近距补偿
        :return: 无
        '''
        self.Position = []  # 第一个距离，第二个角度
        cameraDirection = self.bottomCameraDirection[cameraID]  # 获取摄像头的上下固定仰角，0为上摄像头，1为下摄像头
        if cameraID == 0:
            cameraPosition = self.MOTION.getPosition("CameraTop", 2, True)
        else:
            cameraPosition = self.MOTION.getPosition("CameraBottom", 2, True)
        cameraHeight = cameraPosition[2]  # 获取摄像头高度
        cameraX = cameraPosition[0]  # 获取摄像头位于机器人坐标位置的x值
        cameraY = cameraPosition[1]  # 获取摄像头位于机器人坐标位置的y值
        headPitches = self.MOTION.getAngles("HeadPitch", True)  # 获取头上下仰角headPitches[0]（向上为负）
        headYaws = self.MOTION.getAngles("HeadYaw", True)  # 获取左右角度headYaws[0]（向左为正）
        ballPitch = (location[1] - 240.0) * self.cameraPitchRange / 480.0  # 计算红球在机器人视野中与中心光轴的上下仰角的度数（弧度制）
        ballYaw = (320.0 - location[0]) * self.cameraYawRange / 640.0  # 计算红球在机器人视野中与中心光轴的左右角度（弧度制）
        dPitch = (cameraHeight - hight) / numpy.tan(
            (cameraDirection + 3) / 180 * numpy.pi + headPitches[0] + ballPitch)  # 计算红球到机器人摄像头的水平竖直距离
        dYaw = dPitch / numpy.cos(ballYaw)  # 计算红球到摄像头的水平投影距离
        if not dis:
            # 短距离补偿
            dYaw = -0.0233 * dYaw ** 4 + 0.0833 * dYaw ** 3 - 0.1188 * dYaw ** 2 + 1.0450 * dYaw - 0.0123
        else:
            # 长距离补偿
            dYaw = 0.0186 * dYaw ** 4 - 0.2594 * dYaw ** 3 + 1.2442 * dYaw ** 2 - 1.7217 * dYaw + 1.8826
        # 距离补尝多项式
        ballX = dYaw * numpy.cos(ballYaw + headYaws[0]) + cameraX
        ballY = dYaw * numpy.sin(ballYaw + headYaws[0]) + cameraY
        ballYaw = numpy.arctan2(ballY, ballX)
        # 计算红球相对机器人的水平角度
        self.Position.append(dYaw)
        self.Position.append(ballYaw)


class AllDetection(AllDistance):
    '''
    红球与黄杆（mark）查找策略
    '''

    def __init__(self, IP):
        super(AllDetection, self).__init__(IP)
        self.memvalue1 = "LandmarkDetected"
        self.size = 0
        self.period = 500

    def redBallDetection(self, moveConfig2, S1, V1, H1, H2, cameraID, addAngle):
        '''
        红球查找策略
        :param moveConfig2: 一种合适的步态
        :param S1: 使用setHSV.py测量的S1, V1, H1, H2值
        :param V1:
        :param H1:
        :param H2:
        :param cameraID: 摄像头ID
        :param addAngle: 机器人检测时头部初始的角度，若设置为0则初始角度为向下17度
        :return:位置信息（极坐标）
        '''
        self.MOTION.setMoveArmsEnabled(False, False)
        self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)  # 头部上下仰角回归零度
        self.MOTION.angleInterpolation("HeadPitch", (addAngle + 17) * math.pi / 180.0, 0.5, False)  # 头部上下仰角初始化
        for i in range(3):
            if addAngle > 0:
                if i == 1:
                    self.MOTION.angleInterpolation("HeadPitch", -6 * math.pi / 180.0, 0.5, False)
                elif i == 2:
                    self.MOTION.angleInterpolation("HeadPitch", -6.5 * math.pi / 180.0, 0.5, False)
            # 若初始角度为0，则分两次低头，第一次降低6°，第二次降低6.5°
            else:
                if i == 1:
                    self.MOTION.angleInterpolation("HeadPitch", 6 * math.pi / 180.0, 0.5, False)
                elif i == 2:
                    self.MOTION.angleInterpolation("HeadPitch", 6.5 * math.pi / 180.0, 0.5, False)
            # 若初始角度过大，则分两次抬头，第一次升高6°，第二次升高6.5°
            for j in range(3):
                time.sleep(1)
                if not j:
                    derct = 0
                elif j % 2:
                    derct = 1
                else:
                    derct = -1
                self.MOTION.angleInterpolation("HeadYaw", derct * 45 * math.pi / 180, 0.5, True)
                # 每一次调整头部角度都会进行一次左右45°偏头扫描
                if cameraID == "all":  # 全部摄像头都用
                    circle = self.redballdispose(S1, V1, H1, H2, 0)
                    if len(circle):
                        break
                    # 两个摄像头同时使用，首先使用上面的若上面的找到红球则直接跳出循环
                    circle = self.redballdispose(S1, V1, H1, H2, 1)
                else:  # 只使用顶部或者底部摄像头（左正右负）
                    circle = self.redballdispose(S1, V1, H1, H2, cameraID)
                if len(circle):
                    break
                    # 只是用一个摄像头，找到红球则直接跳出循环
            else:
                continue
            break
            # 跳出两层循环的语句
        if not len(circle):
            return []
        if derct != 0:
            if cameraID != 'all':
                self.allDistance(circle, 0.02, cameraID, 0)
            else:
                cameraid = self.CAMERA.getActiveCamera()
                self.allDistance(circle, 0.02, cameraid, 0)
            # 计算红球位置信息
            self.MOTION.angleInterpolation("HeadPitch", 0, 0.5, True)
            self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
            # 头恢复原始状态
            self.MOTION.moveTo(0, 0, self.Position[1], moveConfig2)  # 机器人进行转体动作对准红球
            print self.Position[0], self.Position[1] * 180.0 / math.pi  # 输出机器人距离红球直线距离，和机器人正对线与红球的角度（距离不精确）
            return self.redBallDetection(moveConfig2, S1, V1, H1, H2, cameraID, addAngle)  # 递归重新识别红球，精确红球与机器人的直线距离
        # 当derct != 0时证明机器人有偏头测距，此时只有机器人转角计算值准确，所以进行机器人转体对准红球，递归再次进行红球检测
        else:
            if cameraID == 'all':
                cameraid = self.CAMERA.getActiveCamera()
                self.allDistance(circle, 0.02, cameraid, 0)  # 计算红球位置信息
                print self.Position[0], self.Position[1] * 180.0 / math.pi  # 输出机器人距离红球直线距离，和机器人正对线与红球的角度
                return self.Position  # 返回位置信息
            self.allDistance(circle, 0.02, cameraID, 0)
            self.MOTION.angleInterpolation("HeadPitch", 0, 0.5, True)
            self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
            # 头恢复原始状态
            print self.Position[0], self.Position[1] * 180.0 / math.pi
            return self.Position  # 返回位置信息

    def naoMarkDetection(self):
        '''
        mark查找策略
        识别mark，使用自带api识别，适用于近距离识别（最后阶段的识别）
        :return: mark的位置信息
        '''
        alpha = 0
        pianlist = [0, -1, -2, 1, 2]
        self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
        self.MOTION.angleInterpolation("HeadPitch", 0, 0.5, True)
        # 头恢复原始状态
        time.sleep(0.5)
        for i in range(2):
            # 两次扫描，都不低头，保存初始角度
            for j in pianlist:
                self.MOTION.angleInterpolation("HeadYaw", j * (45 * math.pi / 180.0), 0.5,
                                               True)  # 分四次偏头分别扫描0°，-45°，-90°，45°，90°
                time.sleep(1.5)
                self.LANDMARK.subscribe("Test_LandMark", self.period, 0.0)
                for i in range(5):
                    val = self.MEMORY.getData(self.memvalue1)
                # print val
                self.LANDMARK.unsubscribe("Test_LandMark")
                # 订阅LANDMARK，识别mark，返回list
                if (val and isinstance(val, list) and len(val) >= 2):  # 判断val是否为空，val是否为list，val是否大于2
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
        # 跳出两层循环
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
        '''
        黄杆查找策略
        :param minH: 使用setHSV.py调节 minH, minS, minV, maxH的值
        :param minS:
        :param minV:
        :param maxH:
        :param dis: 距离标记，若为1则使用远距离的补偿，若为0使用近距补偿
        :return:
        注：适用于远距离查找，精度不高，因为距离远，黄杆没有递归，也就是说只有角度距离比较精确，距离信息误差比较大
            希望使用超声波定位来解决
        '''
        self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)
        self.MOTION.angleInterpolation("HeadPitch", 16 * math.pi / 180.0, 0.5, True)
        # 初始化头部状态，水平为0，垂直为向下16°
        for i in range(3):
            for j in range(3):
                time.sleep(1)
                if not j:
                    derct = 0
                elif j % 2:
                    derct = -1
                else:
                    derct = 1
                self.MOTION.angleInterpolation("HeadYaw", (derct * 45) * math.pi / 180.0, 0.5, True)  # 偏头0°，-45°，45°
                bottommost = self.stickdispose(minH, minS, minV, maxH, 0)  # 黄杆识别函数，使用头顶摄像头
                if len(bottommost):
                    break
            else:
                continue
            break
            # 跳出两层循环
        if not len(bottommost):
            return []
        self.allDistance(bottommost, 0, 0, dis)  # 距离计算，使用dis所对应的补尝试
        print [self.Position[0], self.Position[1]]
        return [self.Position[0], self.Position[1]]  # 第一个距离，第二个角度，极坐标


class OptimizeData(AllDetection):
    '''
    计算机器人应该如何行走的函数
    '''

    def __init__(self, IP):
        super(OptimizeData, self).__init__(IP)

    def redBallReference(self, moveConfig2, S1, V1, H1, H2):
        '''
        使机器人运动到球的左侧面对红球
        主要在Rmian.py中场地三里面，当找不到黄杆时调用，一直绕着红球转，直到找到黄杆位为止
        :param moveConfig2: 步态参数
        :param S1: 使用setHSV.py进行S1, V1, H1, H2四个值的测定
        :param V1:
        :param H1:
        :param H2:
        :return:无
        '''
        self.MOTION.moveTo(0, 0, 45 * math.pi / 180.0, moveConfig2)
        self.MOTION.moveTo(0.30 / math.cos(45 * math.pi / 180.0), 0, 0, moveConfig2)
        self.robotRotate(-135 * math.pi / 180.0, moveConfig2)  # 调用转体函数，分两步转体
        det, angle = self.redBallDetection(moveConfig2, S1, V1, H1, H2, 1, 5)
        self.MOTION.moveTo(det - 0.3, 0, angle * math.pi / 180.0, moveConfig2)

    def searchRedBall(self, moveConfig2, S1, V1, H1, H2, angle):
        '''
        当找不到红球时，向前走0.5m（向右的5°的补偿偏角），若还未找到，左右转45°再找
        :param moveConfig2:步态参数
        :param S1:使用setHSV.py进行S1, V1, H1, H2四个值的测定
        :param V1:
        :param H1:
        :param H2:
        :param angle:redBallDetection函数所需要上下仰角的初始角度
        :return: 红球位置信息
        注：此效果是累加在红球策略之上的
        '''
        self.MOTION.moveTo(0.5, 0, -5 * math.pi / 180.0, moveConfig2)
        redBallInfo = self.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', angle)
        # 向前走0.5m
        if not len(redBallInfo):
            self.MOTION.moveTo(0, 0, 45 * math.pi / 180.0, moveConfig2)
            redBallInfo = self.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', angle)
        # 左转45°
        if not len(redBallInfo):
            self.MOTION.moveTo(0, 0, -45 * math.pi / 180.0, moveConfig2)
            time.sleep(0.5)
            self.MOTION.moveTo(0, 0, -45 * math.pi / 180.0, moveConfig2)
            redBallInfo = self.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', angle)
        # 右转90°（初始位置的-45°）
        self.MOTION.moveTo(0, 0, 45 * math.pi / 180.0, moveConfig2)
        return redBallInfo

    def calculation(self, redBallInfo, targetInfo):
        '''
        计算三点一线行走路线
        :param redBallInfo: 红球位置信息（距离，角度）
        :param targetInfo: 洞位置信息（距离，角度）
        :return: 偏转成与球洞直线平行，水平移动，垂直移动
        '''
        angleRobotAndBall = redBallInfo[1]  # 角度 人球
        angleRobotAndTarget = targetInfo[1]  # 角度 人洞
        distRobotToBall = redBallInfo[0]  # 距离 人球
        distRobotToTarget = targetInfo[0]  # 距离 人洞

        alpha = abs(angleRobotAndBall - angleRobotAndTarget)
        distBallToTarget2 = distRobotToBall ** 2 + distRobotToTarget ** 2 - 2 * distRobotToBall * distRobotToTarget * math.cos(
            alpha)
        distBallToTarget = math.sqrt(distBallToTarget2)

        theta2 = (distRobotToBall ** 2 + distBallToTarget2 - distRobotToTarget ** 2) / (
                    2 * distRobotToBall * distBallToTarget)
        theta = math.acos(theta2)  # theta ：distRobotToBall 和 distBallToTarget 夹角

        if angleRobotAndBall - angleRobotAndTarget >= 0:
            if theta >= math.pi / 2:
                # angle:锐角，负;    x： 正;   y: 正
                angle = theta - math.pi + angleRobotAndBall
                x = -distRobotToBall * math.cos(theta)
                y = distRobotToBall * math.sin(theta)
            else:
                # angle:钝角, 负;    x: 负;   y: 正
                angle = theta - math.pi + angleRobotAndBall
                x = -distRobotToBall * math.cos(theta)
                y = distRobotToBall * math.sin(theta)
        else:
            if theta >= math.pi / 2:
                # angle: 锐角, 正;  x: 正;   y: 负
                angle = math.pi - theta + angleRobotAndBall
                x = -distRobotToBall * math.cos(theta)
                y = -distRobotToBall * math.sin(theta)
            else:
                # angle: 钝角, 正;  x: 负;   y: 负
                angle = math.pi - theta + angleRobotAndBall
                x = -distRobotToBall * math.cos(theta)
                y = -distRobotToBall * math.sin(theta)
        print "finalx = ", x, "finaly = ", y
        print "finalAngle = ", angle
        return [angle, x, y]

    def robotRotate(self, angle, moveConfig2):
        '''
        机器人旋转函数，如果angle大于45°分两次转，第一次转45°，第二次转剩下的角度
        :param angle: 需要转体的角度
        :param moveConfig2: 步态参数
        :return:无
        '''
        if abs(angle) > math.pi / 2:
            if angle >= 0:
                thetaz1 = angle - math.pi / 2
                self.MOTION.setMoveArmsEnabled(False, False)
                self.MOTION.moveTo(0.0, 0.0, math.pi / 2, moveConfig2)
                time.sleep(1)
                self.MOTION.setMoveArmsEnabled(False, False)
                self.MOTION.moveTo(0.0, 0.0, thetaz1, moveConfig2)
            # 角度大于0°时
            else:
                thetaz1 = angle + math.pi / 2
                self.MOTION.setMoveArmsEnabled(False, False)
                self.MOTION.moveTo(0.0, 0.0, -math.pi / 2, moveConfig2)
                time.sleep(1)
                self.MOTION.setMoveArmsEnabled(False, False)
                self.MOTION.moveTo(0.0, 0.0, thetaz1, moveConfig2)
            # 角度小于0°时
        else:
            self.MOTION.setMoveArmsEnabled(False, False)
            self.MOTION.moveTo(0.0, 0.0, angle, moveConfig2)
        # 角度小于45°

    def threePointsAndOneLine(self, dictBallX, dictBallY, compensationAngle, redBallInfo, stickInfo, moveConfig):
        '''
        三点一线函数，有x，y，angle的补偿
        :param dictBallX:水平补偿距离
        :param dictBallY:垂直补偿距离
        :param compensationAngle:补偿角度
        :param redBallInfo:红球位置信息
        :param stickInfo:黄杆位置信息（mark位置信息）
        :param moveConfig: 步态参数
        :return:需要转多少度才能和球洞直线平行
        '''
        theta, x, y = self.calculation(redBallInfo, stickInfo)  # 计算三点一线行走路线函数得到角度，x，y信息
        self.robotRotate(theta, moveConfig)  # 分两次转体函数
        time.sleep(0.5)
        self.MOTION.moveTo(x + dictBallX, 0.0, compensationAngle, moveConfig)  # 水平移动x
        time.sleep(0.5)
        self.MOTION.moveTo(0.0, y + dictBallY, compensationAngle, moveConfig)  # 垂直移动y
        self.MOTION.angleInterpolation("HeadYaw", 0, 0.5, True)  #
        return theta


if __name__ == '__main__':
    '''robotIP = '169.254.199.32'
    red = AllDistance(robotIP)
    circle = red.redballdispose(110, 86, 4, 166, 0)
    print circlez
    red.allDistance(circle, 0.02, 0)
    print red.ballPosition'''
    # 84 95 4 166
