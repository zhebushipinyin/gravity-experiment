#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from psychopy import visual, event, core
from target import *


def run_trial(i, win, df, clk, golf, net, table, ok_shape, scale=800, h0=-600):
    """
    执行抛物运动实验
    :param i: 试次编号
    :param win: 窗口，psychopy visual.Window对象
    :param df: dataFrame, 实验trial表格
    :param clk: 时钟，psychopy clock对象
    :param golf: 运动对象，visual.Circle()
    :param net: 捕捉网，visual.Rect()
    :param table: 桌子&地面，visual.ShapeStim()
    :param ok_shape: 确认键，visual.Rect()
    :param scale: 像素与米之间的关系，在3200*1800分辨率下，1m=800像素
    :param h0: 地面高度，单位像素
    :return: 返回
    """
    w, h = win.size
    hy = df.height[i] * scale
    size_r = df.golf_d[i] * scale / 2
    s_expect = df.s_expect[i] * scale
    v = df.v[i]
    if df.ori[i] == 'right':
        ori = 1
    else:
        ori = -1
    s0 = df.s0[i] * ori * w / 2
    start_pos = (-w*ori / 2, hy + h0 + size_r)
    golf.pos = start_pos
    net.pos = (s0, h0)
    ok_shape.pos = (-w * ori / 4, h0)
    vertices = ((-w*ori / 2, -h / 2), (-w*ori / 2, hy + h0), (0, hy + h0), (0, h0), (w*ori / 2, h0), (w*ori / 2, -h / 2))
    table.vertices = vertices

    myMouse = event.Mouse()
    state = 'move'
    clk.reset()  # 初始时钟

    while True:
        # 初始状态
        if state == 'move':
            t1 = clk.getTime()
            golf.pos = get_x(t1, v=v, scale=scale, pos_start=start_pos,ori=ori)
            table.draw()
            golf.draw()
            win.flip()
            if (abs(golf.pos[0])<1) or (ori*golf.pos[0]>0):
                state = 'estimate'
                clk.reset()

        elif state == 'estimate':
            table.draw()
            golf.draw()
            net.draw()
            ok_shape.draw()
            win.flip()
            if (myMouse.getPressed()[0]) & (myMouse.getPos()[0] * ori > 0):
                net.pos = (myMouse.getPos()[0], h0)
            if myMouse.isPressedIn(ok_shape):
                rt = clk.getTime()
                state = 'quit'
                s = net.pos[0]
        # 结束本试次
        elif state == 'quit':
            point = abs(s_expect - s)
            break
    return rt, s, point
