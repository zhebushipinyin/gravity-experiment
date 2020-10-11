#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from psychopy import visual, core, event, clock, monitors, iohub, gui
from generate_data import *
from target import *


# GUI
myDlg = gui.Dlg(title=u"实验")
myDlg.addText(u'被试信息')
myDlg.addField('name:')
myDlg.addField('sex:', choices=['male', 'female'])
myDlg.addField('age:', 21)
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if not myDlg.OK:
    core.quit()
name = ok_data[0]
sex = ok_data[1]
age = ok_data[2]

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

win = visual.Window(size=(w, h), fullscr=True, units='pix', color=[0, 0, 0], monitor=mon)

scale = 800
v = [1, 2, 3]
hy = [480, 880, 1280]
h0 = -600
x0, y0 = (0, 600)
golf_d = 0.0525
size_r = golf_d*scale/2

start_pos = (-w/2, hy[2]+h0+size_r)
golf = visual.Circle(win, lineWidth=0, radius=size_r, fillColor='red')
golf.pos = start_pos
net = visual.Rect(win, width=size_r*2, height=size_r/5, fillColor='green', lineColor='green')
net.pos = (w/4, h0)
ok_shape = visual.Rect(win, width=100, height=60, pos=(-w/4, h0), fillColor=[1, 1, 1])
table = visual.ShapeStim(win, vertices=((-w/2, -h/2), (-w/2, hy[2]+h0), (0, hy[2]+h0), (0, h0), (w/2, h0), (w/2, -h/2))
                         , fillColor=[-1, -1, -1], lineColor=[-1, -1, -1])
golf.draw()
table.draw()
win.flip()

clk = clock.Clock()
clk.reset()

while abs(golf.pos[0])>1 and golf.pos[0]<0:
    t1 = clk.getTime()
    golf.pos = get_x(t1, v=1, scale=800, pos_start=start_pos)
    golf.draw()
    table.draw()
    win.flip()

drop_pos = golf.pos.copy()
clk.reset()

myMouse = event.Mouse()
while True:
    if (myMouse.getPressed()[0])&(myMouse.getPos()[0]>0):
        net.pos = (myMouse.getPos()[0], -600)
    golf.draw()
    table.draw()
    net.draw()
    ok_shape.draw()
    win.flip()
    if myMouse.isPressedIn(ok_shape):
        break
clk.reset()
while golf.pos[1] > -800:
    t = clk.getTime()
    golf.pos = get_xy(t, v=1, g=9.8, scale=800, pos_start=drop_pos)
    golf.draw()
    golf.pos = get_xy(t, v=0.5, g=9.8, scale=800, pos_start=drop_pos)
    golf.draw()
    golf.pos = get_xy(t, v=2, g=9.8, scale=800, pos_start=drop_pos)
    golf.draw()
    golf.pos = get_xy(t, v=3, g=9.8, scale=800, pos_start=drop_pos)
    golf.draw()
table.draw()
win.flip()

all_point = np.clip(30, 10, 100)
visual.TextStim(win, text='本次实验结束，双击屏幕或点击鼠标退出', pos=(-w/4, 0), height=h/32).draw()
visual.TextStim(win, text='您本试实验得分为：%s/100分' % all_point, pos=(-w/4, h/6), height=h/15).draw()
win.flip()

while sum(myMouse.getPressed(getTime=True)[0]) == 0:
    continue
win.close()
core.quit()