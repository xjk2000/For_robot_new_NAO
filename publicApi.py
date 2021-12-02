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
    angle.append([func_angle(100), func_angle(2)])
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


def fieldBasicShot():
    """
    基本击球打法
    :return:
    """
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(80), func_angle(40), func_angle(46)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-54), func_angle(-42), func_angle(18)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(12), func_angle(40), func_angle(100)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(2), func_angle(41), func_angle(53)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RWristYaw")
    angle.append([func_angle(47), func_angle(-30), func_angle(-12), func_angle(41)])
    move_time.append([3.5, 4.5, 4.7, 4.9])

    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(joints_name, angle, move_time, True)


def fieldThreeFirstShot():
    """
    基本击球打法
    :return:
    """
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(80), func_angle(40), func_angle(46)])
    move_time.append([3.5, 4.5, 5.2])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-54), func_angle(-42), func_angle(18)])
    move_time.append([3.5, 4.5, 5.2])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(12), func_angle(40), func_angle(100)])
    move_time.append([3.5, 4.5, 5.2])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(2), func_angle(41), func_angle(53)])
    move_time.append([3.5, 4.5, 5.2])

    joints_name.append("RWristYaw")
    angle.append([func_angle(47), func_angle(-30), func_angle(-12), func_angle(41)])
    move_time.append([3.5, 4.5, 4.9, 5.2])

    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(joints_name, angle, move_time, True)


def fieldTwoFirstShot():
    """
    场地二第一杆击球
    :return:
    """
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(80), func_angle(38), func_angle(43)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(-54), func_angle(-47), func_angle(18)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RElbowYaw")
    angle.append([func_angle(12), func_angle(40), func_angle(105)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(2), func_angle(38), func_angle(50)])
    move_time.append([3.5, 4.5, 4.9])

    joints_name.append("RWristYaw")
    angle.append([func_angle(47), func_angle(-30), func_angle(-12), func_angle(51)])
    move_time.append([3.5, 4.5, 4.7, 4.88])

    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(joints_name, angle, move_time, True)


def battingChange():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.5, 3.0])  # [1.5, 3.0]
    keys.append([-0.00215657, -0.00215657])

    names.append("HeadYaw")
    times.append([1.5, 3.0])
    keys.append([0.0590473, 1])

    names.append("LAnklePitch")
    times.append([1.5, 3.0])
    keys.append([-0.351406, -0.351406])

    names.append("LAnkleRoll")
    times.append([1.5, 3.0])
    keys.append([-0.00147909, -0.00147909])

    names.append("LElbowRoll")
    times.append([1.5, 3.0])
    keys.append([0.537794, 0.537794])

    names.append("LElbowYaw")
    times.append([1.5, 3.0])
    keys.append([1.4488, 1.4488])
    # 左手握杆positionHitBall
    names.append("LHand")
    times.append([1.5, 3.0])
    keys.append([0.0, 0.0])  # [0.0, 0.0]

    names.append("LHipPitch")
    times.append([1.5, 3.0])
    keys.append([-0.444635, -0.444635])

    names.append("LHipRoll")
    times.append([1.5, 3.0])
    keys.append([0.00744654, 0.00744654])

    names.append("LHipYawPitch")
    times.append([1.5, 3.0])
    keys.append([-0.00721956, -0.00721956])

    names.append("LKneePitch")
    times.append([1.5, 3.0])
    keys.append([0.704064, 0.704064])

    names.append("LShoulderPitch")
    times.append([1.5, 3.0])
    keys.append([0.283386, 0.363146])

    names.append("LShoulderRoll")
    times.append([1.5])
    keys.append([-0.7])  # 加到1.0试一下

    names.append("LWristYaw")
    times.append([1.5])  # [1.5, 3.0]
    keys.append([-51.4205 * math.pi / 180.0])  # [1.07199, 0.527726]#0.627差不多61.4205度到30.2364度

    names.append("RAnklePitch")
    times.append([1.5, 3.0])
    keys.append([-0.350177, -0.350177])

    names.append("RAnkleRoll")
    times.append([1.5, 3.0])
    keys.append([0.00361548, 0.00361548])

    names.append("RElbowRoll")
    times.append([1.5, 3.0])
    keys.append([-0.530618, -0.530618])

    names.append("RElbowYaw")
    times.append([1.5, 3.0])
    keys.append([-1.39613, -1.39613])

    names.append("RHand")
    times.append([1.5, 3.0])
    keys.append([0, 0])

    names.append("RHipPitch")
    times.append([1.5, 3.0])
    keys.append([-0.45268, -0.45268])

    names.append("RHipRoll")
    times.append([1.5, 3.0])
    keys.append([-0.00643682, -0.00643682])

    names.append("RHipYawPitch")
    times.append([1.5, 3.0])
    keys.append([-0.00721956, -0.00721956])

    names.append("RKneePitch")
    times.append([1.5, 3.0])
    keys.append([0.699545, 0.699545])

    names.append("RShoulderPitch")
    times.append([1.5, 3.0])
    keys.append([1.42169, 1.42169])

    names.append("RShoulderRoll")
    times.append([1.5, 3.0])
    keys.append([0.279325, 0.279325])

    names.append("RWristYaw")
    times.append([1.5, 3.0])
    keys.append([-0.0384861, -101.7 * math.pi / 180.0])

    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(names, keys, times, True)


def forwardHit():
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append([func_angle(100), func_angle(15)])
    # func_angle(5), func_angle(-5), func_angle(50), func_angle(91)])
    move_time.append([2.5, 3.5])

    joints_name.append("RShoulderRoll")
    angle.append([func_angle(0), func_angle(-30), func_angle(-30), func_angle(13)])
    # func_angle(1), func_angle(-60), func_angle(-65), func_angle(-17)])
    move_time.append([1.5, 2, 5.5, 7])  # 3.5

    joints_name.append("RElbowYaw")
    angle.append([func_angle(119.5), func_angle(0)])
    # func_angle(94.5), func_angle(40), func_angle(11), func_angle(66)])
    move_time.append([5.5, 7])

    joints_name.append("RElbowRoll")
    angle.append([func_angle(2), func_angle(88.5)])
    # func_angle(57.1), func_angle(34.5), func_angle(6), func_angle(3)])
    move_time.append([3.5, 4.5])

    joints_name.append("RWristYaw")
    angle.append([func_angle(-10), func_angle(-25), func_angle(-50), func_angle(45), func_angle(15)])
    # func_angle(60), func_angle(30), func_angle(35), func_angle(35)])
    move_time.append([2, 2.5, 4.5, 7, 7.5])

    # 脚步动作
    joints_name.append("LHipYawPitch")
    angle.append([func_angle(-0.2)])
    move_time.append([1.08])

    joints_name.append("LKneePitch")
    angle.append([func_angle(52.8)])
    move_time.append([1.08])

    joints_name.append("LAnklePitch")
    angle.append([func_angle(-30.3)])
    move_time.append([1.08])

    joints_name.append("LAnkleRoll")
    angle.append([func_angle(-0.3)])
    move_time.append([1.08])

    joints_name.append("LHipPitch")
    angle.append([func_angle(-33)])
    move_time.append([1.08])

    joints_name.append("LHipRoll")
    angle.append([func_angle(0.4)])
    move_time.append([1.08])

    joints_name.append("RHipRoll")
    angle.append([func_angle(0.4)])
    move_time.append([1.08])

    joints_name.append("RHipPitch")
    angle.append([func_angle(-33)])
    move_time.append([1.08])

    joints_name.append("RHipYawPitch")
    angle.append([func_angle(-0.2)])
    move_time.append([1.08])

    joints_name.append("RKneePitch")
    angle.append([func_angle(52.8)])
    move_time.append([1.08])

    joints_name.append("RAnklePitch")
    angle.append([func_angle(-30.3)])
    move_time.append([1.08])

    joints_name.append("RAnkleRoll")
    angle.append([func_angle(-0.3)])
    move_time.append([1.08])

    # 头部动作
    joints_name.append("HeadYaw")
    angle.append([0.0])
    move_time.append([1.08])

    joints_name.append("HeadPitch")
    angle.append([func_angle(-30)])
    move_time.append([1.08])

    moPr.setMoveArmsEnabled(False, False)
    moPr.angleInterpolation(joints_name, angle, move_time, True)