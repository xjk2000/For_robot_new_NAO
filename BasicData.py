#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : BasicData.py
@CreateTime :2021/7/29 22:19 
@Author : 许嘉凯
@Version  : 1.0
@Description :
自己写的一些常用量及环境配置
"""
from naoqi import ALProxy
from vision_definitions import *
# 机器人的互联网地址及端口
IP = "169.254.203.231"
PORT = 9559

# 以下是机器人的代理对象

# 内存管理模块
memoryProxy = ALProxy("ALMemory", IP, PORT)
# 动作管理模块
motionProxy = ALProxy("ALMotion", IP, PORT)
# 预定义姿势模块
postureProxy = ALProxy("ALRobotPosture", IP, PORT)
# 语音转换模块
ttsProxy = ALProxy("ALTextToSpeech", IP, PORT)
# 提供基于快速视觉的红球探测器模块
redBallProxy = ALProxy("ALRedBallDetection", IP, PORT)
# 负责以一种有效的方式，从视频源(如机器人的摄像机，模拟器)提供图像给所有处理它们的模块
videoDeviceProxy = ALProxy("ALVideoDevice", IP, PORT)
# 一个视觉模块，机器人可以在其中识别带有特定图案的特殊地标
landmarkProxy = ALProxy("ALLandMarkDetection", IP, PORT)

# 以下主要是基本的步态参数

# 前进的基本步态
# advanceConfig = [
#         # 最大前进距离
#         ["MaxStepX", 0.042],
#         # 最大横向位移
#         ["MaxStepY", 0.132],
#         # 最大旋转角度
#         ["MaxStepTheta", 0.04],
#         # 最大步频
#         ["MaxStepFrequency", 0.45],
#         # 最高抬脚高度
#         ["StepHeight", 0.010],
#         # x轴躯干旋转
#         ["TorsoWx", 0],
#         # y轴躯干旋转
#         ["TorsoWy", 0]
#     ]
advanceConfig = [
        ["MaxStepX", 0.04],
        ["MaxStepY", 0.145],
        ["MaxStepTheta", 0.4],
        ["MaxStepFrequency", 0.4],
        ["StepHeight", 0.02],
        ["TorsoWx", 0],
        ["TorsoWy", 0]
    ]
# 前进的微调步态
advanceSlightlyConfig = [
        # 最大前进距离
        ["MaxStepX", 0.024],
        # 最大横向位移
        ["MaxStepY", 0.14],
        # 最大旋转角度
        ["MaxStepTheta", 0.42],
        # 最大步频
        ["MaxStepFrequency", 0.5],
        # 最高抬脚高度
        ["StepHeight", 0.015],
        # x轴躯干旋转
        ["TorsoWx", 0],
        # y轴躯干旋转
        ["TorsoWy", 0]
    ]

# 旋转微调步态
rotationSlightlyConfig = [
        ["MaxStepX", 0.03],
        ["MaxStepY", 0.14],
        ["MaxStepTheta", 0.4],
        ["MaxStepFrequency", 0.3],
        ["StepHeight", 0.02],
        ["TorsoWx", 0],
        ["TorsoWy", 0]
    ]
# 旋转基本步态
rotationConfig = [["MaxStepX", 0.04], ["MaxStepY", 0.14], ["MaxStepTheta", 0.3], ["MaxStepFrequency", 0.6],
               ["StepHeight", 0.02], ["TorsoWx", 0], ["TorsoWy", 0]]

# 后退基本步态
backConfig = [
        # 最大前进距离
        ["MaxStepX", 0.042],
        # 最大横向位移
        ["MaxStepY", 0.132],
        # 最大旋转角度
        ["MaxStepTheta", 0.04],
        # 最大步频
        ["MaxStepFrequency", 0.45],
        # 最高抬脚高度
        ["StepHeight", 0.010],
        # x轴躯干旋转
        ["TorsoWx", 0],
        # y轴躯干旋转
        ["TorsoWy", 0]
    ]

# 后退微调步态
backSlightlyConfig = [
        # 最大前进距离
        ["MaxStepX", 0.042],
        # 最大横向位移
        ["MaxStepY", 0.132],
        # 最大旋转角度
        ["MaxStepTheta", 0.04],
        # 最大步频
        ["MaxStepFrequency", 0.45],
        # 最高抬脚高度
        ["StepHeight", 0.010],
        # x轴躯干旋转
        ["TorsoWx", 0],
        # y轴躯干旋转
        ["TorsoWy", 0]
    ]

# 横移微调步态
swingSlightlyConfig = [
        # 最大前进距离
        ["MaxStepX", 0.042],
        # 最大横向位移
        ["MaxStepY", 0.132],
        # 最大旋转角度
        ["MaxStepTheta", 0.04],
        # 最大步频
        ["MaxStepFrequency", 0.45],
        # 最高抬脚高度
        ["StepHeight", 0.010],
        # x轴躯干旋转
        ["TorsoWx", 0],
        # y轴躯干旋转
        ["TorsoWy", 0]
    ]

# 横移基本步态
swingConfig = [
        ["MaxStepX", 0.04],
        ["MaxStepY", 0.145],
        ["MaxStepTheta", 0.4],
        ["MaxStepFrequency", 0.35],
        ["StepHeight", 0.02],
        ["TorsoWx", 0],
        ["TorsoWy", 0]
    ]