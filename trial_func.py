#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from psychopy import visual, event, core
from target import *


def run_trial(i, win, df, clk, ball, net, table, cat0, cat1, scale=800, h0=-600):
    """
    执行抛物运动实验
    :param i: 试次编号
    :param win: 窗口，psychopy visual.Window对象
    :param df: dataFrame, 实验trial表格
    :param clk: 时钟，psychopy clock对象
    :param ball: 运动对象，visual.Circle()
    :param net: 捕捉网，visual.Rect()
    :param table: 桌子&地面，visual.ShapeStim()
    :param cat0: 猫0，visual.Image()
    :param cat1: 猫1，visual.Image()
    :param scale: 像素与米之间的关系，在3200*1800分辨率下，1m=800像素
    :param h0: 地面高度，单位像素
    :return: 返回
    """
    w, h = win.size
    hy = df.height[i] * scale
    size_r = df.ball_d[i] * scale / 2
    s_expect = df.s_expect[i]
    start_x = df.start_x[i] * scale
    k = df.k[i]
    v = df.v[i]
    click = {
        'click_num': 0,
        'id': i,
        'click_time': [],
        'click_pos': []
    }
    if df.ori[i] == 'right':
        ori = 1
    else:
        ori = -1
    # s0 = df.s0[i] * ori * w / 2
    start_pos = (-start_x*ori, hy + h0 + size_r)
    ball.pos = start_pos
    # net.pos = (s0, h0)
    net.ori = -np.arctan(k)*ori*180/np.pi
    cat0.pos = (-start_x*ori, hy + h0 + 0.42*scale/2)
    cat1.pos = (-start_x*ori, hy + h0 + 0.42 * scale / 2)
    cat0.flipHoriz = (ori==-1)
    cat1.flipHoriz = (ori==-1)
    # ok_shape.pos = (-w * ori / 4, h0)
    # ok.pos = (-w * ori / 4, h0)
    vertices = ((-w*ori / 2, -h / 2), (-w*ori / 2, hy + h0), (0, hy + h0), (0, h0), (w*ori / 2, h0+w*k/2), (w*ori / 2, -h / 2))
    table.vertices = vertices
    myMouse = event.Mouse()
    myMouse.setVisible(False)
    vlow = min(0, w*ori / 2)
    vhigh = max(0, w*ori / 2)
    # 鼠标位置随机化，并限制在斜面上
    random_start = np.random.randint(vlow, vhigh)
    myMouse.setPos((random_start, 0))
    state = 'ready'
    clk.reset()  # 初始时钟
    event.clearEvents()
    response = 0
    colors = ['white', 'green', 'white']
    times = [0.1, 0.2, 0.2]
    ClickRt = 0
    while True:
        # 初始状态
        myMouse.setPos((myMouse.getPos()[0], h0+k*abs(myMouse.getPos()[0])))
        if state == 'ready':
            for ki in range(3):
                table.draw()
                ball.color = colors[ki]
                cat0.draw()
                ball.draw()
                win.flip()
                core.wait(times[ki])
            state = 'move'
        elif state == 'move':
            t1 = clk.getTime()
            ball.pos = get_x(t1, v=v, scale=scale, pos_start=start_pos, ori=ori)
            table.draw()
            cat1.draw()
            ball.draw()
            win.flip()
            if (abs(ball.pos[0]) < size_r) or (ori*ball.pos[0] > 0):
                ball.pos = (0, start_pos[1])
                state = 'estimate'
                table.draw()
                # ball.draw()
                cat1.draw()
                # net.draw()
                win.flip()
                clk.reset()
        elif state == 'estimate':
            if (myMouse.getPressed()[0]) & (myMouse.getPos()[0] * ori > 0):
                net.pos = (myMouse.getPos()[0], h0+k*abs(myMouse.getPos()[0]))
                if click['click_num'] == 0:
                    myMouse.setVisible(True)
                    ClickRt = clk.getTime()
                click['click_num'] += 1
                click['click_time'].append(clk.getTime())
                click['click_pos'].append(net.pos[0]/scale)
                response = 1
                table.draw()
                # ok_shape.draw()
                # ok.draw()
                # ball.draw()
                cat1.draw()
                net.draw()
                win.flip()
            key = event.getKeys(keyList=['space'], timeStamped=clk)
            if not key:
                pass
            elif ('space' in key[-1][0])&(response==1):
                rt = key[-1][1]
                # rt = clk.getTime()
                state = 'quit'
                s = net.pos[0]/scale
        # 结束本试次
        elif state == 'quit':
            point = 1 - abs(s_expect - abs(s))
            break
    return rt, s, point, click, ClickRt, random_start/scale
