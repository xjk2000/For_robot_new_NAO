#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : robotWithThread.py
@CreateTime :2021/9/8 19:57 
@Author : 许嘉凯
@Version  : 1.0
@Description : 
"""
import threading
import time

import BasicData as Bd
import GolfVision
import publicApi
from BasicData import IP
from BasicData import motionProxy

global ballDetect
global whetherToHitTheBall


class GetBallInfoThread(threading.Thread):
    def __init__(self, name):
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
            visualBasis = GolfVision.VisualBasis(IP, cameraId=Bd.kBottomCamera, resolution=Bd.kVGA)
            ballDetect = GolfVision.DetectRedBall(IP, resolution=Bd.kVGA, writeFrame=False)
            ballDetect.updateBallData(client="python_client1", colorSpace="HSV", fitting=True, minS1=180, minV1=33,
                                      maxH1=2,
                                      minH2=175)
            print ballDetect.ballPosition


class MoveThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        global ballDetect
        global whetherToHitTheBall
        motionProxy.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.5)
        time.sleep(3)
        print "move"
        # print ballDetect.ballData
        print ballDetect.ballPosition
        # 看到球之后
        if ballDetect.ballPosition['disX'] != 0:
            motionProxy.moveTo(ballDetect.ballPosition['disX'], ballDetect.ballPosition['disY'],
                               ballDetect.ballPosition['angle'], Bd.advanceConfig)
        # 视野中没有球( 球在脚边  球在区域外 )
        else:
            motionProxy.angleInterpolationWithSpeed("HeadPitch", 0.5, 0.5)
            if ballDetect.ballData['centerX'] != 0 and ballDetect.ballData['centerY'] != 0:
                whetherToHitTheBall = True
            else:
                motionProxy.moveTo(0.2, 0, 0, Bd.advanceConfig)


def hitBefore():
    global whetherToHitTheBall
    if whetherToHitTheBall:
        lock.acquire()
        publicApi.forwardHit()
        whetherToHitTheBall = False
        publicApi.forwardHit()


class BeforeHitThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self, name=name)

    def run(self):
        hitBefore()


if __name__ == '__main__':
    lock = threading.Lock()
    whetherToHitTheBall = False
    thread1 = GetBallInfoThread("getm")
    thread2 = MoveThread("movet")
    motionProxy.wakeUp()
    publicApi.close_pole()
    motionProxy.moveTo(0.8, 0, publicApi.func_angle(-10), Bd.advanceConfig)
    visualBasis = GolfVision.VisualBasis(IP, cameraId=Bd.kBottomCamera, resolution=Bd.kVGA)
    ballDetect = GolfVision.DetectRedBall(IP, resolution=Bd.kVGA, writeFrame=False)
    ballDetect.updateBallData(client="python_client1", colorSpace="HSV", fitting=True, minS1=180, minV1=33, maxH1=2,
                              minH2=175)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

