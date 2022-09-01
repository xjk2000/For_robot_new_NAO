# !/usr/bin/python2.7
# -*- encoding: UTF-8 -*-

import math
import time
import sys
import argparse
from naoqi import ALProxy


# -----------------------------------------------------机器人姿势定义---------------------------------------------------#
def positionHitBallqian():  # 前ji
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append([-2.5 * math.pi / 180.0, -31.5 * math.pi / 180.0, -82.7 * math.pi / 180.0,
                 -86.8 * math.pi / 180.0])  # -69.1  红-86.1 -86.4

    names.append("LElbowYaw")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append([-101.1 * math.pi / 180.0, -61.8 * math.pi / 180.0, -48.7 * math.pi / 180.0,
                 -0.2 * math.pi / 180.0])  # -30.8 红 -8.6 -2.6

    names.append("LShoulderPitch")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append(
        [61.3 * math.pi / 180.0, 0.3 * math.pi / 180.0, 9.4 * math.pi / 180.0, -1.7 * math.pi / 180.0])  # -5.0 红 7.8 1

    names.append("LShoulderRoll")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append([50.1 * math.pi / 180.0, 3.2 * math.pi / 180.0, -15.9 * math.pi / 180.0,
                 -8.8 * math.pi / 180.0])  # -2.3 -5.0 2.5

    names.append("LWristYaw")
    times.append([0.8, 1.5, 3.0, 4.5])
    keys.append([3.9 * math.pi / 180.0, 64.5 * math.pi / 180.0, -51.8 * math.pi / 180.0,
                 -78.6 * math.pi / 180.0])  # -45.5#-68.6

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
    times.append([1.5])
    keys.append([-33.9 * math.pi / 180.0])

    names.append("LAnkleRoll")
    times.append([1.5])
    keys.append([-0.6 * math.pi / 180.0])

    # 左手握杆positionHitBall
    names.append("LHand")
    times.append([1.5])
    keys.append([0.0])  # [0.0, 0.0]

    names.append("LHipPitch")
    times.append([1.5])
    keys.append([-38.3 * math.pi / 180.0])

    names.append("LHipRoll")
    times.append([1.5])
    keys.append([0.4 * math.pi / 180.0])

    names.append("LHipYawPitch")
    times.append([1.5])
    keys.append([-1.1 * math.pi / 180.0])

    names.append("LKneePitch")
    times.append([1.5])
    keys.append([61.6 * math.pi / 180.0])

    names.append("RAnklePitch")
    times.append([1.5])
    keys.append([-34.5 * math.pi / 180.0])

    names.append("RAnkleRoll")
    times.append([1.5])
    keys.append([-0.4 * math.pi / 180.0])

    names.append("RHipPitch")
    times.append([1.5])
    keys.append([-42.9 * math.pi / 180.0])

    names.append("RHipRoll")
    times.append([1.5])
    keys.append([-0.6 * math.pi / 180.0])

    names.append("RHipYawPitch")
    times.append([1.5])
    keys.append([-1.1 * math.pi / 180.0])

    names.append("RKneePitch")
    times.append([1.5])
    keys.append([65.8 * math.pi / 180.0])

    return [names, keys, times]


def positionHitBall():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.5, 3.0])  # [1.5, 3.0]
    keys.append([-0.00215657, -0.00215657])

    names.append("HeadYaw")
    times.append([1.5, 3.0])
    keys.append([0, 0])

    names.append("LAnklePitch")
    times.append([1.5, 3.0])
    keys.append([-0.351406, -0.351406])

    names.append("LAnkleRoll")
    times.append([1.5, 3.0])
    keys.append([-0.00147909, -0.00147909])

    names.append("LElbowRoll")
    times.append([1.5, 3.0])
    keys.append([-0.537794, -0.537794])

    names.append("LElbowYaw")
    times.append([1.5, 3.0])
    keys.append([-1.4488, -1.4488])
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
    times.append([1.5, 3.0])
    keys.append([1.32389, -3.01811e-05])

    names.append("LWristYaw")
    times.append([1.5, 3.0])  # [1.5, 3.0]
    keys.append([61.4205 * math.pi / 180.0, 40 * math.pi / 180.0])  # [1.07199, 0.527726]#0.627差不多61.4205度到30.2364度

    names.append("RAnklePitch")
    times.append([1.5, 3.0])
    keys.append([-0.350177, -0.350177])

    names.append("RAnkleRoll")
    times.append([1.5, 3.0])
    keys.append([0.00361548, 0.00361548])

    names.append("RElbowRoll")
    times.append([1.5, 3.0])
    keys.append([0.530618, 0.530618])

    names.append("RElbowYaw")
    times.append([1.5, 3.0])
    keys.append([1.39613, 1.39613])

    names.append("RHand")
    times.append([1.5, 3.0])
    keys.append([0.0590473, 1])

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
    keys.append([-0.279325, -0.279325])

    names.append("RWristYaw")
    times.append([1.5, 3.0])
    keys.append([0.0384861, 101.7 * math.pi / 180.0])
    return [names, keys, times]


def positionHitBall2():
    names = list()
    times = list()
    keys = list()

    names.append("LElbowRoll")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([-80.0 * math.pi / 180.0, -62.2 * math.pi / 180.0, -62.3 * math.pi / 180.0, -0.541034])

    names.append("LElbowYaw")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([-84.4 * math.pi / 180.0, -86.8 * math.pi / 180.0, -86.1 * math.pi / 180.0, -1.45072])

    names.append("LHand")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([0.0, 0.0, 0.0, 0.0])

    names.append("LShoulderPitch")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([86.9 * math.pi / 180.0, 38.9 * math.pi / 180.0, 23.1 * math.pi / 180.0, 0.363146])

    names.append("LShoulderRoll")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([6.3 * math.pi / 180.0, 5.7 * math.pi / 180.0, 3.7 * math.pi / 180.0, -3.01811e-05])

    names.append("LWristYaw")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([-101.9 * math.pi / 180.0, -99.8 * math.pi / 180.0, -12.8 * math.pi / 180.0, 0.527726])

    names.append("RElbowRoll")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([87.4 * math.pi / 180.0, 45.7 * math.pi / 180.0, 45.7 * math.pi / 180.0, 45.7 * math.pi / 180.0])

    names.append("RElbowYaw")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([87.1 * math.pi / 180.0, 93.9 * math.pi / 180.0, 93.9 * math.pi / 180.0, 93.9 * math.pi / 180.0])

    names.append("RHand")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([1, 1, 1, 1])

    names.append("RShoulderPitch")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([118.7 * math.pi / 180.0, 109.3 * math.pi / 180.0, 109.3 * math.pi / 180.0, 109.3 * math.pi / 180.0])

    names.append("RShoulderRoll")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([-9.1 * math.pi / 180.0, -11.7 * math.pi / 180.0, -11.7 * math.pi / 180.0, -11.7 * math.pi / 180.0])

    names.append("RWristYaw")
    times.append([1.0, 2.0, 3.0, 4.0])
    keys.append([101.7 * math.pi / 180.0, 101.7 * math.pi / 180.0, 101.7 * math.pi / 180.0, 101.7 * math.pi / 180.0])
    return [names, keys, times]


def positionHitBall3():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.5, 3.0])  # [1.5, 3.0]
    keys.append([-0.00215657, -0.00215657])

    names.append("HeadYaw")
    times.append([1.5, 3.0])
    keys.append([0, 0])

    names.append("LAnklePitch")
    times.append([1.5, 3.0])
    keys.append([-0.351406, -0.351406])

    names.append("LAnkleRoll")
    times.append([1.5, 3.0])
    keys.append([-0.00147909, -0.00147909])

    names.append("LElbowRoll")
    times.append([1.5, 3.0])
    keys.append([-0.541034, -0.541034])

    names.append("LElbowYaw")
    times.append([1.5, 3.0])
    keys.append([-1.45072, -1.45072])
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
    keys.append([0.284888, 0.363146])

    names.append("LShoulderRoll")
    times.append([1.5, 3.0])
    keys.append([1.32389, -3.01811e-05])

    names.append("LWristYaw")
    times.append([1.5, 3.0])  # [1.5, 3.0]
    keys.append([1.07199, 0.527726])  # [1.07199, 0.527726]#0.627差不多61.4205度到30.2364度

    names.append("RAnklePitch")
    times.append([1.5, 3.0])
    keys.append([-0.350177, -0.350177])

    names.append("RAnkleRoll")
    times.append([1.5, 3.0])
    keys.append([0.00361548, 0.00361548])

    names.append("RElbowRoll")
    times.append([1.5, 3.0])
    keys.append([0.530618, 0.530618])

    names.append("RElbowYaw")
    times.append([1.5, 3.0])
    keys.append([1.39613, 1.39613])

    names.append("RHand")
    times.append([1.5, 3.0])
    keys.append([0.0590473, 0.0590473])

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
    keys.append([-0.279325, -0.279325])

    names.append("RWristYaw")
    times.append([1.5, 3.0])
    keys.append([0.0384861, 0.0384861])
    return [names, keys, times]


def positionHitBall5():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.5, 3.0])  # [1.5, 3.0]
    keys.append([-0.00215657, -0.00215657])

    names.append("HeadYaw")
    times.append([1.5, 3.0])
    keys.append([0, 0])

    names.append("LAnklePitch")
    times.append([1.5, 3.0])
    keys.append([-0.351406, -0.351406])

    names.append("LAnkleRoll")
    times.append([1.5, 3.0])
    keys.append([-0.00147909, -0.00147909])

    names.append("LElbowRoll")
    times.append([1.5, 3.0])
    keys.append([-0.537794, -0.537794])

    names.append("LElbowYaw")
    times.append([1.5, 3.0])
    keys.append([-1.4488, -1.4488])
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
    keys.append([0.7])  # 加到1.0试一下

    names.append("LWristYaw")
    times.append([1.5])  # [1.5, 3.0]
    keys.append([51.4205 * math.pi / 180.0])  # [1.07199, 0.527726]#0.627差不多61.4205度到30.2364度

    names.append("RAnklePitch")
    times.append([1.5, 3.0])
    keys.append([-0.350177, -0.350177])

    names.append("RAnkleRoll")
    times.append([1.5, 3.0])
    keys.append([0.00361548, 0.00361548])

    names.append("RElbowRoll")
    times.append([1.5, 3.0])
    keys.append([0.530618, 0.530618])

    names.append("RElbowYaw")
    times.append([1.5, 3.0])
    keys.append([1.39613, 1.39613])

    names.append("RHand")
    times.append([1.5, 3.0])
    keys.append([0.0590473, 1])

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
    keys.append([-0.279325, -0.279325])

    names.append("RWristYaw")
    times.append([1.5, 3.0])
    keys.append([0.0384861, 101.7 * math.pi / 180.0])
    return [names, keys, times]



def positionStandWithStick():
    names = list()
    times = list()
    keys = list()

    asd = 1.7

    # 1.7适合蓝色的机器人
    # 1.75适合红色的机器人
    # asd=1.75
    # 1.7适合蓝色的机器人
    names.append("HeadPitch")
    times.append([1.08])
    keys.append([-0.00215657])

    names.append("HeadYaw")
    times.append([1.08])
    keys.append([0])

    names.append("LAnklePitch")
    times.append([1.08])
    keys.append([-0.351406])

    names.append("LAnkleRoll")
    times.append([1.8])
    keys.append([-0.00147909])

    names.append("LElbowRoll")
    times.append([1.08])
    keys.append([-80.5 * math.pi / 180.0])

    names.append("LElbowYaw")
    times.append([1.08])
    keys.append([-83.8 * math.pi / 180.0])

    names.append("LHand")
    times.append([1.08])
    keys.append([0])

    names.append("LHipPitch")
    times.append([1.08])
    keys.append([-0.444635])

    names.append("LHipRoll")
    times.append([1.08])
    keys.append([0.00744654])

    names.append("LHipYawPitch")
    times.append([1.08])
    keys.append([-0.00721956])

    names.append("LKneePitch")
    times.append([1.08])
    keys.append([0.704064])

    names.append("LShoulderPitch")
    times.append([1.08])
    keys.append([85.9 * math.pi / 180.0])

    names.append("LShoulderRoll")
    times.append([1.08])
    keys.append([5.5 * math.pi / 180.0])

    names.append("LWristYaw")
    times.append([1.08])
    keys.append([-101.7 * math.pi / 180.0])

    names.append("RAnklePitch")
    times.append([1.08])
    keys.append([-0.350177])

    names.append("RAnkleRoll")
    times.append([1.08])
    keys.append([0.00361548])

    names.append("RElbowRoll")
    times.append([asd])
    keys.append([76.5 * math.pi / 180.0])  # 80.5*math.pi/180.0

    names.append("RElbowYaw")
    times.append([asd])
    keys.append([83.3 * math.pi / 180.0])

    names.append("RHand")
    times.append([asd])
    keys.append([1])

    names.append("RHipPitch")
    times.append([1.08])
    keys.append([-0.45268])

    names.append("RHipRoll")
    times.append([1.08])
    keys.append([-0.00643682])

    names.append("RHipYawPitch")
    times.append([1.08])
    keys.append([-0.00721956])

    names.append("RKneePitch")
    times.append([1.08])
    keys.append([0.699545])

    names.append("RShoulderPitch")
    times.append([asd])
    keys.append([85.9 * math.pi / 180.0])  # 85.9*math.pi/180.0 ,81.4*math.pi/180.0

    names.append("RShoulderRoll")
    times.append([asd])
    keys.append([5.5 * math.pi / 180.0])  # 5.5*math.pi/180.0,-0.5*math.pi/180.0

    names.append("RWristYaw")
    times.append([asd])
    keys.append([101.7 * math.pi / 180.0])  # 101.7*math.pi/180.0
    return [names, keys, times]


def positionStandWithStick1():
    names = list()
    times = list()
    keys = list()

    asd = 1.75

    # 1.7适合蓝色的机器人
    # 1.75适合红色的机器人
    # asd=1.75
    # 1.7适合蓝色的机器人
    names.append("HeadPitch")
    times.append([1.08])
    keys.append([-0.00215657])

    names.append("HeadYaw")
    times.append([1.08])
    keys.append([0])

    names.append("LAnklePitch")
    times.append([1.08])
    keys.append([-0.351406])

    names.append("LAnkleRoll")
    times.append([1.8])
    keys.append([-0.00147909])

    names.append("LElbowRoll")
    times.append([1.08])
    keys.append([-88 * math.pi / 180.0])  # -80.5*math.pi/180.0

    names.append("LElbowYaw")
    times.append([1.08])
    keys.append([-83.8 * math.pi / 180.0])

    names.append("LHand")
    times.append([1.08])
    keys.append([0])

    names.append("LHipPitch")
    times.append([1.08])
    keys.append([-0.444635])

    names.append("LHipRoll")
    times.append([1.08])
    keys.append([0.00744654])

    names.append("LHipYawPitch")
    times.append([1.08])
    keys.append([-0.00721956])

    names.append("LKneePitch")
    times.append([1.08])
    keys.append([0.704064])

    names.append("LShoulderPitch")
    times.append([1.08])
    keys.append([85.9 * math.pi / 180.0])

    names.append("LShoulderRoll")
    times.append([1.08])
    keys.append([5.5 * math.pi / 180.0])

    names.append("LWristYaw")
    times.append([1.08])
    keys.append([-101.7 * math.pi / 180.0])

    names.append("RAnklePitch")
    times.append([1.08])
    keys.append([-0.350177])

    names.append("RAnkleRoll")
    times.append([1.08])
    keys.append([0.00361548])

    names.append("RElbowRoll")
    times.append([asd])
    keys.append([88 * math.pi / 180.0])  # 80.5*math.pi/180.0  76.5*math.pi/180.0

    names.append("RElbowYaw")
    times.append([asd])
    keys.append([83.3 * math.pi / 180.0])

    names.append("RHand")
    times.append([asd])
    keys.append([1])

    names.append("RHipPitch")
    times.append([1.08])
    keys.append([-0.45268])

    names.append("RHipRoll")
    times.append([1.08])
    keys.append([-0.00643682])

    names.append("RHipYawPitch")
    times.append([1.08])
    keys.append([-0.00721956])

    names.append("RKneePitch")
    times.append([1.08])
    keys.append([0.699545])

    names.append("RShoulderPitch")
    times.append([asd])
    keys.append([85.9 * math.pi / 180.0])  # 85.9*math.pi/180.0 ,81.4*math.pi/180.0

    names.append("RShoulderRoll")
    times.append([asd])
    keys.append([5.5 * math.pi / 180.0])  # 5.5*math.pi/180.0,-0.5*math.pi/180.0

    names.append("RWristYaw")
    times.append([asd])
    keys.append([101.7 * math.pi / 180.0])  # 101.7*math.pi/180.0
    return [names, keys, times]

def positionStandWithStick0():
    names = list()
    times = list()
    keys = list()

    names = list()
    times = list()
    keys = list()

    names.append("LShoulderPitch")  # 肩关节旋转
    times.append([1.08])
    keys.append([118.6 * math.pi / 180.0])

    names.append("LShoulderRoll")  # 肩关节展开
    times.append([1.08])
    keys.append([66.0 * math.pi / 180.0])

    names.append("LElbowYaw")  # 肘关节旋转
    times.append([1.08])
    keys.append([-118.9 * math.pi / 180.0])

    names.append("LElbowRoll")  # 肘关节弯曲
    times.append([1.08])
    keys.append([-47.0 * math.pi / 180.0])

    names.append("LWristYaw")  # 手腕旋转
    times.append([1.08])
    keys.append([-12.6 * math.pi / 180.0])

    names.append("HeadPitch")
    times.append([1.08])
    keys.append([-0.00215657])

    names.append("HeadYaw")
    times.append([1.08])
    keys.append([0])

    names.append("LAnklePitch")  # 脚踝上下
    times.append([1.08])
    keys.append([-0.5340708])

    names.append("LAnkleRoll")  # 脚踝左右
    times.append([1.08])
    keys.append([-0.0087266])

    names.append("LHipPitch")  # 大腿上下
    times.append([1.08])
    keys.append([-0.3228859])

    names.append("LHipRoll")  # 大腿左右
    times.append([1.08])
    keys.append([-0.0034907])

    names.append("LHipYawPitch")  # 大大腿
    times.append([1.08])
    keys.append([0.0])

    names.append("LKneePitch")  # 膝盖
    times.append([1.08])
    keys.append([0.8464847])

    names.append("RElbowRoll")
    times.append([1.08])
    keys.append([0.421753])

    names.append("RElbowYaw")
    times.append([1.08])
    keys.append([1.21901])

    names.append("RHand")
    times.append([1.08])
    keys.append([0.3])

    names.append("RShoulderPitch")
    times.append([1.08])
    keys.append([1.41927])

    names.append("RShoulderRoll")
    times.append([1.08])
    keys.append([-0.262217])

    names.append("RWristYaw")
    times.append([1.08])
    keys.append([0.0915835])

    names.append("RAnklePitch")  # 脚踝上下
    times.append([1.08])
    keys.append([-0.5340708])

    names.append("RAnkleRoll")  # 脚踝左右
    times.append([1.08])
    keys.append([-0.0087266])

    names.append("RHipPitch")  # 大腿上下
    times.append([1.08])
    keys.append([-0.3228859])

    names.append("RHipRoll")  # 大腿左右
    times.append([1.08])
    keys.append([-0.0034907])

    names.append("RHipYawPitch")  # 大大腿
    times.append([1.08])
    keys.append([0.0])

    names.append("RKneePitch")  # 膝盖
    times.append([1.08])
    keys.append([0.8464847])
    return [names, keys, times]


def positionStandWithStick5():
    names = list()
    times = list()
    keys = list()

    names = list()
    times = list()
    keys = list()

    names.append("LShoulderPitch")  # 肩关节旋转
    times.append([1.08, 2.0])
    keys.append([119.5 * math.pi / 180.0, 118.6 * math.pi / 180.0])

    names.append("LShoulderRoll")  # 肩关节展开
    times.append([1.08, 2.0])
    keys.append([38.4 * math.pi / 180.0, -0.4 * math.pi / 180.0])

    names.append("LElbowYaw")  # 肘关节旋转
    times.append([1.08, 2.0])
    keys.append([-119.5 * math.pi / 180.0, -118.9 * math.pi / 180.0])

    names.append("LElbowRoll")  # 肘关节弯曲
    times.append([1.08, 2.0])
    keys.append([-46.8 * math.pi / 180.0, -47.0 * math.pi / 180.0])

    names.append("LWristYaw")  # 手腕旋转
    times.append([1.08, 2.0])
    keys.append([16.5 * math.pi / 180.0, -12.6 * math.pi / 180.0])

    names.append("HeadPitch")
    times.append([1.08])
    keys.append([-0.00215657])

    names.append("HeadYaw")
    times.append([1.08])
    keys.append([0])

    names.append("LAnklePitch")  # 脚踝上下
    times.append([1.08])
    keys.append([-0.5340708])

    names.append("LAnkleRoll")  # 脚踝左右
    times.append([1.08])
    keys.append([-0.0087266])

    names.append("LHipPitch")  # 大腿上下
    times.append([1.08])
    keys.append([-0.3228859])

    names.append("LHipRoll")  # 大腿左右
    times.append([1.08])
    keys.append([-0.0034907])

    names.append("LHipYawPitch")  # 大大腿
    times.append([1.08])
    keys.append([0.0])

    names.append("LKneePitch")  # 膝盖
    times.append([1.08])
    keys.append([0.8464847])

    names.append("RElbowRoll")
    times.append([1.08])
    keys.append([0.421753])

    names.append("RElbowYaw")
    times.append([1.08])
    keys.append([1.21901])

    names.append("RHand")
    times.append([1.08])
    keys.append([0.3])

    names.append("RShoulderPitch")
    times.append([1.08])
    keys.append([1.41927])

    names.append("RShoulderRoll")
    times.append([1.08])
    keys.append([-0.262217])

    names.append("RWristYaw")
    times.append([1.08])
    keys.append([0.0915835])

    names.append("RAnklePitch")  # 脚踝上下
    times.append([1.08])
    keys.append([-0.5340708])

    names.append("RAnkleRoll")  # 脚踝左右
    times.append([1.08])
    keys.append([-0.0087266])

    names.append("RHipPitch")  # 大腿上下
    times.append([1.08])
    keys.append([-0.3228859])

    names.append("RHipRoll")  # 大腿左右
    times.append([1.08])
    keys.append([-0.0034907])

    names.append("RHipYawPitch")  # 大大腿
    times.append([1.08])
    keys.append([0.0])

    names.append("RKneePitch")  # 膝盖
    times.append([1.08])
    keys.append([0.8464847])
    return [names, keys, times]


def positionStandWithStick2():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.08])
    keys.append([-0.00215657])

    names.append("HeadYaw")
    times.append([1.08])
    keys.append([0])

    names.append("LAnklePitch")
    times.append([1.08])
    keys.append([-0.351406])

    names.append("LAnkleRoll")
    times.append([1.08])
    keys.append([-0.00147909])

    names.append("LElbowRoll")
    times.append([1.08])
    keys.append([-0.0707442])

    names.append("LElbowYaw")
    times.append([1.08])
    keys.append([-0.00491104])
    # positionStandWithStick
    names.append("LHand")
    times.append([1.08])
    keys.append([0.0])  # [0]

    names.append("LHipPitch")
    times.append([1.08])
    keys.append([-0.444635])

    names.append("LHipRoll")
    times.append([1.08])
    keys.append([0.00744654])

    names.append("LHipYawPitch")
    times.append([1.08])
    keys.append([-0.00721956])

    names.append("LKneePitch")
    times.append([1.08])
    keys.append([0.704064])

    names.append("LShoulderPitch")
    times.append([1.08])
    keys.append([1.78726])

    names.append("LShoulderRoll")
    times.append([1.08])
    keys.append([0.387533])

    names.append("LWristYaw")
    times.append([1.08])
    keys.append([-1.61286])

    names.append("RAnklePitch")
    times.append([1.08])
    keys.append([-0.350177])

    names.append("RAnkleRoll")
    times.append([1.08])
    keys.append([0.00361548])

    names.append("RElbowRoll")
    times.append([1.08])
    keys.append([0.421753])

    names.append("RElbowYaw")
    times.append([1.08])
    keys.append([1.21901])

    names.append("RHand")
    times.append([1.08])
    keys.append([0.3])

    names.append("RHipPitch")
    times.append([1.08])
    keys.append([-0.45268])

    names.append("RHipRoll")
    times.append([1.08])
    keys.append([-0.00643682])

    names.append("RHipYawPitch")
    times.append([1.08])
    keys.append([-0.00721956])

    names.append("RKneePitch")
    times.append([1.08])
    keys.append([0.699545])

    names.append("RShoulderPitch")
    times.append([1.08])
    keys.append([1.41927])

    names.append("RShoulderRoll")
    times.append([1.08])
    keys.append([-0.262217])

    names.append("RWristYaw")
    times.append([1.08])
    keys.append([0.0915835])
    return [names, keys, times]


def positionReleaseStick():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.08])
    keys.append([-0.00215657])

    names.append("HeadYaw")
    times.append([1.08])
    keys.append([0])

    names.append("LAnklePitch")
    times.append([1.08])
    keys.append([-0.358999])

    names.append("LAnkleRoll")
    times.append([1.08])
    keys.append([-0.00147909])

    names.append("LElbowRoll")
    times.append([1.08])
    keys.append([-0.537794])

    names.append("LElbowYaw")
    times.append([1.08])
    keys.append([-1.4488])

    names.append("LHand")
    times.append([1.08])
    keys.append([1])

    names.append("LHipPitch")
    times.append([1.08])
    keys.append([-0.444635])

    names.append("LHipRoll")
    times.append([1.08])
    keys.append([0.00744654])

    names.append("LHipYawPitch")
    times.append([1.08])
    keys.append([-0.00721956])

    names.append("LKneePitch")
    times.append([1.08])
    keys.append([0.696988])

    names.append("LShoulderPitch")
    times.append([1.08])
    keys.append([0.283386])

    names.append("LShoulderRoll")
    times.append([1.08])
    keys.append([-0.00171348])

    names.append("LWristYaw")
    times.append([1.08])
    keys.append([-0.0934926])

    names.append("RAnklePitch")
    times.append([1.08])
    keys.append([-0.357381])

    names.append("RAnkleRoll")
    times.append([1.08])
    keys.append([0.00361548])

    names.append("RElbowRoll")
    times.append([1.08])
    keys.append([0.546897])

    names.append("RElbowYaw")
    times.append([1.08])
    keys.append([1.39182])

    names.append("RHand")
    times.append([1.08])
    keys.append([0.0644])

    names.append("RHipPitch")
    times.append([1.08])
    keys.append([-0.45268])

    names.append("RHipRoll")
    times.append([1.08])
    keys.append([-0.00643682])

    names.append("RHipYawPitch")
    times.append([1.08])
    keys.append([-0.00721956])

    names.append("RKneePitch")
    times.append([1.08])
    keys.append([0.693492])

    names.append("RShoulderPitch")
    times.append([1.08])
    keys.append([1.45116])

    names.append("RShoulderRoll")
    times.append([1.08])
    keys.append([-0.252997])

    names.append("RWristYaw")
    times.append([1.08])
    keys.append([0.0160101])

    return [names, keys, times]


def positionCatchStick():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0.48])
    keys.append([0])

    names.append("HeadYaw")
    times.append([0.48])
    keys.append([0])

    names.append("LAnklePitch")
    times.append([0.48])
    keys.append([-0.358999])  # -0.351406

    names.append("LAnkleRoll")
    times.append([0.48])
    keys.append([-0.00147909])  # 0

    names.append("LElbowRoll")
    times.append([0.48])
    keys.append([-0.537794])  # -0.517034

    names.append("LElbowYaw")
    times.append([0.48])
    keys.append([-1.4488])  # -1.45072
    # 左手握杆positionCatchStick
    names.append("LHand")
    times.append([5])  # 0.48#3
    keys.append([0.0])  # 0.0

    names.append("LHipPitch")
    times.append([0.48])
    keys.append([-0.444635])

    names.append("LHipRoll")
    times.append([0.48])
    keys.append([0.00744654])  # 0

    names.append("LHipYawPitch")
    times.append([0.48])
    keys.append([-0.00721956])  # 0

    names.append("LKneePitch")
    times.append([0.48])
    keys.append([0.696988])  # 0.704064

    names.append("LShoulderPitch")
    times.append([0.48])
    keys.append([0.283386])  # 0.385181

    names.append("LShoulderRoll")
    times.append([0.48])
    keys.append([-0.00171348])  # -0.00935468

    names.append("LWristYaw")
    times.append([0.48])
    keys.append([-0.0934926])  # -0.077322

    names.append("RAnklePitch")
    times.append([0.48])
    keys.append([-0.357381])  # -0.350177

    names.append("RAnkleRoll")
    times.append([0.48])
    keys.append([0.00361548])  # 0

    names.append("RElbowRoll")
    times.append([0.48])
    keys.append([0.546897])  # 0.532616

    names.append("RElbowYaw")
    times.append([0.48])
    keys.append([1.39182])  # 1.39879

    names.append("RHand")
    times.append([0.48])  # [0.48]
    keys.append([0.0644])  # 0.0590473

    names.append("RHipPitch")
    times.append([0.48])
    keys.append([-0.45268])

    names.append("RHipRoll")
    times.append([0.48])
    keys.append([-0.00643682])  # 0

    names.append("RHipYawPitch")
    times.append([0.48])
    keys.append([-0.00721956])  # 0

    names.append("RKneePitch")
    times.append([0.48])
    keys.append([0.693492])  # 0.699545

    names.append("RShoulderPitch")
    times.append([0.48])
    keys.append([1.45116])  # 1.41542

    names.append("RShoulderRoll")
    times.append([0.48])
    keys.append([-0.252997])  # -0.276462

    names.append("RWristYaw")
    times.append([0.48])
    keys.append([0.0384861])
    return [names, keys, times]


def positionRaiseStick():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([1.08, 1.68])
    keys.append([-0.00215657, -0.00215657])

    names.append("HeadYaw")
    times.append([1.08, 1.68])
    keys.append([0, 0])

    names.append("LAnklePitch")
    times.append([1.08, 1.68])
    keys.append([-0.358999, -0.358999])

    names.append("LAnkleRoll")
    times.append([1.08, 1.68])
    keys.append([-0.00147909, -0.00147909])

    names.append("LElbowRoll")
    times.append([1.08, 1.68])
    keys.append([-0.537794, -0.537794])

    names.append("LElbowYaw")
    times.append([1.08, 1.68])
    keys.append([-1.4488, -1.4488])
    # positionRaiseStick
    names.append("LHand")
    times.append([1.08, 1.68])
    keys.append([0.0, 0.0])

    names.append("LHipPitch")
    times.append([1.08, 1.68])
    keys.append([-0.444635, -0.444635])

    names.append("LHipRoll")
    times.append([1.08, 1.68])
    keys.append([0.00744654, 0.00744654])

    names.append("LHipYawPitch")
    times.append([1.08, 1.68])
    keys.append([-0.00721956, -0.00721956])

    names.append("LKneePitch")
    times.append([1.08, 1.68])
    keys.append([0.696988, 0.696988])

    names.append("LShoulderPitch")
    times.append([1.08, 1.68])
    keys.append([0.283386, 0.283386])

    names.append("LShoulderRoll")
    times.append([1.08, 1.68])
    keys.append([-0.000886967, 1.32045])

    names.append("LWristYaw")
    times.append([1.08, 1.68])
    keys.append([1.65869, 1.07807])

    names.append("RAnklePitch")
    times.append([1.08, 1.68])
    keys.append([-0.357381, -0.357381])

    names.append("RAnkleRoll")
    times.append([1.08, 1.68])
    keys.append([0.00361548, 0.00361548])

    names.append("RElbowRoll")
    times.append([1.08, 1.68])
    keys.append([0.546897, 0.546897])

    names.append("RElbowYaw")
    times.append([1.08, 1.68])
    keys.append([1.39182, 1.39182])

    names.append("RHand")
    times.append([1.08, 1.68])
    keys.append([0.0644, 0.0644])

    names.append("RHipPitch")
    times.append([1.08, 1.68])
    keys.append([-0.45268, -0.45268])

    names.append("RHipRoll")
    times.append([1.08, 1.68])
    keys.append([-0.00643682, -0.00643682])

    names.append("RHipYawPitch")
    times.append([1.08, 1.68])
    keys.append([-0.00721956, -0.00721956])

    names.append("RKneePitch")
    times.append([1.08, 1.68])
    keys.append([0.693492, 0.693492])

    names.append("RShoulderPitch")
    times.append([1.08, 1.68])
    keys.append([1.44085, 1.44085])

    names.append("RShoulderRoll")
    times.append([1.08, 1.68])
    keys.append([-0.265356, -0.276408])

    names.append("RWristYaw")
    times.append([1.08, 1.68])
    keys.append([0.0160101, 0.0160101])
    return [names, keys, times]


# ---------------------------------------------------机器人姿势定义结束--------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
# *********************************************************************************************************************
# @函数名：   raiseStick()
# @参数：    robotIP - 机器人IP地址
#           port - 机器人端口
# @返回值：   无
# @功能说明： 机器人放杆过程中防止让杆碰地，所以加了一个举杆的中间动作
# @最后修改日期：2016-8-29
# *********************************************************************************************************************
def raiseStick(robotIP="127.0.0.1", port=9559):
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionRaiseStick()
    MOTION.angleInterpolation(names, keys, times, True)


# ---------------------------------------------------------------------------------------------------------------------#
# *********************************************************************************************************************
# @函数名：   standWithStick()
# @参数：    speed - 站立速度，目前保留
#           robotIP - 机器人IP地址
#           port - 机器人端口
# @返回值：   无
# @功能说明： 机器人在移动过程中以及识别物体时的站立姿势
# @最后修改日期：2016-8-29
# *********************************************************************************************************************
def standWithStick(speed=0.1, robotIP="127.0.0.1", port=9559):
    speed = speed
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionStandWithStick()
    MOTION.angleInterpolation(names, keys, times, True)


def standWithStick1(speed=0.1, robotIP="127.0.0.1", port=9559):
    speed = speed
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionStandWithStick1()
    MOTION.angleInterpolation(names, keys, times, True)


def standWithStick2(speed=0.1, robotIP="127.0.0.1", port=9559):
    speed = speed
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionStandWithStick2()
    MOTION.angleInterpolation(names, keys, times, True)


def standWithStick5(speed=0.1, robotIP="127.0.0.1", port=9559):
    speed = speed
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionStandWithStick5()
    MOTION.angleInterpolation(names, keys, times, True)


def standWithStick0(speed=0.1, robotIP="127.0.0.1", port=9559):
    speed = speed
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionStandWithStick0()
    MOTION.angleInterpolation(names, keys, times, True)


# ---------------------------------------------------------------------------------------------------------------------#
# *********************************************************************************************************************
# @函数名：   catchStick()
# @参数：     robotIP - 机器人IP地址
#           port - 机器人端口
# @返回值：   无
# @功能说明： 最开始的抓杆动作，左手抓杆。
# @最后修改日期：2016-8-29
# *********************************************************************************************************************
def catchStick(robotIP="127.0.0.1", port=9559):
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionCatchStick()
    MOTION.angleInterpolation(names, keys, times, True)


# ---------------------------------------------------------------------------------------------------------------------#
# *********************************************************************************************************************
# @函数名：   releaseStick()
# @参数：     robotIP - 机器人IP地址
#           port - 机器人端口
# @返回值：   无
# @功能说明： 松杆
# @最后修改日期：2016-8-29
# *********************************************************************************************************************
def releaseStick(robotIP="127.0.0.1", port=9559):
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionReleaseStick()
    MOTION.angleInterpolation(names, keys, times, True)


# ---------------------------------------------------------------------------------------------------------------------#
# *********************************************************************************************************************
# @函数名：   hitBall()
# @参数：     hitBallSpeed - 击球力度
#           robotIP - 机器人IP地址
#           port - 机器人端口
# @返回值：   无
# @功能说明： 机器人最终的击球动作。
# @最后修改日期：2016-8-29
# *********************************************************************************************************************
def hitBallqian(hitBallSpeed=0.1, robotIP="127.0.0.1", port=9559):
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionHitBallqian()
    MOTION.angleInterpolation(names, keys, times, True)
    time.sleep(1)
    MOTION.angleInterpolationWithSpeed("LWristYaw", -40 * math.pi / 180.0, hitBallSpeed * 3)

def hitBall5(hitBallSpeed=0.1, robotIP="127.0.0.1", port=9559):#目前红球最好的
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionHitBall5()
    MOTION.angleInterpolation(names, keys, times, True)
    KnuckleBearing = (["LShoulderRoll","LWristYaw"])
    Targetangle = ([-0.002,-50*math.pi/180.0])
    #MOTION.angleInterpolationWithSpeed("LShoulderRoll", -0.002, hitBallSpeed *2)
    #MOTION.angleInterpolationWithSpeed("LWristYaw", -50 * math.pi / 180.0, hitBallSpeed * 2)#插值 控制单个关节 原有角度到该角度
    MOTION.angleInterpolationWithSpeed(KnuckleBearing,Targetangle, hitBallSpeed * 2)#插值 控制单个关节 原有角度到该角度


def hitBall3(hitBallSpeed=0.1, robotIP="127.0.0.1", port=9559):
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionHitBall3()
    MOTION.angleInterpolation(names, keys, times, True)
    time.sleep(1)
    MOTION.angleInterpolationWithSpeed("LWristYaw", -50 * math.pi / 180.0, hitBallSpeed * 2)


def hitBall2(hitBallSpeed=0.1, robotIP="127.0.0.1", port=9559):
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionHitBall2()
    MOTION.angleInterpolation(names, keys, times, True)
    # 把角度从-30改为-50:2018.8.7
    # MOTION.angleInterpolationWithSpeed("LWristYaw", -50*math.pi/180.0, hitBallSpeed)


def hitBall(hitBallSpeed=0.1, robotIP="127.0.0.1", port=9559):
    MOTION = ALProxy("ALMotion", robotIP, port)
    names, keys, times = positionHitBall()
    MOTION.angleInterpolation(names, keys, times, True)
    time.sleep(1)
    MOTION.angleInterpolationWithSpeed("LWristYaw", -50 * math.pi / 180.0, hitBallSpeed * 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number.")
    args = parser.parse_args()
    robotIP = args.ip
    port = args.port

    MOTION = ALProxy("ALMotion", robotIP, port)
    POSTURE = ALProxy("ALRobotPosture", robotIP, port)
    MOTION.setFallManagerEnabled(True)
