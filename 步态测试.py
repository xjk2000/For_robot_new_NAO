#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : 步态测试.py
@CreateTime :2021/7/20 10:53 
@Author : 许嘉凯
@Version  : 1.0
@Description : 
"""

import math

import naoqi
from naoqi import ALProxy


def func_angle(x):
    return x * math.pi / 180.0


def close_pole(ip, port=9559):
    """
    收杆

    :param ip: 机器人ip
    :param port: 机器人端口
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

    naoqi.ALProxy("ALMotion", ip, port).setMoveArmsEnabled(False, False)
    naoqi.ALProxy("ALMotion", ip, port).angleInterpolation(joints_name, angle, move_time, True)


if __name__ == '__main__':
    naoIp = "169.254.244.127"
    naoPort = 9559
    motionProxy = ALProxy("ALMotion", naoIp, naoPort)
    ttsProxy = ALProxy("ALTextToSpeech", naoIp, naoPort)
    memoryProxy = ALProxy("ALMemory", naoIp, naoPort)
    redBallProxy = ALProxy("ALRedBallDetection", naoIp, naoPort)
    cameraProxy = ALProxy("ALVideoDevice", naoIp, naoPort)
    motionProxy.wakeUp()

    # 定义全局步态参数
    # 前进使用的参数
    moveConfig1 = [
        ["MaxStepX", 0.04],
        ["MaxStepY", 0.14],
        ["MaxStepTheta", 0.4],
        ["MaxStepFrequency", 0.6],
        ["StepHeight", 0.02],
        ["TorsoWx", 0],
        ["TorsoWy", 0]
    ]
    # 旋转步态参数
    moveConfig2 = [
        ["MaxStepX", 0.04],
        ["MaxStepY", 0.14],
        ["MaxStepTheta", 0.4],
        ["MaxStepFrequency", 0.6],
        ["StepHeight", 0.02],
        ["TorsoWx", 0],
        ["TorsoWy", 0]
    ]
    # 横向偏移步态参数
    moveConfig3 = [
        ["MaxStepX", 0.04],
        ["MaxStepY", 0.14],
        ["MaxStepTheta", 0.4],
        ["MaxStepFrequency", 0.6],
        ["StepHeight", 0.02],
        ["TorsoWx", 0],
        ["TorsoWy", 0]
    ]
    # 倒退步态参数
    moveConfig4 = [
        ["MaxStepX", 0.04],
        ["MaxStepY", 0.14],
        ["MaxStepTheta", 0.4],
        ["MaxStepFrequency", 0.6],
        ["StepHeight", 0.02],
        ["TorsoWx", 0],
        ["TorsoWy", 0]
    ]

    close_pole(naoIp, naoPort)
    motionProxy.moveTo(1.0, 0, 0, moveConfig1)
    # motionProxy.moveTo(0,0,90*math.pi/180,moveConfig1)
    # motionProxy.moveTo(0,0.5,0,moveConfig3)
    # motionProxy.moveTo(-0.5,0,0,moveConfig4)
