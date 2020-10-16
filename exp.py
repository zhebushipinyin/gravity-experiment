#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from psychopy import visual, core, event, clock, monitors, gui
from generate_data import *
from trial_func import *


# GUI
myDlg = gui.Dlg(title=u"实验")
myDlg.addText(u'被试信息')
myDlg.addField('姓名:')
myDlg.addField('性别:', choices=['male', 'female'])
myDlg.addField('年龄:', 21)
myDlg.addField('第几次实验:')
myDlg.addField('屏幕分辨率:', choices=['1920*1080', '3200*1800', '1280*720', '2048*1152'])
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if not myDlg.OK:
    core.quit()
name = ok_data[0]
sex = ok_data[1]
age = ok_data[2]
exp_num = ok_data[3]
resolution = ok_data[4]
w, h = resolution.split('*')
w = int(w)
h = int(h)
# w, h = (1920, 1080)  # 显示器像素
# w, h = (3200, 1800)  # 显示器像素
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


ball_d = 0.05715
# height = [0.6, 1.1, 1.6]
# v = [1, 2, 3]
height = [0.4, 0.8, 1.2, 1.6]
v = [1, 1.7, 2.4]
start_x = [2, 1.7]
ori = ['left', 'right']
repeat = 2
# 生成trial
df = generate(ball_d=ball_d, height=height, v=v, ori=ori, start_x=start_x, repeat=repeat, unit='m')
df_tr = generate_train(ball_d=ball_d)
df['pix_w'] = w
df['pix_h'] = h
scale = w*800/3200
df['scale'] = scale
df_tr['scale'] = scale
h0 = -h/3
df['h0'] = h0
size_r = ball_d*scale/2
df.to_csv('trial.csv')
df_tr.to_csv('train.csv')

result = {'id': [], 'rt': [], 's': [], 'points': [], 'click_num':[]}
result_tr = {'id': [], 'rt': [], 's': [], 'points': []}
click_log = {
    'id': [],
    'click_pos': [],
    'click_time': []
}
win = visual.Window(size=(w, h), fullscr=True, units='pix', color=[0, 0, 0], monitor=mon)

fix = visual.ImageStim(win, pos=(0, 0), image='icon/fix.png')

ball = visual.Circle(win, lineWidth=0, radius=size_r, fillColor='white')
net = visual.Rect(win, width=size_r*4, height=size_r/5, fillColor='white', lineColor='white')
# ok_shape = visual.Rect(win, width=w/30, height=h/32, fillColor=[0, 0, 0], lineWidth=0)
table = visual.ShapeStim(win, fillColor=[-0.5, -0.5, -0.5], lineColor=[-0.5, -0.5, -0.5])
# ok = visual.TextStim(win, text=u"确认", height=h/40, color='white')
cat0 = visual.ImageStim(win, size=(0.48*scale, 0.42*scale), image='icon/Cats0.png')
cat1 = visual.ImageStim(win, size=(0.48*scale, 0.42*scale), image='icon/Cats.png')

myMouse = event.Mouse()
# 指导语
pic = visual.ImageStim(win, size=(w, h))
# 指导语
for i in range(3):
    pic.image = 'pic/指导语%s.png'%(i+1)
    pic.draw()
    win.flip()
    core.wait(1)
    while sum(myMouse.getPressed(getTime=True)[0]) == 0:
        continue
    event.clearEvents()
event.clearEvents()
visual.TextStim(win, bold=True, text='点击鼠标开始练习', height=h/32, color='white').draw()
win.flip()
core.wait(1)
while sum(myMouse.getPressed(getTime=True)[0]) == 0:
    continue
event.clearEvents()
# 练习
clk = clock.Clock()
clk.reset()
for i in range(len(df_tr)):
    win.flip()
    rt, s, points, _ = run_trial(i, win, df_tr, clk, ball, net, table, cat0, cat1, scale=scale, h0=h0)
    result_tr['id'].append(i)
    result_tr['rt'].append(rt)
    result_tr['s'].append(s)
    result_tr['points'].append(points)
    win.flip()
    key = event.waitKeys(maxWait=0.2, keyList=['escape'])
    if key:
        core.wait(0.2)
        win.close()
        core.quit()
    event.clearEvents()
df_tr['id'] = result_tr['id']
df_tr['rt'] = result_tr['rt']
df_tr['s'] = result_tr['s']
df_tr['points'] = result_tr['points']
df_tr['name'] = [name]*len(df_tr)
df_tr['sex'] = [sex]*len(df_tr)
df_tr['age'] = [age]*len(df_tr)
df_tr['distance'] = [distance]*len(df_tr)
df_tr['date'] = time.strftime("%y/%m/%d")
df_tr.to_csv('exp_data\\train\\%s_train_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))

visual.TextStim(win, bold=True, text='练习结束，点击鼠标开始实验', height=h/32, color='white').draw()
win.flip()
while sum(myMouse.getPressed(getTime=True)[0]) == 0:
    continue
# 实验
clk.reset()
for i in range(len(df)):
    print(i)
    if i == len(df)//2:
        visual.TextStim(win, text='请休息一下，双击屏幕或点击鼠标继续', pos=(0, 0), height=h/32).draw()
        win.flip()
        core.wait(2)
        while sum(myMouse.getPressed(getTime=True)[0]) == 0:
            continue
    rt, s, points, click = run_trial(i, win, df, clk, ball, net, table, cat0, cat1, scale=scale, h0=h0)
    result['id'].append(i)
    result['rt'].append(rt)
    result['s'].append(s)
    result['points'].append(points)
    result['click_num'].append(click['click_num'])
    click_log['click_time'] += click['click_time']
    click_log['click_pos'] += click['click_pos']
    click_log['id'] += [i]*len(click['click_pos'])

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
df['exp_num'] = [exp_num]*len(df)
df['distance'] = [distance]*len(df)
df['est'] = abs(df.s)
df['g_inv'] = 2*df.height*df.v**2/df.est**2
df['date'] = time.strftime("%y/%m/%d")
df.to_csv('exp_data\\data\\%s_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))

df_click_log = pd.DataFrame(click_log)
df_click_log['name'] = name
df_click_log['exp_num'] = exp_num
df_click_log.to_csv('exp_data\\click_log\\%s_ClickLog_%s.csv' % (name, time.strftime("%y-%m-%d-%H-%M")))
all_point = np.clip(np.round(df.points.sum()*100/len(df), 1), 10, 100)
visual.TextStim(win, text='本次实验结束，双击屏幕或点击鼠标退出', pos=(-w/4, 0), height=h/32).draw()
visual.TextStim(win, text='您本试实验得分为：%s/100分' % all_point, pos=(-w/4, h/6), height=h/15).draw()
win.flip()

while sum(myMouse.getPressed(getTime=True)[0]) == 0:
    continue
win.close()
core.quit()
