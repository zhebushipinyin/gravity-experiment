#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def get_xy(t, v=1, g=9.8, scale=1, pos_start=(0, 0)):
    """
    计算抛物运动的座标
    :param t: 运动时间
    :param v: 水平方向速度
    :param g: 重力加速度
    :param scale: 画面缩放尺度
    :param pos_start: 初始点，(x, y)
    :return: 直角坐标(x, y)
    """
    x0, y0 = pos_start
    sx = v*t
    sy = 0.5*g*t**2
    return sx*scale+x0, sy*scale+y0

