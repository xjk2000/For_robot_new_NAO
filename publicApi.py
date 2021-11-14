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
    angle.append([func_angle(0), func_angle(70), func_angle(100)])  # 40
    move_time.append([1.5, 2.3, 4.2])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-5), func_angle(-30), func_angle(0)])
    move_time.append([1.5, 2.0, 4.2])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(94.5), func_angle(119.5)])
    move_time.append([1.5, 4])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(57.1), func_angle(2)])
    move_time.append([1.5, 3.5])

    joints_name.append("RWristYaw")
    angle.append([func_angle(-60), func_angle(-60), func_angle(-10)])
    move_time.append([1.7, 2.2, 4.3])

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


def firstShotOfFieldTwo():
    """
    场地二第一次击球

    :return:
    """
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(80), func_angle(36), func_angle(43)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-54), func_angle(-42), func_angle(18)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(12), func_angle(40), func_angle(100)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(2), func_angle(38), func_angle(50)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RWristYaw")
    angle.append([func_angle(47), func_angle(-30), func_angle(-12), func_angle(41)])
    move_time.append([3.5, 4.5, 4.7, 4.9])

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


def fieldOneFirstShot():
    """
    场地一击球
    :return:
    """
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(70), func_angle(30)])
    move_time.append([3.5, 4.5])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-65), func_angle(18)])
    move_time.append([3.5, 4.5])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(80), func_angle(107.5)])
    move_time.append([3.5, 4.5])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(42), func_angle(43)])
    move_time.append([3.5, 4.5])

    joints_name.append("RWristYaw")
    angle.append([func_angle(-5), func_angle(-45), func_angle(-45), func_angle(6), func_angle(60)])
    move_time.append([3.0, 3.8, 4.8, 5, 5.2])
    # , func_angle(10), func_angle(0.0), func_angle(40), 3.5, 5.75, 5.87
    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(joints_name, angle, move_time, True)