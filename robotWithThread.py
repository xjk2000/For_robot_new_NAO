#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : robotWithThread.py
@CreateTime :2021/9/8 19:57 
@Author : 许嘉凯
@Version  : 1.0
@Description : 
"""
import math
import threading
import time

import BasicData as Bd
import GolfVision
from BasicData import IP
from BasicData import motionProxy, memoryProxy, ttsProxy
from publicApi import grip, close_pole, func_angle

ballDetect = GolfVision.DetectRedBall(IP, resolution=Bd.kVGA, writeFrame=False)
stickDetect = GolfVision.StickDetect(IP, resolution=Bd.kVGA, writeFrame=False)
landMarkDetect = GolfVision.LandMarkDetect(IP)

redBallHSV = [132, 50, 13, 96]
yellowStickHSV = [6, 61, 44, 40]


class GetBallInfoThread(threading.Thread):
    def __init__(self, name="GetBallInfoThread"):
        threading.Thread.__init__(self, name=name)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()

    def run(self):
        while True:
            global ballDetect
            global redBallHSV
            lock.acquire()
            visualBasis = GolfVision.VisualBasis(IP, cameraId=Bd.kBottomCamera, resolution=Bd.kVGA)
            ballDetect = GolfVision.DetectRedBall(IP, resolution=Bd.kVGA, writeFrame=False)
            ballDetect.updateBallData(client="python_redBall_001", colorSpace="HSV", fitting=True, minS1=redBallHSV[0],
                                      minV1=redBallHSV[1],
                                      maxH1=redBallHSV[2],
                                      minH2=redBallHSV[3])
            # 使当前线程将数据刷回到全局变量中并让cpu有时间切换线程
            lock.release()


class GetStickInfoThreadTop(threading.Thread):
    def __init__(self, name="GetBallInfoThread"):
        threading.Thread.__init__(self, name=name)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()

    def run(self):
        while True:
            global stickDetect
            global yellowStickHSV

            lock1.acquire()
            visualBasis = GolfVision.VisualBasis(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA)
            stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA,
                                                 writeFrame=False)
            stickDetect.updateStickData("python_stick_001", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                        minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                        cropKeep=0.75, savePreprocessImg=False)
            # 使当前线程将数据刷回到全局变量中并让cpu有时间切换线程

            lock1.release()


class GetStickInfoThreadMark(threading.Thread):
    def __init__(self, name="GetBallInfoThread"):
        threading.Thread.__init__(self, name=name)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()

    def run(self):
        while True:
            global landMarkDetect
            lock1.acquire()
            visualBasis = GolfVision.VisualBasis(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA)
            landMarkDetect = GolfVision.LandMarkDetect(IP)
            landMarkDetect.updateLandMarkData("python_landmark_001")
            lock1.release()


def printData():
    while True:
        time.sleep(1)
        global ballDetect
        print "==============================="
        print ballDetect.ballPosition


def findBallData(searchTime=2):
    searchRange = -60 * searchTime
    search = searchRange
    while search <= -searchRange:
        motionProxy.angleInterpolationWithSpeed("HeadYaw", func_angle(search), 0.8)
        time.sleep(1)
        global ballDetect
        lock.acquire()
        findBallInfo = ballDetect.ballPosition
        if findBallInfo['disX'] != 0 or findBallInfo['disY'] != 0:
            motionProxy.angleInterpolationWithSpeed('HeadYaw', 0, 0.5)
            print "findBallInfo", findBallInfo
            print func_angle(search)
            motionProxy.moveTo(0, findBallInfo["disY"] / 1.5, 0, Bd.swingConfig)
            print ballDetect.ballPosition
            lock.release()
            return func_angle(search)
        else:
            search += 60
            print "no"
            lock.release()

    motionProxy.angleInterpolationWithSpeed('HeadYaw', 0, 0.5)
    print "no Red Ball"
    motionProxy.moveTo(0.3, 0, 0, Bd.advanceConfig)
    return findBallData(2)


def findBallData2(searchTime=2):
    """
    当 球 和机器人横向距离过远时

    :param searchTime:
    :return:
    """
    searchRange = -60 * searchTime
    search = searchRange
    while search <= -searchRange:
        motionProxy.angleInterpolationWithSpeed("HeadYaw", func_angle(search), 0.8)
        time.sleep(1)
        global ballDetect
        lock.acquire()
        findBallInfo = ballDetect.ballPosition
        if findBallInfo['disX'] != 0 or findBallInfo['disY'] != 0:
            motionProxy.angleInterpolationWithSpeed('HeadYaw', 0, 0.5)
            print "findBallInfo", findBallInfo
            print func_angle(search)
            motionProxy.moveTo(findBallInfo["disX"]/2, findBallInfo["disY"], 0, Bd.swingConfig)
            print ballDetect.ballPosition
            lock.release()
            return func_angle(search)
        else:
            search += 60
            print "no"
            lock.release()

    motionProxy.angleInterpolationWithSpeed('HeadYaw', 0, 0.5)
    print "no Red Ball"
    motionProxy.moveTo(0.3, 0, 0, Bd.advanceConfig)
    return findBallData(2)


def findStick1Data():
    searchRange = 60
    search = searchRange
    while search >= 0:
        motionProxy.angleInterpolationWithSpeed("HeadYaw", func_angle(search), 0.8)
        time.sleep(1)
        global stickDetect
        stick_Detect = stickDetect
        print "stick", stick_Detect.stickAngle
        if stick_Detect.stickAngle != 0:
            motionProxy.angleInterpolationWithSpeed('HeadYaw', 0.1, 0.5)
            return [func_angle(search), stick_Detect.stickAngle]
        else:
            search -= 60
    motionProxy.angleInterpolationWithSpeed('HeadYaw', 0.1, 0.5)
    print "no stick"
    return []


def findStickData(times=2):
    searchRange = 60 * times
    search = searchRange
    while search >= 0:
        motionProxy.angleInterpolationWithSpeed("HeadYaw", func_angle(search), 0.8)
        time.sleep(1)
        global stickDetect
        stick_Detect = stickDetect
        print "stick", stick_Detect.stickAngle
        if stick_Detect.stickAngle != 0:
            motionProxy.angleInterpolationWithSpeed('HeadYaw', 0.1, 0.5)
            return [func_angle(search), stick_Detect.stickAngle]
        else:
            search -= 60
    motionProxy.angleInterpolationWithSpeed('HeadYaw', 0.1, 0.5)
    print "no stick"
    return []


def field_1_1():
    global ballDetect
    print "ball", ballDetect.ballPosition
    time.sleep(1)
    if ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0 and ballDetect.ballPosition[
        "angle"] == 0:
        findBallData(1)
    else:
        motionProxy.moveTo(0, ballDetect.ballPosition["disY"] / 1.5, 0, Bd.swingConfig)
    print "ball", ballDetect.ballPosition
    motionProxy.moveTo(ballDetect.ballPosition["disX"] - 0.1, ballDetect.ballPosition["disY"], 0, Bd.advanceConfig)
    motionProxy.moveTo(0, func_angle(-90), 0, Bd.rotationConfig)
    motionProxy.moveTo(-0.3, 0, 0, Bd.backConfig)
    motionProxy.moveTo(0, 0.4, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    print "----------"
    time.sleep(0.5)
    print "ball ", ballDetect.ballPosition
    while ballDetect.ballPosition["disY"] == 0 and ballDetect.ballPosition["disX"] == 0:
        motionProxy.moveTo(-0.05, 0, 0, Bd.backSlightlyConfig)
        time.sleep(0.5)
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        print "ball Y", ballDetect.ballPosition["disY"]
        if ballDetect.ballPosition["disY"] == 0:
            motionProxy.moveTo(-0.05, 0, 0, Bd.backSlightlyConfig)
            time.sleep(0.5)
        else:
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
            time.sleep(0.5)
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        print "ball X", ballDetect.ballPosition["disX"]
        if ballDetect.ballPosition["disX"] == 0:
            motionProxy.moveTo(-0.05, 0, 0, Bd.backSlightlyConfig)
            time.sleep(0.5)
        else:
            if ballDetect.ballPosition["disX"] < 0.1:
                motionProxy.moveTo(-0.02, 0, 0, Bd.backSlightlyConfig)
                time.sleep(0.5)
            else:
                motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
                time.sleep(0.5)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_1_2():
    motionProxy.moveTo(0, func_angle(90), 0, Bd.rotationConfig)
    motionProxy.moveTo(0.5, 0, 0, Bd.advanceConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.1, 0.5)


def field_1_3():
    global stickDetect
    print "sti", stickDetect.stickAngle
    if stickDetect.stickAngle == 0:
        motionProxy.moveTo(0.5, 0, 0, Bd.advanceConfig)
    else:
        motionProxy.moveTo(0.5, 0, stickDetect.stickAngle, Bd.advanceConfig)


def field_2_1():
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.4, 0.5)
    global ballDetect
    time.sleep(1)
    print "ball", ballDetect.ballPosition
    if ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0 and ballDetect.ballPosition[
        "angle"] == 0:
        motionProxy.moveTo(0.2, 0, 0, Bd.advanceConfig)
    else:
        motionProxy.moveTo(ballDetect.ballPosition["disX"] - 0.1, ballDetect.ballPosition["disY"], 0, Bd.advanceConfig)
    motionProxy.moveTo(0, 0, func_angle(-90), Bd.rotationConfig)
    motionProxy.moveTo(-0.3, 0, 0, Bd.backConfig)
    motionProxy.moveTo(0, 0.3, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    time.sleep(0.3)
    print "ball", ballDetect.ballPosition
    while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
        motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        print "disY", ballDetect.ballPosition["disY"]
        if ballDetect.ballPosition["disY"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        print "disX", ballDetect.ballPosition["disX"]
        if ballDetect.ballPosition["disX"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        elif ballDetect.ballPosition["disX"] < 0.1:
            motionProxy.moveTo(0.02, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_2_2():
    motionProxy.moveTo(0, 0.3, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    global ballDetect
    time.sleep(0.3)
    print "ball", ballDetect.ballPosition
    while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
        motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        print "disY", ballDetect.ballPosition["disY"]
        if ballDetect.ballPosition["disY"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        print "disX", ballDetect.ballPosition["disX"]
        if ballDetect.ballPosition["disX"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        elif ballDetect.ballPosition["disX"] < 0.1:
            motionProxy.moveTo(0.02, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_2_3():
    motionProxy.moveTo(-0.5, 0, 0, Bd.backConfig)
    motionProxy.moveTo(0, 0, func_angle(90), Bd.rotationConfig)
    motionProxy.moveTo(0.6, 0, 0, Bd.advanceConfig)


def field_2_4():
    global stickDetect
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.1, 0.5)
    time.sleep(0.3)
    print "stickAngle", stickDetect.stickAngle
    if stickDetect.stickAngle == 0:
        motionProxy.moveTo(0.5, 0, 0, Bd.advanceConfig)
    else:
        motionProxy.moveTo(0.5, 0, stickDetect.stickAngle, Bd.advanceConfig)


def field_3_1():
    motionProxy.moveTo(0.2, 0, 0, Bd.advanceConfig)
    motionProxy.moveTo(0, 0, func_angle(-30), Bd.rotationConfig)
    motionProxy.moveTo(0, -0.2, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    global ballDetect
    print ballDetect.ballPosition
    time.sleep(0.5)
    while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
        motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        print "disY", ballDetect.ballPosition["disY"]
        if ballDetect.ballPosition["disY"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        print "disX", ballDetect.ballPosition["disX"]
        if ballDetect.ballPosition["disX"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        elif ballDetect.ballPosition["disX"] < 0.1:
            motionProxy.moveTo(0.02, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_3_2():
    motionProxy.moveTo(0,0,func_angle(-60),Bd.rotationConfig)
    motionProxy.moveTo(2,0,0,Bd.advanceConfig)
    motionProxy.moveTo(0,0,func_angle(-90),Bd.rotationConfig)
    global ballDetect
    print ballDetect.ballPosition
    if ballDetect.ballPosition["disX"]==0 and ballDetect.ballPosition["disY"]==0:
        findBallData2(1)
    motionProxy.moveTo(ballDetect.ballPosition["disX"]-0.1,ballDetect.ballPosition["disY"],0,Bd.advanceConfig)
    motionProxy.moveTo(0, 0, func_angle(-90), Bd.rotationConfig)
    motionProxy.moveTo(-0.3, 0, 0, Bd.backConfig)
    motionProxy.moveTo(0, 0.3, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    time.sleep(0.3)
    print "ball", ballDetect.ballPosition
    while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
        motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        print "disY", ballDetect.ballPosition["disY"]
        if ballDetect.ballPosition["disY"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        print "disX", ballDetect.ballPosition["disX"]
        if ballDetect.ballPosition["disX"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        elif ballDetect.ballPosition["disX"] < 0.1:
            motionProxy.moveTo(0.02, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_3_3():
    global stickDetect
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.1, 0.5)
    time.sleep(0.3)
    print "stickAngle", stickDetect.stickAngle
    if stickDetect.stickAngle == 0:
        motionProxy.moveTo(0.5, 0, 0, Bd.advanceConfig)
    else:
        motionProxy.moveTo(0.5, 0, stickDetect.stickAngle, Bd.advanceConfig)


def field_hexagon():
    global ballDetect
    global stickDetect
    global landMarkDetect
    print "ball==>", ballDetect.ballPosition
    print "stick==>", stickDetect.stickAngle
    print "land==>", landMarkDetect.getLandMarkData()
    time.sleep(0.3)
    if ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0 and ballDetect.ballPosition[
        "angle"] == 0:
        findBallData2(2)
    else:
        motionProxy.moveTo(0, ballDetect.ballPosition["disY"] / 1.8, 0, Bd.swingConfig)
    print "ball", ballDetect.ballPosition
    time.sleep(0.3)
    motionProxy.moveTo(ballDetect.ballPosition["disX"] - 0.1, ballDetect.ballPosition["disY"],
                       ballDetect.ballPosition["angle"], Bd.advanceConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.15, 0.5)
    while True:
        time.sleep(0.3)
        while stickDetect.stickAngle == 0:
            motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.05, 0.5)
            time.sleep(0.3)
            while landMarkDetect.getLandMarkData()[2] == 0:
                motionProxy.moveTo(0, 0, func_angle(10), Bd.rotationConfig)
                time.sleep(0.3)
            if math.fabs(landMarkDetect.getLandMarkData()) > 1.5:
                global yellowStickHSV
                lock1.acquire()
                yellowStickHSV = [6, 61, 44, 40]
                lock1.release()
            else:
                global yellowStickHSV
                lock1.acquire()
                yellowStickHSV = [6, 61, 44, 40]
                lock1.release()
        time.sleep(0.3)
        if not -1 < stickDetect.stickAngle < 1 and stickDetect.stickAngle != 0:
            motionProxy.moveTo(0, 0, stickDetect.stickAngle, Bd.rotationSlightlyConfig)
            motionProxy.moveTo(-0.05, 0, 0, Bd.backSlightlyConfig)
            motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
            numberOfTimes = 0
            time.sleep(0.3)
            while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
                if numberOfTimes < 3:
                    motionProxy.moveTo(-0.1, 0, 0, Bd.backConfig)
                else:
                    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.3, 0.5)
                numberOfTimes += 1
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
        else:
            motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
            time.sleep(0.3)
            while not 0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0:
                if ballDetect.ballPosition["disX"] == 0:
                    motionProxy.moveTo(-0.05, 0, 0, Bd.backSlightlyConfig)
                else:
                    if ballDetect.ballPosition["disX"] < 1.0:
                        motionProxy.moveTo(0.02, 0, 0, Bd.advanceSlightlyConfig)
                    else:
                        motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
                time.sleep(0.3)
            motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)
            break


if __name__ == '__main__':
    try:
        while True:
            if not motionProxy.robotIsWakeUp():
                motionProxy.wakeUp()
                motionProxy.setMoveArmsEnabled(False, False)
                grip()
                close_pole()
            else:
                motionProxy.setMoveArmsEnabled(False, False)
                while motionProxy.robotIsWakeUp():
                    # 判断是否进行了头部触摸操作,分别对应场地123
                    if memoryProxy.getData("FrontTactilTouched") == 1:
                        motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)
                        motionProxy.moveTo(0.95, 0.0, func_angle(-20), Bd.advanceConfig)
                        # motionProxy.moveTo(0.2, 0.0,0, Bd.advanceConfig)
                        lock = threading.Lock()
                        lock1 = threading.Lock()
                        ballInfoThread = GetBallInfoThread(name="for-field1")
                        ballInfoThread.start()
                        t1 = threading.Thread(target=field_1_1)
                        t1.start()
                        t1.join()
                        ttsProxy.say("击球")
                        t2 = threading.Thread(target=field_1_2)
                        t2.start()
                        t2.join()
                        stickInfoThread = GetStickInfoThreadTop(name="for-field1-sti")
                        stickInfoThread.start()
                        landMarkThread = GetStickInfoThreadMark(name="for-field1-land")
                        landMarkThread.start()
                        t3 = threading.Thread(target=field_1_3)
                        t3.start()
                        t3.join()
                        while True:
                            t4 = threading.Thread(target=field_hexagon)
                            t4.start()
                            t4.join()
                            ttsProxy.say("前击")

                    if memoryProxy.getData("MiddleTactilTouched") == 1:
                        lock = threading.Lock()
                        lock1 = threading.Lock()
                        ballInfoThread = GetBallInfoThread(name="for-field2")
                        ballInfoThread.start()
                        time.sleep(2)
                        t1 = threading.Thread(target=field_2_1)
                        t1.start()
                        t1.join()
                        ttsProxy.say("轻击")
                        t2 = threading.Thread(target=field_2_2)
                        t2.start()
                        t2.join()
                        ttsProxy.say("击球")
                        t3 = threading.Thread(target=field_2_3)
                        t3.start()
                        t3.join()
                        stickInfoThread = GetStickInfoThreadTop(name="for-field2-sti")
                        stickInfoThread.start()
                        landMarkDetect = GetStickInfoThreadMark(name="for-field2-land")
                        landMarkDetect.start()
                        t4 = threading.Thread(target=field_2_4)
                        t4.start()
                        t4.join()
                        while True:
                            t5 = threading.Thread(target=field_hexagon)
                            t5.start()
                            t5.join()
                            ttsProxy.say("前击")
                    if memoryProxy.getData("RearTactilTouched") == 1:
                        lock = threading.Lock()
                        lock1 = threading.Lock()
                        ballInfoThread = GetBallInfoThread(name="for-field2")
                        ballInfoThread.start()
                        t1=threading.Thread(target=field_3_1)
                        t1.start()
                        t1.join()
                        ttsProxy.say("击球")
                        t2 = threading.Thread(target=field_3_2)
                        t2.start()
                        t2.join()
                        ttsProxy.say("击球")
                        stickInfoThread = GetStickInfoThreadTop(name="for-field2-sti")
                        stickInfoThread.start()
                        landMarkDetect = GetStickInfoThreadMark(name="for-field2-land")
                        landMarkDetect.start()
                        t3 = threading.Thread(target=field_3_3)
                        t3.start()
                        t3.join()
                        while True:
                            t4 = threading.Thread(target=field_hexagon)
                            t4.start()
                            t4.join()
                            ttsProxy.say("前击")









    except:
        print Exception
