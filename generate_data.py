#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def generate(ball_d=0.05715, height=[0.4, 0.8, 1.2, 1.6], v=[1, 1.7, 2.4], ori=['left', 'right'], start_x=[2, 1.7],
             repeat=2, unit='m'):
    """
    生成实验的数据
    :param ball_d: 刺激直径，m
    :param height: 下落高度, m
    :param v: 水平运动速度, m/s
    :param ori: 运动方向
    :param start_x: 初始距离, m
    :param repeat: 每种条件重复次数
    :param unit: 单位, 'm'
    return: DataFrame
    """
    df = pd.DataFrame()
    n = len(height) * len(v) * len(ori) * len(start_x) * repeat
    df['height'] = height * len(v) * len(ori) * len(start_x) * repeat
    v_ = v * len(height)
    v_.sort()
    df['v'] = v_ * len(ori) * len(start_x) * repeat
    ori_ = ori * len(v) * len(height)
    ori_.sort()
    df['ori'] = ori_ * len(start_x) * repeat
    start_ = start_x * len(height) * len(v) * len(ori)
    start_.sort()
    df['start_x'] = start_ * repeat
    df['ball_d'] = ball_d
    df['g'] = 9.8
    df['unit'] = unit
    df['s_expect'] = df.v * np.sqrt(2 * df.height / df.g)
    df = df.sample(frac=1)
    df.index = range(len(df))
    return df


def generate_train(ball_d=0.05715, height=[0.5, 1], v=[1.5, 2], ori=['left', 'right'], start_x=[2, 1.7]
                   , repeat=1, unit='m'):
    """
    生成实验的数据
    :param ball_d: 刺激直径，m
    :param height: 下落高度, m
    :param v: 水平运动速度, m/s
    :param ori: 运动方向
    :param start_x: 初始距离, m
    :param repeat: 每种条件重复次数
    :param unit: 单位, 'm'
    return: DataFrame
    """
    df = pd.DataFrame()
    n = len(height) * len(v) * len(ori) * repeat
    df['height'] = height * len(v) * len(ori) * repeat
    v_ = v * len(height)
    v_.sort()
    df['v'] = v_ * len(ori) * repeat
    ori_ = ori * len(v) * len(height)
    ori_.sort()
    df['ori'] = ori_ * repeat
    df['s0'] = np.random.randint(0, 2, len(df))
    df['ball_d'] = ball_d
    df['g'] = 9.8
    df['unit'] = unit
    df['s_expect'] = df.v * np.sqrt(2 * df.height / df.g)
    df['start_x'] = start_x*len(height) * len(v) * repeat
    df = df.sample(frac=1)
    df.index = range(len(df))
    return df


if __name__ == '__main__':
    df = generate()
    df.to_csv('trial.csv')
