# -*- coding: utf-8 -*-

"""
@Time    : 2019/9/21 11:58
@User    : HouYushan
@Author  : xueba1521
@FileName: D_data3.py
@Software: PyCharm
@Blog    ：http://---
"""
import pandas as pd

new_df = pd.DataFrame(columns= ['平均速度', '平均行驶速度', '平均加速度', '平均减速度', '怠速时间比',
                                '加速时间比', '减速时间比', '速度标准差', '加速度标准差'])

df = pd.read_excel('./data/result_df/7.xls')
print(df)
# 平均速度 km/h
p_v = sum(df['GPS车速']) / len(df)
# 平均行驶速度 km/h
p_s_v = sum(df[df['GPS车速'] > 0]['GPS车速']) / len(df[df['GPS车速'] > 0])

n_up = 0
n_up_sum = 0
n_down = 0
n_down_sum = 0

n_0 = 0
n_0_sum = 0
s = []
for i in df['GPS车速'].diff():
    s.append(i)
print(s)
for i in df['GPS车速'].diff():
    if i > 0.1 :
        n_up += 1
        n_up_sum += i
    if i < -0.1:
        n_down += 1
        n_down_sum += i
    if -0.1 <= i <= 0.1:
        n_0 += 1
        n_0_sum += i
# 平均加速度 m/s
p_up_a = (n_up_sum * 1000 / 3600) / n_up
# 平均减速度 m/s
p_down_a = (n_down_sum * 1000 / 3600) / n_down

# 怠速时间比 %
d_t_b = (len(df[df['GPS车速'] == 0]) / len(df) ) * 100

# 加速时间比 %
up_t_b = (n_up / len(df)) * 100

# 减速时间比 %
down_t_b = (n_down / len(df)) * 100


# 速度标准差 km/h
v_std = df['GPS车速'].std(ddof=0)

# 加速度标准差 m/s
a_std = (df['GPS车速'].diff()).std(ddof=0)

'''匀速时间比'''
# y_t_b = (n_0 / len(df)) * 100
# y_t_b = y_t_b - d_t_b
y_t_b = (100- d_t_b - up_t_b - down_t_b)

'''持续时间'''
c_t = len(df)
'''最大速度'''
max_v = df['GPS车速'].max()
'''行驶距离'''
s_l = sum(df[df['GPS车速'] > 0]['GPS车速'])


print(p_v, p_s_v, p_up_a, p_down_a ,d_t_b, up_t_b, down_t_b, y_t_b, v_std, a_std, y_t_b, c_t, max_v, s_l)
dict = {'平均速度':p_v, '平均行驶速度':p_s_v, '平均加速度':p_up_a, '平均减速度':p_down_a, '怠速时间比':d_t_b,
                                '加速时间比':up_t_b, '减速时间比':down_t_b, '速度标准差':v_std, '加速度标准差':a_std,
        '匀速时间比':y_t_b, '持续时间':c_t,'最大速度':max_v, '行驶距离':s_l  }
new_df = new_df.append(pd.DataFrame.from_dict(dict, orient='index').T)
print(new_df)
new_df.to_excel('./data/result_df/7_result.xls')