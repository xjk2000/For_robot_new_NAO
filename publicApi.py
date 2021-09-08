#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : publicApi.py
@CreateTime :2021/7/20 9:40 
@Author : 许嘉凯
@Version  : 1.0
@Description : 
"""
import math
import time

import naoqi


import motion
import numpy as np
import BasicData as BData
from BasicData import videoDeviceProxy as vPr
from BasicData import motionProxy as moPr
from BasicData import memoryProxy as mePr
from BasicData import landmarkProxy as lPr


def __find_ball(angle, sub_angle=0):
    """
    内置红球识别算法,判断是否找到红球

    :param angle:偏头角度
    :param sub_angle:低头角度
    :return: {
            'head-angle':偏头角度,
            'ballData':内置的球数据,
            'didYouFind':是否找到红球
        }
    """
    ballData = []
    BData.videoDeviceProxy.setActiveCamera(1)
    BData.motionProxy.angleInterpolationWithSpeed("HeadYaw", angle * math.pi / 180, 0.8)  # math.pi 圆周率  180/圆周率就是弧度转换公式
    BData.motionProxy.angleInterpolationWithSpeed("HeadPitch", sub_angle * math.pi / 180, 0.8)
    BData.redBallProxy.subscribe("redBallDetected")
    BData.memoryProxy.insertData("redBallDetected", [])  # 将数据插入内存

    # 增加红球识别和取消红球识别
    for i in range(10):
        ballData = BData.memoryProxy.getData("redBallDetected")

    # redballProxy.unsubscribe("redBallDetected")
    if ballData:
        print("红球位置在")
        print(ballData)
        headangle = BData.motionProxy.getAngles("HeadYaw", True)
        allballData = {
            'head-angle':headangle,
            'ballData':ballData,
            'didYouFind':True
        }
        return allballData
    else:
        print("没找到红球")
        return {
            'head-angle': None,
            'ballData': None,
            'didYouFind': False
        }


def __computing_robot_and_red_ball(ballSFieldOfViewData):
    """
    计算球和机器人的一部分数据

    :param ballSFieldOfViewData: 球的视野数据
    :return: 字典:
     {
        'centerX':红球球心在内置视野中的X,
        'centerY':红球球心在内置视野中的Y,
        'cameraX':摄像头X轴距离,
        'cameraY':摄像头Y轴距离,
        'cameraH':摄像头离地高度,
        'robotBallXDistance':机器人和红球的水平距离(及其不精确),
        'didFindBall':是否找到红球
    }

    """
    if ballSFieldOfViewData['ballData'] is not None or ballSFieldOfViewData['ballData'] != []:
        centerX = ballSFieldOfViewData['ballData'][1][0]
        centerY = ballSFieldOfViewData['ballData'][1][1]
        camera1Position = moPr.getPosition("CameraBottom", motion.FRAME_ROBOT, True)
        cameraX = camera1Position[0]
        cameraY = camera1Position[0]
        cameraH = camera1Position[0]
        robotBallHorizontalDistance = math.sqrt(
            (0.025 ** 2) / math.sin(ballSFieldOfViewData['ballData'][1][2]) ** 2 - (cameraH - 0.025)
        )
        print "红球球心在内置视野中的X" + str(centerX)
        print "红球球心在内置视野中的Y" + str(centerY)
        print "摄像头X轴距离" + str(cameraX)
        print "摄像头Y轴距离" + str(cameraY)
        print "摄像头离地高度" + str(cameraH)
        print "机器人和红球的水平距离(m):" + str(robotBallHorizontalDistance)

        return {
            'centerX':centerX,
            'centerY':centerY,
            'cameraX':cameraX,
            'cameraY':cameraY,
            'cameraH':cameraH,
            'robotBallXDistance':robotBallHorizontalDistance,
            'didFindBall':True
        }


def search_red_ball(searchTime=2):
    """
    查找(内置API)红球

    :param searchTime: 偏头查找次数
    :return: 如果找到红球返回红球信息 , 没找到返回 None
    """
    BData.videoDeviceProxy.setActiveCamera(1)

    searchRange = -60 * searchTime
    search = searchRange
    while search <= -searchRange:
        time.sleep(1)
        findBallInfo = __find_ball(search)
        if findBallInfo['didYouFind']:
            ballInfo = __computing_robot_and_red_ball(findBallInfo)
            ballInfo['head-angle'] = findBallInfo['head-angle']
            return ballInfo
        else:
            search += 60
    BData.motionProxy.angleInterpolationWithSpeed('HeadYaw', 0, 0.5)
    print "没有红球,准备前进再次寻找"
    BData.ttsProxy.say("当前视野中没有红球")
    moPr.moveTo(0.2,0,0,BData.advanceConfig)
    return search_red_ball(2)
    # if judgingTheLocation == 0:
    #     BData.motionProxy.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
    #     BData.motionProxy.setMoveArmsEnabled(False, False)
    #     BData.motionProxy.moveTo(0.3, 0.0, 0.0, BData.advance2Config)
    # elif judgingTheLocation == 1:
    #     BData.motionProxy.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
    #     BData.motionProxy.setMoveArmsEnabled(False, False)
    #     BData.motionProxy.moveTo(0, 0, 90 * math.pi / 180.0, BData.advance2Config)
    #     BData.motionProxy.moveTo(0.8, 0, 0, BData.advance2Config)
    #     # 找
    # elif judgingTheLocation == 2:
    #     BData.motionProxy.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
    #     BData.motionProxy.setMoveArmsEnabled(False, False)
    #     BData.motionProxy.moveTo(0, 0, -45 * math.pi / 180.0, BData.advance2Config)
    #     BData.motionProxy.moveTo(0.8, 0, 0, BData.advance2Config)
    # elif judgingTheLocation == 3:
    #     BData.motionProxy.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.5)
    #     BData.motionProxy.setMoveArmsEnabled(False, False)
    #     BData.motionProxy.moveTo(0, 0, -45 * math.pi / 180.0, BData.advance2Config)
    #     BData.motionProxy.moveTo(0.4, 0, 0, BData.advance2Config)
    #     BData.motionProxy.moveTo(0.5, 0, 0, BData.advance2Config)
    return None


def firstSearchNAOmark():
    headYawAngle = -2.0
    vPr.setActiveCamera(0)
    currentCamera = "CameraTop"

    moPr.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
    moPr.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.3)
    lPr.subscribe("landmarkTest")
    markData = mePr.getData("LandmarkDetected")
    while headYawAngle < 2.0:
        moPr.angleInterpolationWithSpeed("HeadYaw", headYawAngle, 0.1)
        time.sleep(1)
        for i in range(10):
            markData = mePr.getData("LandmarkDetected")
            if markData and isinstance(markData, list) and len(markData) >= 2:
                break

        if not (not markData or not isinstance(markData, list) or not (len(markData) >= 2)):
            landmarkFlag = 0  # landmark识别符0代表识别到，1代表未识别到。
            # Retrieve landmark center position in radians.
            markwzCamera = markData[1][0][0][1]
            markwyCamera = markData[1][0][0][2]
            # Retrieve landmark angular size in radians.
            markangularSize = markData[1][0][0][3]
            headangle = moPr.getAngles("HeadYaw", True)
            markheadangle = markwzCamera + headangle[0]
            allmarkdata = [markData[1][0][0][0], markwzCamera, markwyCamera, markangularSize, markheadangle,
                           landmarkFlag]
            markdata = {
                "alpha": markData[1][0][0][1],
                "beta": markData[1][0][0][2],
                "sizeX": markData[1][0][0][3],
                "sizeY": markData[1][0][0][4],
                "/actualAngle": (markData[1][0][0][1] + headangle[0])*(180/math.pi),
                "landmarkFlag":landmarkFlag
            }
            return markdata

        else:

            markwzCamera = 0
            markwyCamera = 0
            markangularSize = 0

        headYawAngle = headYawAngle + 0.5

    print "landmark is not in sight !"
    return [0, 0, 0, 0, 1]


def func_angle(x):
    """
    角度制转弧度制
    :param x:
    :return:
    """
    return x * math.pi / 180.0


def grip():
    """
    握杆

    :return:
    """
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RHand")
    angle.append([func_angle(100), func_angle(6)])
    move_time.append([2.3, 8.3])

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(41.3)])
    move_time.append([2.5])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-5.0)])
    move_time.append([2.5])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(85)])
    move_time.append([2.5])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(57.1)])
    move_time.append([2.5])

    joints_name.append("RWristYaw")
    angle.append([func_angle(1.2)])
    move_time.append([2.5])

    # 脚步动作
    joints_name.append("LHipYawPitch")
    angle.append([-0.00721956])
    move_time.append([1.08])

    joints_name.append("LKneePitch")
    angle.append([0.696988])
    move_time.append([1.08])

    joints_name.append("LAnklePitch")
    angle.append([-0.358999])
    move_time.append([1.08])

    joints_name.append("LAnkleRoll")
    angle.append([-0.00147909])
    move_time.append([1.08])

    joints_name.append("LHipPitch")
    angle.append([-0.444635])
    move_time.append([1.08])

    joints_name.append("LHipRoll")
    angle.append([0.00744654])
    move_time.append([1.08])

    joints_name.append("RHipRoll")
    angle.append([-0.00643682])
    move_time.append([1.08])

    joints_name.append("RHipPitch")
    angle.append([-0.45268])
    move_time.append([1.08])

    joints_name.append("RHipYawPitch")
    angle.append([-0.00721956])
    move_time.append([1.08])

    joints_name.append("RKneePitch")
    angle.append([0.693492])
    move_time.append([1.08])

    joints_name.append("RAnklePitch")
    angle.append([-0.357381])
    move_time.append([1.08])

    joints_name.append("RAnkleRoll")
    angle.append([0.00361548])
    move_time.append([1.08])

    # 头部动作
    joints_name.append("HeadYaw")
    angle.append([0.0])
    move_time.append([1.08])

    joints_name.append("HeadPitch")
    angle.append([-0.00215657])
    move_time.append([1.08])

    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(joints_name, angle, move_time, True)


def close_pole():
    """
    收杆

    :return:
    """
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(40), func_angle(85)])
    move_time.append([2.5, 5.5])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-70), func_angle(-13)])
    move_time.append([2.5, 5.5])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(35), func_angle(82)])
    move_time.append([2.5, 5.5])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(25), func_angle(12)])
    move_time.append([2.5, 5.5])

    joints_name.append("RWristYaw")
    angle.append([func_angle(1.2), func_angle(2.4)])
    move_time.append([2.5, 4.5])

    # 脚步动作
    joints_name.append("LHipYawPitch")
    angle.append([-0.00721956])
    move_time.append([1.08])

    joints_name.append("LKneePitch")
    angle.append([0.696988])
    move_time.append([1.08])

    joints_name.append("LAnklePitch")
    angle.append([-0.358999])
    move_time.append([1.08])

    joints_name.append("LAnkleRoll")
    angle.append([-0.00147909])
    move_time.append([1.08])

    joints_name.append("LHipPitch")
    angle.append([-0.444635])
    move_time.append([1.08])

    joints_name.append("LHipRoll")
    angle.append([0.00744654])
    move_time.append([1.08])

    joints_name.append("RHipRoll")
    angle.append([-0.00643682])
    move_time.append([1.08])

    joints_name.append("RHipPitch")
    angle.append([-0.45268])
    move_time.append([1.08])

    joints_name.append("RHipYawPitch")
    angle.append([-0.00721956])
    move_time.append([1.08])

    joints_name.append("RKneePitch")
    angle.append([0.693492])
    move_time.append([1.08])

    joints_name.append("RAnklePitch")
    angle.append([-0.357381])
    move_time.append([1.08])

    joints_name.append("RAnkleRoll")
    angle.append([0.00361548])
    move_time.append([1.08])

    # 头部动作
    joints_name.append("HeadYaw")
    angle.append([0.0])
    move_time.append([1.08])

    joints_name.append("HeadPitch")
    angle.append([-0.00215657])
    move_time.append([1.08])

    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(joints_name, angle, move_time, True)


def soft_hit_with11():
    """
    右手向左轻击击球,球距离右脚10cm~11cm

    :return:
    """
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(70), func_angle(41.3)])
    move_time.append([3.5, 4.5])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-65), func_angle(-5.0)])
    move_time.append([3.5, 4.5])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(80), func_angle(85)])
    move_time.append([3.5, 4.5])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(47), func_angle(57.1)])
    move_time.append([3.5, 4.5])

    joints_name.append("RWristYaw")
    angle.append([func_angle(-21), func_angle(-65.0), func_angle(50)])
    move_time.append([3.5, 6, 6.5])

    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(joints_name, angle, move_time, True)



def forwardHit():
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(70), func_angle(6),func_angle(34.1)])
    move_time.append([3.5, 4.5,5.5])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-65), func_angle(-10.80),func_angle(3.0)])
    move_time.append([3.5, 4.5,5.5])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(80), func_angle(29.4),func_angle(11.7)])
    move_time.append([3.5, 4.5,5.5])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(47), func_angle(73.1),func_angle(67.2)])
    move_time.append([3.5, 4.5,5.5])

    joints_name.append("RWristYaw")
    angle.append([func_angle(-21), func_angle(6.2), func_angle(35.6),func_angle(9.6)])
    move_time.append([3.5, 4.5, 5.5,5.8])

    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(joints_name, angle, move_time, True)
