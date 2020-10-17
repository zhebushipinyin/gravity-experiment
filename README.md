# gravity-experiment
太空实验， 测量重力，试验任务为抛物运动，根据被试反应反推主观重力

实验为3(速度)*4(高度)*2(方向)*2(初始位置)*2(重复)的实验

数据格式：\
ball_d: 刺激直径，m\
height: 下落高度, m\
v: 水平运动速度, m/s\
ori: 运动方向\
start_x: 初始距离, m\
repeat: 每种条件重复次数 \
pix_w, pix_h: 屏幕像素 \
scale: 尺度，1米代表的像素量，默认为pix_w/4，即屏幕宽代表4m\
s_expect: 理论移动距离\
h0: 地面高度，单位像素\
s: 被试估计位置, m\
points: 得分\
est: 估计值, |s|\
g_inv: 推测重力 m/s^2




