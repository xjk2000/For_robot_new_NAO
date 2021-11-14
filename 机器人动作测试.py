#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : 机器人动作测试.py
@CreateTime :2021/10/22 15:53 
@Author : 许嘉凯
@Version  : 1.0
@Description : 
"""
import time

from BasicData import motionProxy
from publicApi import func_angle, grip,close_pole


def fieldOneFirstShot_test():
    """
    右手向左轻击击球,并收球
    :return:
    """
    joints_name = []
    angle = []
    move_time = []

    joints_name.append("RShoulderPitch")
    angle.append(
        [func_angle(97.0), func_angle(57.6),func_angle(22)])
    move_time.append([1.0, 2.5,4])

    joints_name.append("RShoulderRoll")
    angle.append(
        [func_angle(-59.1), func_angle(-34.6),func_angle(14.9)])
    move_time.append([1.0, 2.5,4])

    joints_name.append("RElbowYaw")
    angle.append(
        [func_angle(110.9), func_angle(87.2),func_angle(116.2)])
    move_time.append([1.0, 2.5,4])

    joints_name.append("RElbowRoll")
    angle.append(
        [func_angle(66.3), func_angle(81.5),func_angle(36)])
    move_time.append([1.0, 2.5,4])

    joints_name.append("RWristYaw")
    angle.append(
        [func_angle(28.4), func_angle(28.0),func_angle(-55)])
    move_time.append([1.0, 2.5,4])

    motionProxy.setMoveArmsEnabled(False, False)
    motionProxy.angleInterpolation(joints_name, angle, move_time, True)
    # motionProxy
    motionProxy.angleInterpolationWithSpeed("RWristYaw", func_angle(77), 1)

    # joints_name = []
    # angle = []
    # move_time = []
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
    # joints_name.append("RWristYaw")
    # angle.append(
    #     [func_angle(-0.7)])
    # move_time.append([1.0])
    #
    # motionProxy.angleInterpolation(joints_name, angle, move_time, True)


if __name__ == '__main__':
    motionProxy.wakeUp()
    grip()
    close_pole()
    fieldOneFirstShot_test()
    close_pole()

    motionProxy.angleInterpolationWithSpeed("RHand", 0.88, .5)
    time.sleep(1)
    motionProxy.angleInterpolationWithSpeed("RHand", 0.13, .5)
    motionProxy.rest()
