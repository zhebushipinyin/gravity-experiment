#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from psychopy import visual, core, event, clock, monitors, iohub
from generate_data import *
from target import *


w, h = (3200, 1800)  # 显示器像素
distance = 50
width = 29.3
height = width * h / w
mon = monitors.Monitor(
    name='my_monitor',
    width=width,
    distance=distance,  # 被试距显示器距离，单位cm
    gamma=1,  # gamma值
    verbose=False)  # 是否输出详细信息
# mon.setSizePix((3200, 1800))  # 设置显示器分辨率
mon.setSizePix((w, h))  # 设置显示器分辨率
mon.save()  # 保存显示器信息

win = visual.Window(size=(w, h), fullscr=True, color=[0, 0, 0], monitor=mon)

start_pos = np.array([-1500, 800])
golf = visual.Circle(win, lineWidth=1, radius=20, fillColor=[-1, -1, -1], lineColor=[0.5, 0.5, 0.5])
golf.pos = start_pos

clk = clock.Clock()
clk.reset()

while golf.pos[1] > -800:
    t = clk.getTime()
    golf.pos = get_xy(t, v=1, g=9.8, scale=800, pos_start=start_pos)
    golf.draw()
    win.flip()


win.flip()
core.wait(2)
win.close()
core.quit()