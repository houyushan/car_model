# -*- coding: utf-8 -*-

"""
@Time    : 2019/9/19 10:30
@User    : HouYushan
@Author  : xueba1521
@FileName: D_data.py
@Software: PyCharm
@Blog    ：http://---
"""
import pandas as pd
import time
import xlwt


def forTime():
    data_1 = pd.read_excel('./data/1.xlsx')
    time1 = data_1['时间']
    print(time1[1])
    timeList = []
    for t in time1:
        t = t.replace('/', '-').split('.')[0]
        print('t',t)
        ts = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        time_new = time.mktime(ts)
        print(time_new)
        timeList.append(time_new)

    data_1['时间'] = timeList
    data_1.to_csv('./data/1_forTime.csv')


df = pd.read_csv('./data/1_forTime.csv')
startnum = 0
i = 0
for it in df['时间']:
    if i == 0:
        i = i + 1
        startnum = it
        pass
    else:
        if it - startnum == 1:
            # print('差一',i)
            startnum = it
        else:
            t = int(it - startnum)
            print('有跳跃：', i, t )
            startnum = it
            # if it - startnum < 180:
            insertRow = pd.DataFrame([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]],
                                     columns=['时间', 'GPS车速', 'X轴加速度', 'Y轴加速度', 'Z轴加速度', '经度', '纬度', '发动机转速', '扭矩百分比',
                                              '瞬时油耗', '油门踏板开度', '空燃比', '发动机负荷百分比', '进气流量'])
            print(t)
            for j in range(0, t):
                if j < 181:
                    print(j)
                    # insertRow = insertRow.append(insertRow)
                    # print(insertRow)
                    above = df.loc[:i]
                    below = df.loc[i+1:]
                    df = above.append(insertRow,ignore_index=True).append(below,ignore_index=True)
                    i = i + 1
                else:
                    pass
        i = i + 1
df.to_csv('./data/1_forTimefull2.csv')

# # 缺失值处理，插值替换
# def data_full():
#     df1 = pd.read_csv('./data/1_forTime.csv', index_col='i')
#     data_start = df1.iloc[0,0] #初始时间
#     df1_date = df1['时间'].tolist()  # 数据日期转为列表
#     df1_data = df1['value'].tolist()  # 数据值转为列表
#     act =


