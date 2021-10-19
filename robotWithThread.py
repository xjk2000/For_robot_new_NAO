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
import multiprocessing
import time

import BasicData as Bd
import GolfVision
from BasicData import IP
from BasicData import motionProxy, memoryProxy, ttsProxy
from publicApi import grip, close_pole, func_angle

ballDetect = GolfVision.DetectRedBall(IP, cameraId=Bd.kBottomCamera, resolution=Bd.kVGA, writeFrame=False)
landMarkDetect = GolfVision.LandMarkDetect(IP)

redBallHSV = [155, 49, 7, 122]
yellowStickHSV = [8,117,69,42]


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
            lock.acquire()
            try:
                visualBasis = GolfVision.VisualBasis(IP, cameraId=Bd.kBottomCamera, resolution=Bd.kVGA)
                ballDetect = GolfVision.DetectRedBall(IP, resolution=Bd.kVGA, writeFrame=False)
                ballDetect.updateBallData(client=self.name, colorSpace="HSV", fitting=True, minS1=redBallHSV[0],
                                          minV1=redBallHSV[1],
                                          maxH1=redBallHSV[2],
                                          minH2=redBallHSV[3],
                                          saveFrameBin=False)
                print ballDetect.ballPosition
            except:
                print "错误"
            finally:
                lock.release()



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


def findStickData(searchTime=1):
    searchRange=-30*searchTime
    search = searchRange
    while search<=-searchRange:
        motionProxy.angleInterpolationWithSpeed("HeadYaw", func_angle(search), 0.8)
        time.sleep(3)
        stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA, writeFrame=False)

        stickDetect.updateStickData("findStick-python", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                    minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                    cropKeep=0.75, savePreprocessImg=False)
        stick = stickDetect.stickAngle
        if stick !=0:
            motionProxy.angleInterpolationWithSpeed('HeadYaw', 0, 0.5)
            print "stickInfo", stick
            motionProxy.moveTo(0,0,(func_angle(search)+stick)/3,Bd.rotationSlightlyConfig)
            return
        else:
            search+=30


def field_1_1():
    """
    场地一第一部分的
    :return:
    """
    time.sleep(1)
    findBallData(1)
    time.sleep(1)
    global ballDetect
    lock.acquire()
    motionProxy.moveTo(0, ballDetect.ballPosition["disY"] / 1.5, 0, Bd.swingConfig)
    lock.release()
    lock.acquire()
    motionProxy.moveTo(ballDetect.ballPosition["disX"] - 0.1, ballDetect.ballPosition["disY"], 0, Bd.advanceConfig)
    lock.release()
    motionProxy.moveTo(0, 0, func_angle(-90), Bd.rotationConfig)
    motionProxy.moveTo(-0.2, 0, 0, Bd.backConfig)
    motionProxy.moveTo(0, 0.4, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    time.sleep(2)
    lock.acquire()
    if ballDetect.ballPosition["disY"] == 0 and ballDetect.ballPosition["disX"] == 0:
        motionProxy.moveTo(-0.03, 0, 0, Bd.backSlightlyConfig)
    lock.release()
    time.sleep(1)
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        lock.acquire()
        motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
        time.sleep(2)
        lock.release()
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        lock.acquire()
        if ballDetect.ballPosition["disX"] < 0.1:
            motionProxy.moveTo(-0.02, 0, 0, Bd.backSlightlyConfig)
            if not -0.01 < ballDetect.ballPosition["disY"] < 0.01:
                motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
            lock.release()
        else:
            motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
            time.sleep(2)
            lock.release()
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_1_2():
    """
    场地一第二部分 第一杆打完走到横向方形区域
    :return:
    """
    motionProxy.moveTo(0, 0, func_angle(90), Bd.rotationConfig)
    motionProxy.moveTo(0.5, 0, 0, Bd.advanceConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.1, 0.5)


def field_1_3():
    """
    场地一 先判断视野内是否有黄杆, 有则对准黄杆走1.2m至八边形区域内 ,否则直走到八边形区域内
    :return:
    """
    stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA, writeFrame=False)
    stickDetect.updateStickData("field_1_3", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                cropKeep=0.75, savePreprocessImg=False)
    print "sti", stickDetect.stickAngle
    if stickDetect.stickAngle == 0:
        motionProxy.moveTo(1.2, 0, 0, Bd.advanceConfig)
    else:
        motionProxy.moveTo(1.2, 0, stickDetect.stickAngle, Bd.advanceConfig)
    motionProxy.moveTo(0,-0.3,0,Bd.swingConfig)


def field_2_1():
    """
    场地二 第一部分,轻击球,不上坡
    :return:
    """
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.4, 0.5)
    global ballDetect
    time.sleep(1)
    lock.acquire()
    print "ball", ballDetect.ballPosition
    if ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0 and ballDetect.ballPosition[
        "angle"] == 0:
        motionProxy.moveTo(0.2, 0, 0, Bd.advanceConfig)
        lock.release()
    else:
        motionProxy.moveTo(ballDetect.ballPosition["disX"] - 0.1, ballDetect.ballPosition["disY"], 0, Bd.advanceConfig)
        lock.release()
    motionProxy.moveTo(0, 0, func_angle(-90), Bd.rotationConfig)
    motionProxy.moveTo(-0.3, 0, 0, Bd.backConfig)
    motionProxy.moveTo(0, 0.3, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    time.sleep(0.3)
    while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
        lock.acquire()
        print "ball", ballDetect.ballPosition
        motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        lock.release()
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        lock.acquire()
        print "disY", ballDetect.ballPosition["disY"]
        if ballDetect.ballPosition["disY"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
        lock.release()
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        lock.acquire()
        print "disX", ballDetect.ballPosition["disX"]
        if ballDetect.ballPosition["disX"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        elif ballDetect.ballPosition["disX"] < 0.1:
            motionProxy.moveTo(0.02, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
        lock.release()
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_2_2():
    """
    第二部分 重击过坡,球滚至八边形区域内
    :return:
    """
    motionProxy.moveTo(0, 0.3, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    global ballDetect
    time.sleep(0.3)
    while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
        lock.acquire()
        print "ball", ballDetect.ballPosition
        motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        lock.release()
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        lock.acquire()
        print "disY", ballDetect.ballPosition["disY"]
        if ballDetect.ballPosition["disY"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
        lock.release()
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        lock.acquire()
        print "disX", ballDetect.ballPosition["disX"]
        if ballDetect.ballPosition["disX"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        elif ballDetect.ballPosition["disX"] < 0.1:
            motionProxy.moveTo(0.02, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
        lock.release()
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_2_3():
    motionProxy.moveTo(-0.5, 0, 0, Bd.backConfig)
    motionProxy.moveTo(0, 0, func_angle(90), Bd.rotationConfig)
    motionProxy.moveTo(0.6, 0, 0, Bd.advanceConfig)


def field_2_4():
    stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA, writeFrame=False)
    stickDetect.updateStickData("field_2_4", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                cropKeep=0.75, savePreprocessImg=False)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.1, 0.5)
    time.sleep(0.3)
    print "stickAngle", stickDetect.stickAngle
    if stickDetect.stickAngle == 0:
        motionProxy.moveTo(0.5, 0, 0, Bd.advanceConfig)
    else:
        motionProxy.moveTo(0.5, 0, stickDetect.stickAngle, Bd.advanceConfig)


def field_3_1():
    """
    场地三第一部分
    :return:
    """
    motionProxy.moveTo(0.2, 0, 0, Bd.advanceConfig)
    motionProxy.moveTo(0, 0, func_angle(-30), Bd.rotationConfig)
    motionProxy.moveTo(0, -0.2, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    global ballDetect
    time.sleep(0.5)
    while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
        lock.acquire()
        print ballDetect.ballPosition
        motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        lock.release()
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        lock.acquire()
        print "disY", ballDetect.ballPosition["disY"]
        if ballDetect.ballPosition["disY"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
        lock.release()
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        lock.acquire()
        print "disX", ballDetect.ballPosition["disX"]
        if ballDetect.ballPosition["disX"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        elif ballDetect.ballPosition["disX"] < 0.1:
            motionProxy.moveTo(0.02, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
        lock.release()
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_3_2():
    """
    场地三第二部分 打完第一杆之后准备前往打第二杆
    :return:
    """
    motionProxy.moveTo(0, 0, func_angle(-60), Bd.rotationConfig)
    motionProxy.moveTo(2, 0, 0, Bd.advanceConfig)
    motionProxy.moveTo(0, 0, func_angle(-90), Bd.rotationConfig)
    global ballDetect
    if ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
        findBallData(1)
    lock.acquire()
    print ballDetect.ballPosition
    motionProxy.moveTo(ballDetect.ballPosition["disX"] - 0.1, ballDetect.ballPosition["disY"], 0, Bd.advanceConfig)
    lock.release()
    motionProxy.moveTo(0, 0, func_angle(-90), Bd.rotationConfig)
    motionProxy.moveTo(-0.3, 0, 0, Bd.backConfig)
    motionProxy.moveTo(0, 0.3, 0, Bd.swingConfig)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
    time.sleep(0.3)
    while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
        lock.acquire()
        print "ball", ballDetect.ballPosition
        motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        lock.release()
    while not (-0.01 < ballDetect.ballPosition["disY"] < 0.01 and ballDetect.ballPosition["disY"] != 0):
        lock.acquire()
        print "disY", ballDetect.ballPosition["disY"]
        if ballDetect.ballPosition["disY"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0, ballDetect.ballPosition["disY"], 0, Bd.swingSlightlyConfig)
        lock.release()
    while not (0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0):
        lock.acquire()
        print "disX", ballDetect.ballPosition["disX"]
        if ballDetect.ballPosition["disX"] == 0:
            motionProxy.moveTo(0.05, 0, 0, Bd.backSlightlyConfig)
        elif ballDetect.ballPosition["disX"] < 0.1:
            motionProxy.moveTo(0.02, 0, 0, Bd.backSlightlyConfig)
        else:
            motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
        lock.release()
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0, 0.5)


def field_3_3():
    """
    场地三第三部分
    :return:
    """
    stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA, writeFrame=False)
    stickDetect.updateStickData("field_33", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                cropKeep=0.75, savePreprocessImg=False)
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.1, 0.5)
    time.sleep(0.3)
    print "stickAngle", stickDetect.stickAngle
    if stickDetect.stickAngle == 0:
        motionProxy.moveTo(0.5, 0, 0, Bd.advanceConfig)
    else:
        motionProxy.moveTo(0.5, 0, stickDetect.stickAngle, Bd.advanceConfig)


def field_hexagon():
    """
    进入八边形场地之后执行 找球以及对准
    :return:
    """
    global ballDetect
    global yellowStickHSV
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.2, 0.5)
    time.sleep(0.3)
    findBallData(1)
    print "----------------"
    lock.acquire()
    print "ball", ballDetect.ballPosition
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.3, 0.5)
    motionProxy.moveTo(ballDetect.ballPosition["disX"] - 0.1, ballDetect.ballPosition["disY"],
                       ballDetect.ballPosition["angle"], Bd.advanceConfig)
    lock.release()
    motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.15, 0.5)
    while True:
        # time.sleep(0.3)
        # while stickDetect.stickAngle == 0:
        #     motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.05, 0.5)
        #     while landMarkDetect.getLandMarkData()[2] == 0:
        #         print "land",landMarkDetect.getLandMarkData()
        #         motionProxy.moveTo(0, 0, func_angle(10), Bd.rotationConfig)
        #         time.sleep(0.3)
        #     landMarkDetect.updateLandMarkData("python_landmark_001")
        #     print "land",landMarkDetect.getLandMarkData()
        #     if math.fabs(landMarkDetect.getLandMarkData()[2]) > 1.5:
        #         lock1.acquire()
        #         yellowStickHSV = [10, 78, 10, 28]
        #         lock1.release()
        #     else:
        #         lock1.acquire()
        #         yellowStickHSV = [10, 83, 30, 40]
        #         lock1.release()
        time.sleep(0.3)
        stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA, writeFrame=False)
        stickDetect.updateStickData("field_hh", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                    minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                    cropKeep=0.75, savePreprocessImg=False)
        print "stick", stickDetect.stickAngle
        while True:
            # 不适合击球
            print "stick--", stickDetect.stickAngle,"******************"
            RangeTime=0
            stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA, writeFrame=False)
            stickDetect.updateStickData("field_hh", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                        minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                        cropKeep=0.75, savePreprocessImg=False)
            while stickDetect.stickAngle == 0:

                findStickData()
                stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA, writeFrame=False)
                stickDetect.updateStickData("field_hh", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                            minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                            cropKeep=0.75, savePreprocessImg=False)
                print "stick----", stickDetect.stickAngle
                if stickDetect.stickAngle!=0:
                    break
                time.sleep(0.5)
            stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA, writeFrame=False)
            stickDetect.updateStickData("field_hh", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                        minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                        cropKeep=0.75, savePreprocessImg=False)
            motionProxy.moveTo(0, 0, stickDetect.stickAngle, Bd.rotationSlightlyConfig)
            motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
            # numberOfTimes = 0
            # time.sleep(0.3)
            # while ballDetect.ballPosition["disX"] == 0 and ballDetect.ballPosition["disY"] == 0:
            #     print "ball===>", ballDetect.ballPosition
            #     if numberOfTimes < 3:
            #         motionProxy.moveTo(-0.05, 0, 0, Bd.backConfig)
            #     else:
            #         motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.3, 0.5)
            #         motionProxy.moveTo(0.2, 0, 0, Bd.advanceConfig)
            #     numberOfTimes += 1
            lock.acquire()
            motionProxy.moveTo(ballDetect.ballPosition["disX"] - 0.10, ballDetect.ballPosition["disY"], 0,
                               Bd.swingSlightlyConfig)
            lock.release()
            motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.2, 0.5)
            time.sleep(0.5)
            time.sleep(0.3)
            stickDetect = GolfVision.StickDetect(IP, cameraId=Bd.kTopCamera, resolution=Bd.kVGA, writeFrame=False)
            stickDetect.updateStickData("field_hh", minH=yellowStickHSV[0], minS=yellowStickHSV[1],
                                        minV=yellowStickHSV[2], maxH=yellowStickHSV[3],
                                        cropKeep=0.75, savePreprocessImg=False)
            if -0.052360 < stickDetect.stickAngle < 0.052360 and stickDetect.stickAngle != 0:
                break
        # 差不多可以击球了
        motionProxy.angleInterpolationWithSpeed('HeadPitch', 0.5, 0.5)
        time.sleep(0.5)
        while not 0.10 < ballDetect.ballPosition["disX"] < 0.12 and ballDetect.ballPosition["disX"] != 0:
            lock.acquire()
            print "ball==>", ballDetect.ballPosition
            if ballDetect.ballPosition["disX"] == 0:
                motionProxy.moveTo(-0.05, 0, 0, Bd.backSlightlyConfig)
            else:
                if ballDetect.ballPosition["disX"] < 1.0:
                    motionProxy.moveTo(0.02, 0, 0, Bd.advanceSlightlyConfig)
                else:
                    motionProxy.moveTo(0.03, 0, 0, Bd.advanceSlightlyConfig)
            time.sleep(0.3)
            lock.release()
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
                        motionProxy.moveTo(0.90, 0.0, func_angle(-20), Bd.advanceConfig)
                        motionProxy.moveTo(0.2, 0.0,0, Bd.advanceConfig)
                        lock = threading.Condition()
                        getBallInfoThread = GetBallInfoThread(name="for-field01-")
                        getBallInfoThread.start()
                        t1 = threading.Thread(target=field_1_1)
                        t1.start()
                        t1.join()
                        ttsProxy.say("击球")
                        t2 = threading.Thread(target=field_1_2)

                        t2.start()
                        t2.join()
                        t3 = threading.Thread(target=field_1_3)
                        t3.start()
                        t3.join()
                        while True:
                            t4 = threading.Thread(target=field_hexagon)
                            t4.start()
                            t4.join()
                            ttsProxy.say("前击")

                    if memoryProxy.getData("MiddleTactilTouched") == 1:
                        lock = threading.Condition()
                        getBallInfoThread = GetBallInfoThread(name="for-field02-")
                        getBallInfoThread.start()
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
                        t4 = threading.Thread(target=field_2_4)
                        t4.start()
                        t4.join()
                        while True:
                            t5 = threading.Thread(target=field_hexagon)
                            t5.start()
                            t5.join()
                            ttsProxy.say("前击")
                    if memoryProxy.getData("RearTactilTouched") == 1:
                        lock = threading.Condition()
                        getBallInfoThread = GetBallInfoThread(name="for-field03-")
                        getBallInfoThread.start()
                        t1 = threading.Thread(target=field_3_1)
                        t1.start()
                        t1.join()
                        ttsProxy.say("击球")
                        t2 = threading.Thread(target=field_3_2)
                        t2.start()
                        t2.join()
                        ttsProxy.say("击球")
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
