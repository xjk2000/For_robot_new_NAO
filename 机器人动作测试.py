#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : 机器人动作测试.py
@CreateTime :2021/10/22 15:53 
@Author : 许嘉凯
@Version  : 1.0
@Description : 
"""
import math
import time

from BasicData import motionProxy
from publicApi import func_angle, grip,close_pole


def shotTest():
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

    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.angleInterpolation(joints_name, angle, move_time, True)


if __name__ == '__main__':
    motionProxy.wakeUp()
    grip()
    close_pole()
    shotTest()
    time.sleep(10)
    close_pole()

    motionProxy.angleInterpolationWithSpeed("RHand", 0.88, .5)
    time.sleep(1)
    motionProxy.angleInterpolationWithSpeed("RHand", 0.13, .5)
    motionProxy.rest()
