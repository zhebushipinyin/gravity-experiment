#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from psychopy import visual, core, event, clock, monitors, gui
from generate_data import *
from trial_func import *


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
mon = monitors.Monitor(
    name='my_monitor',
    width=width,
    distance=distance,    # 被试距显示器距离，单位cm
    gamma=1,        # gamma值
    verbose=False)  # 是否输出详细信息
mon.setSizePix((w, h))  # 设置显示器分辨率
mon.save()  # 保存显示器信息


golf_d = 0.0525
height = [0.6, 1.1, 1.6]
v = [1, 2, 3]
ori = ['left', 'right']
repeat = 4
repeat_half = 2
# 生成trial
df = generate(golf_d=golf_d, height=height, v=v, ori=ori,  repeat=repeat, unit='m')
df['pix_w'] = w
df['pix_h'] = h
scale = 3200*800/w
df['scale'] = scale
h0 = -h/3
df['h0'] = h0
size_r = golf_d*scale/2
df.to_csv('trial.csv')

result = {'id':[], 'rt': [], 's': [], 'points': []}

win = visual.Window(size=(w, h), fullscr=True, units='pix', color=[0, 0, 0], monitor=mon)

fix = visual.ImageStim(win, pos=(0, 0), image='icon/fix.png')

golf = visual.Circle(win, lineWidth=0, radius=size_r, fillColor='red')
net = visual.Rect(win, width=size_r*2, height=size_r/5, fillColor='green', lineColor='green')
ok_shape = visual.Rect(win, width=w/32, height=h/32, fillColor=[1, 1, 1])
table = visual.ShapeStim(win, fillColor=[-1, -1, -1], lineColor=[-1, -1, -1])

ok = visual.TextStim(win, text=u"确认", pos=(10, -4), height=h/32, color='black')

myMouse = event.Mouse()

# 指导语
visual.TextStim(win, bold=True, text='双击屏幕或点击鼠标开始实验', height=h/32, color='white').draw()
win.flip()
while sum(myMouse.getPressed(getTime=True)[0]) == 0:
    continue
# 实验
clk = clock.Clock()
clk.reset()
for i in range(len(df)):
    print(i)
    if i == len(df)//2:
        visual.TextStim(win, text='请休息一下，双击屏幕或点击鼠标继续', pos=(0, 0)).draw()
        win.flip()
        while sum(myMouse.getPressed(getTime=True)[0]) == 0:
            continue
    win.flip()
    fix.draw()
    win.flip()
    core.wait(0.2)
    rt, s, points = run_trial(i, win, df, clk, golf, net, table, ok_shape, scale=scale, h0=h0)
    result['id'].append(i)
    result['rt'].append(rt)
    result['s'].append(s)
    result['points'].append(points)

    win.flip()
    key = event.waitKeys(maxWait=0.2, keyList=['escape'])
    if key:
        core.wait(0.2)
        win.close()
        core.quit()
    event.clearEvents()
df['id'] = result['id']
df['rt'] = result['rt']
df['s'] = result['s']
df['points'] = result['points']

df['name'] = [name]*len(df)
df['sex'] = [sex]*len(df)
df['age'] = [age]*len(df)
df['distance'] = [distance]*len(df)


df.to_csv('exp_data\\%s_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))
visual.TextStim(win, text='本次实验结束，双击屏幕或点击鼠标退出', pos=(0, 0)).draw()
win.flip()
while sum(myMouse.getPressed(getTime=True)[0]) == 0:
    continue
win.close()
core.quit()
