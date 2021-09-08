import cv2
import naoqi
import publicApi
import numpy as np
import vision_definitions as vd
from naoqi import ALProxy

cv_version = cv2.__version__.split(".")[0]
if cv_version == "2":
    import cv2.cv as cv

    aa = cv2.CV_AA
else:
    aa = cv2.LINE_AA


class setHSV(object):
    def __init__(self, robotIP):
        self.cropKeep = 1
        self.cameraID = 0
        self.resolution = vd.kVGA
        self.colorSpace = vd.kBGRColorSpace
        self.fps = 30
        self.frameArray = None
        self.kernel = np.ones((3, 3), np.uint8)
        self.CAMERA = ALProxy("ALVideoDevice", robotIP, 9559)
        self.MOTION = ALProxy("ALMotion", robotIP, 9559)
        self.bottomCameraDirection = [1.2, 39.7]
        self.cameraPitchRange = 47.64 / 180 * np.pi
        self.cameraYawRange = 60.97 / 180 * np.pi

    def updateFrame(self):
        if self.CAMERA.getActiveCamera() != self.cameraID:
            self.CAMERA.setActiveCamera(self.cameraID)
        videoClient = self.CAMERA.subscribe("python_client", self.resolution, self.colorSpace, self.fps)
        naoImage = self.CAMERA.getImageRemote(videoClient)
        self.CAMERA.releaseImage(videoClient)
        self.CAMERA.unsubscribe(videoClient)
        try:
            self.frameWidth = naoImage[0]
            self.frameHeight = naoImage[1]
            self.frameChannels = naoImage[2]
            self.frameArray = np.frombuffer(naoImage[6], dtype=np.uint8).reshape(
                [naoImage[1], naoImage[0], naoImage[2]])
        except IndexError:
            print("get image failed!")

    def redballSetHSV(self):
        self.CAMERA.setActiveCamera(self.cameraID)

        def __nothing():
            pass

        windowName = "slider for ball detection"
        cv2.namedWindow(windowName)
        cv2.createTrackbar("minS1", windowName, 145, 180, __nothing)
        cv2.createTrackbar("minV1", windowName, 50, 180, __nothing)
        cv2.createTrackbar("maxH1", windowName, 4, 20, __nothing)
        cv2.createTrackbar("minH2", windowName, 166, 190, __nothing)
        while True:
            self.updateFrame()
            minS1 = cv2.getTrackbarPos("minS1", windowName)
            minV1 = cv2.getTrackbarPos("minV1", windowName)
            maxH1 = cv2.getTrackbarPos("maxH1", windowName)
            minH2 = cv2.getTrackbarPos("minH2", windowName)
            minHSV1 = np.array([0, minS1, minV1])
            maxHSV1 = np.array([maxH1, 255, 255])
            minHSV2 = np.array([minH2, minS1, minV1])
            maxHSV2 = np.array([180, 255, 255])
            try:
                imgHSV = cv2.cvtColor(self.frameArray, cv2.COLOR_BGR2HSV)
            except:
                print("no image detected!")
            else:
                frameBin1 = cv2.inRange(imgHSV, minHSV1, maxHSV1)
                frameBin2 = cv2.inRange(imgHSV, minHSV2, maxHSV2)
                frameBin = np.maximum(frameBin1, frameBin2)
                opening = cv2.morphologyEx(frameBin, cv2.MORPH_OPEN, self.kernel)
                # frameBin = cv2.bilateralFilter(frameBin, 10, 200, 200)
                frameBin = cv2.GaussianBlur(frameBin, (9, 9), 1.5)
                circle = self.redBallCalculate(frameBin)
                if len(circle) != 0:
                    self.allDistance(circle, 0.02, self.cameraID)
                    x = int(circle[0])
                    y = int(circle[1])
                    r = int(circle[2])
                    cv2.circle(self.frameArray, (x, y), r, (0, 0, 255), 3)
                    cv2.circle(self.frameArray, (x, y), 3, (255, 255, 0), -1)
                    text = 'x:  ' + str(x) + ' y:  ' + str(y)
                    cv2.putText(self.frameArray, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, aa, 0)
                cv2.imshow('frame', self.frameArray)
                cv2.imshow("bin_frame", frameBin)
                k = cv2.waitKey(10) & 0xFF
                if k == 27:
                    break
        cv2.destroyAllWindows()

    def sticksetHSV(self):
        self.CAMERA.setActiveCamera(self.cameraID)

        def __nothing():
            pass

        windowName = "slider for stick detection"
        cv2.namedWindow(windowName)
        cv2.createTrackbar("minH", windowName, 26, 150, __nothing)
        cv2.createTrackbar("minS", windowName, 43, 180, __nothing)
        cv2.createTrackbar("minV", windowName, 46, 150, __nothing)
        cv2.createTrackbar("maxH", windowName, 34, 100, __nothing)
        while True:
            self.updateFrame()
            minH = cv2.getTrackbarPos("minH", windowName)
            minS = cv2.getTrackbarPos("minS", windowName)
            minV = cv2.getTrackbarPos("minV", windowName)
            maxH = cv2.getTrackbarPos("maxH", windowName)
            minHSV = np.array([minH, minS, minV])
            maxHSV = np.array([maxH, 255, 255])
            try:
                frameArray = self.frameArray[int((1 - self.cropKeep) * self.frameHeight):, :]
            except IndexError:
                print("error happened when crop the image!")
            frameHSV = cv2.cvtColor(frameArray, cv2.COLOR_BGR2HSV)
            frameBin = cv2.inRange(frameHSV, minHSV, maxHSV)
            kernelErosion = np.ones((5, 5), np.uint8)
            kernelDilation = np.ones((5, 5), np.uint8)
            frameBin = cv2.erode(frameBin, kernelErosion, iterations=1)
            frameBin = cv2.dilate(frameBin, kernelDilation, iterations=1)
            frameBin = cv2.GaussianBlur(frameBin, (9, 9), 0)
            rect = self.stickdispose(frameBin)
            if len(rect):
                self.allDistance(rect, 0.0, self.cameraID)
                cv2.circle(self.frameArray, (rect[0], rect[1]), 2, (255, 255, 0), -1)
                text = 'x:  ' + str(rect[0]) + ' y:  ' + str(rect[1])
                print text
                cv2.putText(self.frameArray, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, aa, 0)
            cv2.imshow("stick", self.frameArray)
            cv2.imshow(windowName, frameBin)
            k = cv2.waitKey(10) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()

    def redBallCalculate(self, frame):
        minDist = int(self.frameHeight / 20)
        maxRadius = int(self.frameHeight / 12.3)
        minRadius = 5
        if cv_version >= "3":  # for OpenCV >= 3.0.0
            gradient_name = cv2.HOUGH_GRADIENT
        else:
            gradient_name = cv.CV_HOUGH_GRADIENT
        circles = cv2.HoughCircles(np.uint8(frame), gradient_name, 1, minDist,
                                   param1=150, param2=15, minRadius=minRadius, maxRadius=maxRadius)
        if circles is None:
            # print circles
            circles = np.uint16([])
        else:
            circles = np.uint16(np.around(circles[0,]))
            # print circles
        if circles.shape[0] == 0:
            return circles
        rRatioMin = 1.0
        circleSelected = np.uint16([])
        for circle in circles:
            centerX = circle[0]
            centerY = circle[1]
            radius = circle[2]
            initX = centerX - 2 * radius
            initY = centerY - 2 * radius
            if initX < 0 or initY < 0 or (initX + 4 * radius) > self.frameWidth or (
                    initY + 4 * radius) > self.frameHeight or radius < 1:
                continue
            # print self.frame
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
            if rRatio >= 0.12 and gRatio >= 0.1 and abs(rRatio - 0.19) < abs(rRatioMin - 0.19):
                circleSelected = circle
        return circleSelected

    def stickdispose(self, frame):
        rects = []
        self.minPerimeter = self.frameHeight / 8.0
        self.minArea = self.frameHeight * self.frameWidth / 1000.0
        if cv_version == "2":
            contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else:
            _, contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
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
        rects = np.array(rects)
        rect = rects[np.argmax(1.0 * (rects[:, -1]) / rects[:, -2]),]
        lastrect = np.array([rect[0] + rect[2] / 2, rect[1] + rect[3]])
        return lastrect

    def allDistance(self, location, hight, cameraID):
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
        # print cameraPosition
        headPitches = self.MOTION.getAngles("HeadPitch", True)
        headPitch = headPitches[0]
        # print headPitch*180/np.pi
        headYaws = self.MOTION.getAngles("HeadYaw", True)
        headYaw = headYaws[0]
        ballPitch = (centerY - 240.0) * self.cameraPitchRange / 480.0
        # print ballPitch*180/np.pi
        ballYaw = (320.0 - centerX) * self.cameraYawRange / 640.0
        # print ballYaw * 180 / np.pi
        dPitch = (cameraHeight - hight) / np.tan(headPitch + (cameraDirection) * np.pi / 180.0 + ballPitch)
        dYaw = dPitch / np.cos(ballYaw)
        # dYaw = -0.1975*dYaw**4+0.6839*dYaw**3-0.7945*dYaw**2+1.5192*dYaw-0.0322
        ballX = dYaw * np.cos(ballYaw + headYaw) + cameraX
        ballY = dYaw * np.sin(ballYaw + headYaw) + cameraY
        dict = np.sqrt(ballX ** 2 + ballY ** 2)
        self.Position.append(dYaw)
        self.Position.append(ballYaw + headYaw)
        print self.Position


if __name__ == "__main__":
    robotIP = "169.254.2.57"
    # mm = naoqi.ALProxy("ALMotion",robotIP,9559)
    # mm.wakeUp()
    # publicApi.grip(robotIP)
    # publicApi.close_pole(robotIP)
    sethsv = setHSV(robotIP)
    sethsv.sticksetHSV()
    # sethsv.redballSetHSV()
