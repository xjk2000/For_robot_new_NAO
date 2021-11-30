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
    """
    右手向左轻击击球,并收球
    :return:
    """
    names = []
    keys = []
    times = []

    names.append("RElbowRoll")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append([2.5 * math.pi / 180.0, 31.5 * math.pi / 180.0, 82.7 * math.pi / 180.0,
                 86.8 * math.pi / 180.0])  # -69.1  红-86.1 -86.4

    names.append("RElbowYaw")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append([101.1 * math.pi / 180.0, 61.8 * math.pi / 180.0, 48.7 * math.pi / 180.0,
                 0.2 * math.pi / 180.0])  # -30.8 红 -8.6 -2.6

    names.append("RShoulderPitch")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append(
        [61.3 * math.pi / 180.0, 0.3 * math.pi / 180.0, 9.4 * math.pi / 180.0, -1.7 * math.pi / 180.0])  # -5.0 红 7.8 1

    names.append("RShoulderRoll")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append([-50.1 * math.pi / 180.0, -3.2 * math.pi / 180.0, 15.9 * math.pi / 180.0,
                 8.8 * math.pi / 180.0])  # -2.3 -5.0 2.5

    names.append("RWristYaw")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append([-3.9 * math.pi / 180.0, -64.5 * math.pi / 180.0, 51.8 * math.pi / 180.0,
                 78.6 * math.pi / 180.0])  # -45.5#-68.6

    ##    names.append("LElbowRoll")
    ##    times.append([1.5,3.0,4.5])
    ##    keys.append([-31.5*math.pi/180.0, -69.1*math.pi/180.0, -86.4*math.pi/180.0])
    ##
    ##    names.append("LElbowYaw")
    ##    times.append([1.5,3.0,4.5])
    ##    keys.append([-61.8*math.pi/180.0,-30.8*math.pi/180.0, -2.6*math.pi/180.0])
    ##
    ##    names.append("LShoulderPitch")
    ##    times.append([1.5,3.0,4.5])
    ##    keys.append([0.3*math.pi/180.0,-5.0*math.pi/180.0,1.6*math.pi/180.0])
    ##
    ##    names.append("LShoulderRoll")
    ##    times.append([1.5,3.0,4.5])
    ##    keys.append([3.2*math.pi/180.0,-2.3*math.pi/180.0,-2.5*math.pi/180.0])
    ##
    ##    names.append("LWristYaw")
    ##    times.append([1.5,3.0,4.5])
    ##    keys.append([64.5*math.pi/180.0,-45.5*math.pi/180.0,-82.2*math.pi/180.0])

    names.append("HeadPitch")
    times.append([1.5])
    keys.append([-27.2 * math.pi / 180.0])

    names.append("HeadYaw")
    times.append([1.5, 3.0])
    keys.append([0, 0])

    names.append("LAnklePitch")
    times.append([1.5,5.5])
    keys.append([-33.9 * math.pi / 180.0,func_angle(-54.8)])

    names.append("LAnkleRoll")
    times.append([1.5,5.5])
    keys.append([-0.6 * math.pi / 180.0,func_angle(0.4)])

    # 左手握杆positionHitBall
    names.append("LHand")
    times.append([1.5])
    keys.append([0.0])  # [0.0, 0.0]

    names.append("LHipPitch")
    times.append([1.5,5.5])
    keys.append([-38.3 * math.pi / 180.0,func_angle(-49.3)])

    names.append("LHipRoll")
    times.append([1.5,5.5])
    keys.append([0.4 * math.pi / 180.0,func_angle(0.3)])

    names.append("LHipYawPitch")
    times.append([1.5,5.5])
    keys.append([-1.1 * math.pi / 180.0,func_angle(-1.1)])

    names.append("LKneePitch")
    times.append([1.5,5.5])
    keys.append([61.6 * math.pi / 180.0,func_angle(95.9)])

    names.append("RAnklePitch")
    times.append([1.5,5.5])
    keys.append([-34.5 * math.pi / 180.0,func_angle(-54.8)])

    names.append("RAnkleRoll")
    times.append([1.5,5.5])
    keys.append([-0.4 * math.pi / 180.0,func_angle(-0.4)])

    names.append("RHipPitch")
    times.append([1.5,5.5])
    keys.append([-42.9 * math.pi / 180.0,func_angle(-49.3)])

    names.append("RHipRoll")
    times.append([1.5,5.5])
    keys.append([-0.6 * math.pi / 180.0,func_angle(-0.3)])

    names.append("RHipYawPitch")
    times.append([1.5,5.5])
    keys.append([-1.1 * math.pi / 180.0,func_angle(-1.1)])

    names.append("RKneePitch")
    times.append([1.5,5.5])
    keys.append([65.8 * math.pi / 180.0,func_angle(95.9)])

    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.angleInterpolation(names, keys, times, True)
    # motionProxy

    joints_name = []
    angle = []
    move_time = []
    #
    # joints_name.append("RShoulderPitch")
    # angle.append(
    #     [func_angle(50.2)])
    # move_time.append([1.0])
    #
    # joints_name.append("RShoulderRoll")
    # angle.append(
    #     [func_angle(-51.3)])
    # move_time.append([1.0])
    #
    # joints_name.append("RElbowYaw")
    # angle.append(
    #     [func_angle(81.8)])
    # move_time.append([1.0])
    #
    # joints_name.append("RElbowRoll")
    # angle.append(
    #     [func_angle(32.5)])
    # move_time.append([1.0])
    #
    joints_name.append("RWristYaw")
    angle.append(
        [func_angle(60)])
    move_time.append([0.2])
    #
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
