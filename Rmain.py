# -*- coding: utf-8 -*-
# @Time    : 2020/9/30 19:03
# @Author  : Baokang_Xie
# @FileName: N61main.py
# @Software: PyCharm

import argparse
import math
import sys
import time

from naoqi import ALBroker, ALModule
from naoqi import ALProxy

from Detection_class import AllDetection, OptimizeData
from movement import raiseStick, standWithStick5, catchStick, releaseStick, \
    hitBallqian, hitBall5, standWithStick0

# ------------------------------------------------全局变量定义-------------------------------------------------------------#
holeFlag = 0  # 球洞标志。   1：第一个球洞   2：第二个球洞   3：第三个球洞
robotHasFallenFlag = 0  # 机器人跌倒检测标志
myGolf = None
codeTest = False  # 测试标志，如果为True，代码直接从最后一个击球阶段进行
# ------------------------------------------------参数定义（根据实际情况调整）----------------------------------------------#
# ----------击球速度---------------------#
HitBallSpeed_FirstHole_Num_1 = 0.125 * 4  # 场地一力度
HitBallSpeed_SecondHole_Num_1 = 0.2  # 场地二力度
HitBallSpeed_ThirdHole_Num_3 = 0.095  # 场地三第一杆力度
HitBallSpeed_SecondHole_Num_5 = 0.25  # 场地二一杆进洞
# HitBallSpeed_SecondHole_Num_1 = 0.125#第一杆机球力度

HitBallSpeed_SecondHole_Num_2 = 0.175  # 前击力度
HitBallSpeed_SecondHole_Num_4 = 0.1  # 场地三第二杆力度
HitBallSpeed_SecondHole_Num_0 = 0.33

# -----------------步态三的补偿角----------------
compensation_3 = 4 * math.pi / 180.0

compensation_2 = 3 * math.pi / 180.0
# 红色HSV阈值
S1 = 125
V1 = 96
H1 = 4
H2 = 146

minH = 5
minS = 56
minV = 101
maxH = 57


def main(robotIP, port):
    myBroker = ALBroker("myBroker", "nao.local", 0, robotIP, port)
    TTS = ALProxy("ALTextToSpeech", robotIP, port)
    MOTION = ALProxy("ALMotion", robotIP, port)
    POSTURE = ALProxy("ALRobotPosture", robotIP, port)

    # 实例化
    global myGolf
    myGolf = Golf("myGolf", robotIP, port)
    alldet = AllDetection(robotIP)
    opt = OptimizeData(robotIP)
    MOTION.setFallManagerEnabled(True)

    # --------------------------------------------------------主死循环结束--------------------------------------------------------#
    try:
        # -----------------------------------------------------主死循环，待机状态-----------------------------------------------------#
        # standWithStick standWithStick1 双手  standWithStick2单手 catchStick 握手伸直 releaseStick 张手伸直 raiseStick 挥手
        while (True):
            '''判断是否蹲下，握杆环节'''
            if (MOTION.robotIsWakeUp() == False):
                # TTS.say("开始")
                MOTION.wakeUp()
                POSTURE.goToPosture("StandInit", 0.3)
                MOTION.setMoveArmsEnabled(False, False)  # 移动前需要加禁用手臂
                time.sleep(0.5)
                releaseStick(robotIP, port)  # 伸手 （官网说明）
                # TTS.say("准备握手")
                time.sleep(5)  # 控制握手时间
                catchStick(robotIP, port)  # 停十秒 握手 /// #

            time.sleep(1)
            print "holeFlag =", holeFlag
            if (holeFlag != 0):
                # ---------------------------------------------次死循环，工作状态------------------------------------------------------#
                while (True):
                    MOTION.setMoveArmsEnabled(False, False)

                    if (codeTest == False):  # 测试标志，如果为True，代码直接从最后一个击球阶段进行
                        # ---------------------高尔夫击球第一个阶段，直打----------------------------------------------#
                        if (holeFlag == 1):
                            # TTS.say("场地一一秒后开始")
                            time.sleep(1)
                            raiseStick(robotIP, port)
                            standWithStick5(0.1, robotIP, port)
                            MOTION.moveTo(0.4, 0, compensation_2, moveConfig2)  ##加偏角
                            MOTION.moveTo(0.4, 0, compensation_2, moveConfig2)  ##加偏角
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            if not len(redBallInfo):
                                MOTION.moveTo(0.20, 0, compensation_2, moveConfig2)  ##加偏角
                                redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                                if not len(redBallInfo):
                                    TTS.say("not find")
                                    holeFlag = 0
                                    break
                            MOTION.moveTo(0, 0, redBallInfo[1], moveConfig2)
                            MOTION.moveTo(redBallInfo[0] - 0.45, 0, compensation_2, moveConfig2)  ##加偏角
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            MOTION.moveTo(0, 0, redBallInfo[1], moveConfig2)
                            MOTION.moveTo(redBallInfo[0] - 0.3, 0, compensation_2, moveConfig2)  ##加偏角
                            # 三点一线-------------------------------------------------------
                            stickInfo = alldet.yellowStickDetection(minH, minS, minV, maxH, 1)
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            opt.threePointsAndOneLine(-0.26, 0.11, compensation_3, redBallInfo,
                                                      stickInfo, moveConfig3)
                            #
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            MOTION.moveTo(0.0, 0, redBallInfo[1], moveConfig3)
                            MOTION.moveTo(redBallInfo[0] - 0.1, 0, compensation_3, moveConfig3)
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            MOTION.moveTo(0.0, 0, redBallInfo[1], moveConfig3)
                            # MOTION.moveTo(0.0, 0.07, compensation_3, moveConfig3)
                            time.sleep(0.5)
                            hitBallqian(HitBallSpeed_SecondHole_Num_0, robotIP, port)  # 击球，前击
                            time.sleep(5)
                            if holeFlag == 3:
                                catchStick(robotIP, port)
                                holeFlag = 0
                                break
                            time.sleep(1)
                            raiseStick(robotIP, port)
                            standWithStick5(0.1, robotIP, port)
                            MOTION.moveTo(0.55, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0.55, 0, compensation_2, moveConfig2)
                            holeFlag = 0

                        if (holeFlag == 2):
                            time.sleep(0.5)
                            raiseStick(robotIP, port)
                            standWithStick5(0.1, robotIP, port)
                            MOTION.moveTo(0.25, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0.295, 0, compensation_2, moveConfig2)
                            time.sleep(0.5)
                            MOTION.moveTo(0.0, 0, 45 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.0, 0, 45 * math.pi / 180.0, moveConfig2)

                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            MOTION.moveTo(0.0, redBallInfo[0] * math.sin(redBallInfo[1]), 0.0, moveConfig3)
                            MOTION.moveTo(redBallInfo[0] * math.cos(redBallInfo[1]) - 0.20, 0.0, 0.0, moveConfig3)

                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            MOTION.moveTo(0.0, 0.0, redBallInfo[1] + 2 * math.pi / 180.0, moveConfig3)
                            MOTION.moveTo(redBallInfo[0] - 0.15, 0.0, 0.0, moveConfig3)
                            MOTION.moveTo(0, -0.06, 0.0, moveConfig3)
                            standWithStick0(0.1, robotIP, port)
                            raiseStick(robotIP, port)
                            # catchStick(robotIP, port)
                            hitBall5(HitBallSpeed_SecondHole_Num_1, robotIP, port)  # 击球
                            time.sleep(5)
                            if holeFlag == 3:
                                holeFlag = 0
                                break
                            raiseStick(robotIP, port)
                            standWithStick5(0.1, robotIP, port)
                            time.sleep(5)
                            MOTION.moveTo(0.6, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0, 0, -30 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0, 0, -30 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0, 0, -10 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.56, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0.0, 0, 3 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.56, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0, 0, -5 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.56, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0, 0, 5 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.5, 0, compensation_2, moveConfig2)
                            holeFlag = 0
                            '''
                            MOTION.moveTo(-0.30, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0, 0, -30 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0, 0, -30 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0, 0, -10 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.56, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0.0, 0, 10 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.56, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0, 0, 5 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.56, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0, 0, 5 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.5, 0, compensation_2, moveConfig2)
                            '''
                            holeFlag = 0

                        if (holeFlag == 3):
                            raiseStick(robotIP, port)
                            standWithStick5(0.1, robotIP, port)
                            MOTION.moveTo(0.1, 0, 0.0, moveConfig2)
                            MOTION.moveTo(0.0, 0, (- math.pi / 2 + math.atan(100 / 75)) / 2, moveConfig2)
                            # MOTION.moveTo(0.0, 0, (- math.pi / 2 + math.atan(100 / 75)) / 2, moveConfig2)
                            MOTION.moveTo(0.0, 0.4 * math.cos(math.atan(100 / 75)) + 0.05, -6 * math.pi / 180.0,
                                          moveConfig2)
                            # MOTION.moveTo(0.0, 0.0, 20*math.pi/180.0, moveConfig2)

                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            MOTION.moveTo(0.0, redBallInfo[0] * math.sin(redBallInfo[1]), 0.0, moveConfig2)
                            MOTION.moveTo(redBallInfo[0] * math.cos(redBallInfo[1]) - 0.10, 0.0, 0.0, moveConfig3)
                            MOTION.moveTo(0.0, 0.0, 24 * math.pi / 180.0, moveConfig3)
                            MOTION.moveTo(0.0, 0.04, 0.0, moveConfig3)
                            time.sleep(0.5)

                            hitBallqian(HitBallSpeed_SecondHole_Num_4, robotIP, port)  # 击球，前击
                            time.sleep(5)
                            if holeFlag == 1:
                                catchStick(robotIP, port)
                                holeFlag = 0
                                break
                            time.sleep(1)
                            raiseStick(robotIP, port)
                            standWithStick5(0.1, robotIP, port)
                            MOTION.moveTo(0.0, 0, (math.pi / 2 - math.atan(100 / 75)) / 2, moveConfig2)
                            # MOTION.moveTo(0, 0, (-math.pi / 2 + 10 * math.pi / 180.0) / 3, moveConfig2)
                            # MOTION.moveTo(0, 0, (-math.pi / 2 + 10 * math.pi / 180.0) / 4, moveConfig2)
                            MOTION.moveTo(0.65, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0.65, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0.30, 0, 0.0, moveConfig2)
                            MOTION.moveTo(0, 0, -40 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0, 0, -20 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0.20, 0, compensation_2, moveConfig2)

                            # ------------------------------------------------------场地三上阶段红球识别----------------------------------------------------

                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            if not len(redBallInfo):
                                MOTION.moveTo(0.2, 0, compensation_2, moveConfig2)
                                MOTION.moveTo(0, 0, 30 * math.pi / 180.0, moveConfig2)
                                redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            if not len(redBallInfo):
                                MOTION.moveTo(0, 0, -30 * math.pi / 180.0, moveConfig2)
                                MOTION.moveTo(0, 0, -20 * math.pi / 180.0, moveConfig2)
                                redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            if not len(redBallInfo):
                                TTS.say('没有找到红球，请重新开始！')
                                exit()
                            MOTION.moveTo(0, 0, redBallInfo[1], moveConfig2)
                            time.sleep(0.5)
                            MOTION.moveTo(redBallInfo[0] - 0.4, 0, compensation_2, moveConfig2)

                            # ------------------------------------------------------场地三第二次红球识别-----------------------------------------------------

                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            MOTION.moveTo(0, 0, redBallInfo[1], moveConfig2)
                            MOTION.moveTo(redBallInfo[0] - 0.35, 0, compensation_2, moveConfig2)
                            # 校准红球与机器人位置

                            # ------------------------------------------------------场地三上阶段第一次三点一线-----------------------------------------------------

                            stickInfo = alldet.yellowStickDetection(minH, minS, minV, maxH, 1)
                            while len(stickInfo) == 0:
                                opt.redBallReference(moveConfig2, S1, V1, H1, H2)
                                stickInfo = alldet.yellowStickDetection(minH, minS, minV, maxH, 1)
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            opt.threePointsAndOneLine(-0.3, 0.05, compensation_3, redBallInfo,
                                                      stickInfo, moveConfig3)

                            # ------------------------------------------------------场地三上阶段第二次三点一线----------------------------------------------------

                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            stickInfo = alldet.yellowStickDetection(minH, minS, minV, maxH, 1)
                            opt.threePointsAndOneLine(-0.25, 0.05, compensation_3, redBallInfo,
                                                      stickInfo, moveConfig3)

                            # ------------------------------------------------------场地三前阶段击球---------------------------------------------------------

                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            MOTION.moveTo(0.0, 0, redBallInfo[1], moveConfig3)
                            MOTION.moveTo(redBallInfo[0] - 0.13, 0, compensation_3, moveConfig3)
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            MOTION.moveTo(0.0, 0, redBallInfo[1], moveConfig3)
                            MOTION.moveTo(0.0, 0.05, compensation_3, moveConfig3)
                            time.sleep(0.5)
                            hitBallqian(HitBallSpeed_SecondHole_Num_4, robotIP, port)  # 击球，前击
                            time.sleep(1)
                            raiseStick(robotIP, port)
                            standWithStick5(0.1, robotIP, port)
                            MOTION.moveTo(0.55, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(0.55, 0, compensation_2, moveConfig2)
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 0, 12.5)
                            if not len(redBallInfo):
                                MOTION.moveTo(0, 0, -45 * math.pi / 180.0, moveConfig2)
                                redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 0, 12.5)
                                if not len(redBallInfo):
                                    MOTION.moveTo(0, 0, 45 * math.pi / 180.0, moveConfig2)
                                    time.sleep(0.5)
                                    MOTION.moveTo(0, 0, 45 * math.pi / 180.0, moveConfig2)
                                    redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 0, 12.5)
                            if len(redBallInfo):
                                MOTION.moveTo(redBallInfo[0] - 0.6, 0, compensation_2, moveConfig2)
                                MOTION.moveTo(0, 0, redBallInfo[1], moveConfig2)
                            else:
                                MOTION.moveTo(0.45, 0, compensation_2, moveConfig2)
                            # MOTION.moveTo(0, 0, redBallInfo[1], moveConfig2)
                            holeFlag = 0

                        # ----------------------------------------------------场地二、三下阶段第一次寻球--------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                        redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 0, 0)
                        if not len(redBallInfo):
                            MOTION.moveTo(0, 0, -30 * math.pi / 180.0, moveConfig2)
                            redBallInfo = opt.searchRedBall(moveConfig2, S1, V1, H1, H2, 0)
                            if not len(redBallInfo):
                                redBallInfo = opt.searchRedBall(moveConfig2, S1, V1, H1, H2, 0)
                                if not len(redBallInfo):
                                    TTS.say("第一次找球未成功，请重新开始！")
                                    exit()
                        MOTION.moveTo(0, 0, redBallInfo[1], moveConfig2)  # 转角对准红球
                        time.sleep(1)
                        if redBallInfo[0] >= 0.55:
                            MOTION.moveTo(redBallInfo[0] / 2, 0, compensation_2, moveConfig2)
                            MOTION.moveTo(redBallInfo[0] / 2 - 0.35, 0, compensation_2, moveConfig2)
                        else:
                            MOTION.moveTo(redBallInfo[0] - 0.35, 0, compensation_2, moveConfig2)

                        # ----------------------------------------------------场地二、三下阶段第二次寻球---------------------------------------------------------------

                        redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                        if not len(redBallInfo):
                            MOTION.moveTo(0, 0, 30 * math.pi / 180.0, moveConfig2)
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                        if not len(redBallInfo):
                            MOTION.moveTo(0, 0, -30 * math.pi / 180.0, moveConfig2)
                            MOTION.moveTo(0, 0, -30 * math.pi / 180.0, moveConfig2)
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                        if not len(redBallInfo):
                            TTS.say("第二次找球未成功，请重新开始！")
                            exit()
                        MOTION.moveTo(0, 0, redBallInfo[1], moveConfig2)
                        time.sleep(1)
                        MOTION.moveTo(redBallInfo[0] - 0.32, 0, compensation_2, moveConfig2)
                        # TTS.say("距离35")

                        # ----------------------------------------------------第一次三点一线、黄杆识别----------------------------------------------------------------
                        stickInfo = alldet.yellowStickDetection(minH, minS, minV, maxH, 0)
                        while len(stickInfo) == 0:
                            opt.redBallReference(moveConfig2, S1, V1, H1, H2)
                            stickInfo = alldet.yellowStickDetection(minH, minS, minV, maxH, 0)
                        redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                        if len(stickInfo):
                            theta = opt.threePointsAndOneLine(-0.30, 0.0, compensation_2, redBallInfo,
                                                              stickInfo, moveConfig2)

                            # ---------------------------------------------------------第二次三点一线------------------------------------------------------------

                            stickInfo = alldet.yellowStickDetection(minH, minS, minV, maxH, 0)
                            while len(stickInfo) == 0:
                                opt.redBallReference(moveConfig2, S1, V1, H1, H2)
                                stickInfo = alldet.yellowStickDetection(minH, minS, minV, maxH, 0)
                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            a = 1
                            while (abs(theta) >= 5 * math.pi / 180):
                                a += 1
                                theta = opt.threePointsAndOneLine(-0.29 + a * 0.02, 0.0, compensation_3, redBallInfo,
                                                                  stickInfo, moveConfig3)
                                if (a > 2):
                                    break
                                redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                                stickInfo = alldet.yellowStickDetection(minH, minS, minV, maxH, 0)

                            # -------------------------------------------------------场地二、三后阶段击球------------------------------------------------------

                            redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            # MOTION.moveTo(0, 0.05, 0.0, moveConfig3)
                            MOTION.moveTo(0.0, 0.0, redBallInfo[1], moveConfig2)
                            MOTION.moveTo(redBallInfo[0] - 0.14, 0, compensation_2, moveConfig2)  # 0.15
                            # redBallInfo = alldet.redBallDetection(moveConfig2, S1, V1, H1, H2, 'all', 12.5)
                            # MOTION.moveTo(0.0, 0.0, redBallInfo[1], moveConfig3)
                            MOTION.moveTo(0, 0.05, 0.0, moveConfig2)
                            MOTION.moveTo(0, 0.0, 2 * math.pi / 180.0, moveConfig2)
                            hitBallqian(HitBallSpeed_SecondHole_Num_2, robotIP, port)  # 击球，前击
                            time.sleep(8)
                            catchStick(robotIP, port)
                            holeFlag = 0
                            break
                            # 最开始在障碍物旁边识别红球成功的话执行下面的程序
                    global holeFlag
                    holeFlag = 0
                    break
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)


class Golf(ALModule):
    def __init__(self, name, robotIP, port):
        ALModule.__init__(self, name)
        self.robotIP = robotIP
        self.port = port

        self.memory = ALProxy("ALMemory")
        self.motion = ALProxy("ALMotion")
        self.posture = ALProxy("ALRobotPosture")

        self.memory.subscribeToEvent("ALChestButton/TripleClickOccurred", "myGolf", "chestButtonPressed")
        self.memory.subscribeToEvent("FrontTactilTouched", "myGolf", "frontTactilTouched")
        self.memory.subscribeToEvent("MiddleTactilTouched", "myGolf", "middleTactilTouched")
        self.memory.subscribeToEvent("RearTactilTouched", "myGolf", "rearTactilTouched")
        self.memory.subscribeToEvent("robotHasFallen", "myGolf", "fallDownDetected")

    def frontTactilTouched(self):
        print "frontTactilTouched!!!!!!!!!!!!!TactileHeadBack"
        self.memory.unsubscribeToEvent("FrontTactilTouched", "myGolf")
        global holeFlag
        holeFlag = 1
        self.memory.subscribeToEvent("FrontTactilTouched", "myGolf", "frontTactilTouched")

    def middleTactilTouched(self):
        print "middleTactilTouched!!!!!!!!!!!!!!!!!!"
        self.memory.unsubscribeToEvent("MiddleTactilTouched", "myGolf")
        global holeFlag
        holeFlag = 2
        self.memory.subscribeToEvent("MiddleTactilTouched", "myGolf", "middleTactilTouched")

    def rearTactilTouched(self):
        print "rearTactilTouched!!!!!!!!!!!!!!!!!!"
        self.memory.unsubscribeToEvent("RearTactilTouched", "myGolf")
        global holeFlag
        holeFlag = 3
        self.memory.subscribeToEvent("RearTactilTouched", "myGolf", "rearTactilTouched")

    def chestButtonPressed(self):
        print "chestButtonPressed!!!!!!!!!!!!!!!!"
        self.memory.unsubscribeToEvent("ALChestButton/TripleClickOccurred", "myGolf")
        global holeFlag
        holeFlag = 0
        self.motion.angleInterpolationWithSpeed("LHand", 1, 1)
        self.motion.angleInterpolationWithSpeed("RHand", 1, 1)
        time.sleep(3)
        self.motion.angleInterpolationWithSpeed("LHand", 0.2, 1)
        self.motion.angleInterpolationWithSpeed("RHand", 0.2, 1)
        self.motion.rest()
        self.memory.subscribeToEvent("ALChestButton/TripleClickOccurred", "myGolf", "chestButtonPressed")

    def fallDownDetected(self):
        print "fallDownDetected!!!!!!!!!!!!!!!!"
        self.memory.unsubscribeToEvent("robotHasFallen", "myGolf")
        global robotHasFallenFlag
        robotHasFallenFlag = 1
        self.posture.goToPosture("StandInit", 0.5)
        releaseStick(self.robotIP, self.port)
        time.sleep(5)
        catchStick(self.robotIP, self.port)
        raiseStick(self.robotIP, self.port)
        standWithStick5(0.1, self.robotIP, self.port)
        self.memory.subscribeToEvent("robotHasFallen", "myGolf", "fallDownDetected")


# ---------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="169.254.228.115",
                        help="Robot ip address.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number.")
    args = parser.parse_args()
    #
    moveConfig1 = [["MaxStepX", 0.025],
                   ["MaxStepY", 0.11],
                   ["MaxStepTheta", 0.3],
                   ["MaxStepFrequency", 0.055],
                   ["StepHeight", 0.015],
                   ["TorsoWx", 0],
                   ["TorsoWy", 0]]

    moveConfig2 = [["MaxStepX", 0.05],
                   ["MaxStepY", 0.22],
                   ["MaxStepTheta", 0.3],
                   ["MaxStepFrequency", 0.45],
                   ["StepHeight", 0.02],
                   ["TorsoWx", 0],
                   ["TorsoWy", 0]]

    moveConfig3 = [["MaxStepX", 0.035],
                   ["MaxStepY", 0.11],
                   ["MaxStepTheta", 0.4],
                   ["MaxStepFrequency", 0.50],
                   ["StepHeight", 0.02],
                   ["TorsoWx", 0],
                   ["TorsoWy", 0]]

    robotIP = args.ip
    port = args.port

    main(robotIP, 9559)
