# -*- coding: utf-8 -*-

"""
@Time    : 2019/9/19 16:09
@User    : HouYushan
@Author  : xueba1521
@FileName: D_data1.py
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
# 删除无经纬度信息
df = df[df['经度'] != 0]
df = df[df['纬度'] != 0]


i = 0
j = 0
startnum = 0
df_list = []
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
            df1 = df[j:i]
            df_list.append(df1)
            print(len(df_list))
            # df1.to_csv('./data/data1/{}_{}.csv'.format(j, i))
            j = i + 1
        i = i + 1

df_list_new = []

for df_one in df_list:
    print(df_one)
    print('df_one', type(df_one))
    startnum1 = 0
    endnum1 = 0
    gpsv0_sum = 0
    tp_num = []
    v = []
    start_index = 0
    start_v = 0
    v_list = [0]
    start_time = 0
    time_list = []
    little_index = []
    for index, df_one_i in df_one.iterrows():
        # print(type(df_one_i))
        # print(df_one_i)

        print(df_one_i['GPS车速'])
        '''车加速度异常'''
        if df_one_i['GPS车速'] != 0:
            if df_one_i['GPS车速'] > start_v:
                v_list.append(df_one_i['GPS车速'])
                time_list.append(df_one_i['时间'])
                index = df_one_i.index
                little_index.append(index)
                start_v = df_one_i['GPS车速']
            else:
                v_list = []
                time_list = []
                little_index = []
            if df_one_i['GPS车速'] < start_v:
                v_list.append(df_one_i['GPS车速'])
                time_list.append(df_one_i['时间'])
                index = df_one_i.index
                little_index.append(index)
                if (start_v - df_one_i['GPS车速']) * 1000 / 3600 > 8 or (start_v - df_one_i['GPS车速']) * 1000 / 3600 < 7.5:
                    df_one.drop(df_one.index[index]).tail()
                start_v = df_one_i['GPS车速']

            else:
                v_list = []
                time_list = []
                little_index = []

            # 判断加速度
            try:
                if v_list[-1] > 100 :
                    if time_list[-1] - time_list[0] < 7:
                        df_one.drop(df_one.index[little_index[0] : little_index[-1]]).tail()

                # for v in v_list:
            except:
                pass


        else:
            v_list = []
            time_list = []
            little_index = []


        '''怠速'''
        if df_one_i['GPS车速'] <10.0 :
            v.append(0)
            print(v)
        if df_one_i['GPS车速'] >= 10.0:
            print('车速小于10长度', len(v))
            if len(v) > 180:
                tp_num.append((start_index, index))
                start_index = index
            if len(v) <= 180:
                start_index = index
            v = []
        # try:
        #     if df_one_i['GPS车速'] == 0.0 :
        #         gpsv0_sum += 1
        #         endnum1 += 1
        #     elif df_one_i['GPS车速'] != 0.0:
        #         if gpsv0_sum > 180:
        #             tp_num.append((startnum1, endnum1))
        #             startnum1 = endnum1
        #         else:
        #             endnum1 += 1
        #             startnum1 = endnum1
        #         gpsv0_sum = 0
        # except:
        #     print('err', df_one_i)
        #     pass
    print(tp_num)
    if tp_num != []:
        if len(df_one[0: tp_num[0][0]]) > 1:
            df_list_new.append(df_one[0: tp_num[0][0]])
        try:
            for i in range(len(tp_num)):
                df_list_new.append(df_one[tp_num[i][1] : tp_num[i+1][0]])
        except:
            pass
        if len(df_one[0: tp_num[-1][1]]) > 1:
            df_list_new.append(df_one[0: tp_num[-1][1]])
print('df_list_new----',df_list_new)

