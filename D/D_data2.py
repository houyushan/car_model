# -*- coding: utf-8 -*-

"""
@Time    : 2019/9/20 15:00
@User    : HouYushan
@Author  : xueba1521
@FileName: D_data2.py
@Software: PyCharm
@Blog    ：http://---
"""
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties

'''画图'''
def get_drow(dff):
    fontP = FontProperties(fname=r"C:\\Windows\\Fonts\\SimHei.ttf")  # 设置字体
    fontP.set_size('small')

    x = dff['时间'].head(1000)
    y = dff['GPS车速'].head(1000)
    plt.title("时间-GPS车速", fontproperties=fontP)
    plt.xlabel("x 时间", fontproperties=fontP)
    plt.ylabel("y 车速", fontproperties=fontP)
    plt.plot(x, y)
    plt.show()
    # plt.savefig('./data/1.png', dip=200)
    # plt.draw()

'''求特征'''
def get_data(new_df, df):

    # df = pd.read_csv('./data/data1/0.csv')
    # print(df)


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
    for i in df['GPS车速'].diff():
        if i > 0.1:
            n_up += 1
            n_up_sum += i
        if i < -0.1:
            n_down += 1
            n_down_sum += i
        if -0.1 <=i <= 0.1:
            n_0 += 1
            n_0_sum += i
    # 平均加速度 m/s
    p_up_a = (n_up_sum * 1000 / 3600) / n_up
    # 平均减速度 m/s
    p_down_a = (n_down_sum * 1000 / 3600) / n_down

    # 怠速时间比 %
    d_t_b = (len(df[df['GPS车速'] == 0]) / (len(df)-1)) * 100

    # 加速时间比 %
    up_t_b = (n_up / (len(df)-1)) * 100

    # 减速时间比 %
    down_t_b = (n_down / (len(df)-1)) * 100

    # 速度标准差 km/h
    v_std = df['GPS车速'].std(ddof=0)

    # 加速度标准差 m/s
    a_std = (df['GPS车速'].diff()).std(ddof=0)

    '''匀速时间比'''
    # y_t_b = (n_0 / len(df)) * 100
    # y_t_b = y_t_b - d_t_b
    y_t_b = (100 - up_t_b - down_t_b - d_t_b)

    '''持续时间'''
    c_t = len(df)
    '''最大速度'''
    max_v = df['GPS车速'].max()
    '''行驶距离'''
    s_l = sum(df[df['GPS车速'] > 0]['GPS车速'])

    print(p_v, p_s_v, p_up_a, p_down_a, d_t_b, up_t_b, down_t_b, y_t_b, v_std, a_std, y_t_b, c_t, max_v, s_l)
    dict = {'平均速度': p_v, '平均行驶速度': p_s_v, '平均加速度': p_up_a, '平均减速度': p_down_a, '怠速时间比': d_t_b,
            '加速时间比': up_t_b, '减速时间比': down_t_b, '速度标准差': v_std, '加速度标准差': a_std,
            '匀速时间比': y_t_b, '持续时间': c_t, '最大速度': max_v, '行驶距离': s_l}
    new_df = new_df.append(pd.DataFrame.from_dict(dict, orient='index').T)
    return new_df
    # print(len(new_df))

df = pd.read_excel('./data/3.xlsx')
df['时间'] = df['时间'].apply(lambda x:x[:-5])
df['时间'] = pd.to_datetime(df['时间'])

# 时间序列填充
helper = pd.DataFrame({'时间':pd.date_range(df['时间'].min(),df['时间'].max(), freq='s')})
# print(helper)
df = pd.merge(df, helper, on='时间', how='outer').sort_values('时间')

# 插值
'''X轴加速度	Y轴加速度	Z轴加速度	经度	纬度	发动机转速	扭矩百分比	瞬时油耗	油门踏板开度	空燃比	发动机负荷百分比	进气流量
'''
df['GPS车速'] = df['GPS车速'].interpolate(method='linear')
df['X轴加速度'] = df['X轴加速度'].interpolate(method='linear')
df['Y轴加速度'] = df['Y轴加速度'].interpolate(method='linear')
df['Z轴加速度'] = df['Z轴加速度'].interpolate(method='linear')
df['经度'] = df['经度'].interpolate(method='linear')
df['纬度'] = df['纬度'].interpolate(method='linear')
df['发动机转速'] = df['发动机转速'].interpolate(method='linear')
df['扭矩百分比'] = df['扭矩百分比'].interpolate(method='linear')
df['瞬时油耗'] = df['瞬时油耗'].interpolate(method='linear')
# df['油门踏板开度'] = df['油门踏板开度'].interpolate(method='linear')
# df['空燃比'] = df['空燃比'].interpolate(method='linear')
# df['发动机负荷百分比'] = df['发动机负荷百分比'].interpolate(method='linear')
# df['进气流量'] = df['进气流量'].interpolate(method='linear')

# print(df) # [518137 rows x 14 columns]
# df = df[df['经度'] != 0]
# df = df[df['纬度'] != 0]

# get_drow(df[440:480])
# df[440:480].to_excel('./data/440-480_new.xls')
# print(input('hahah'))

# 计算斜率 加速度
df = df[(df['GPS车速'].diff() * 1000 / 3600) < ((100 * 1000 / 3600) / 7)] # [518106 rows x 14 columns]
df = df[( -8.0 < (df['GPS车速'].diff() * 1000 / 3600) ) & ( (df['GPS车速'].diff() * 1000 / 3600) < -7.5) | ( (df['GPS车速'].diff() * 1000 / 3600) >= 0)] # [424601 rows x 14 columns]

helper = pd.DataFrame({'时间':pd.date_range(df['时间'].min(),df['时间'].max(), freq='s')})
# print(helper)
df = pd.merge(df, helper, on='时间', how='outer').sort_values('时间')


# 插值
'''X轴加速度	Y轴加速度	Z轴加速度	经度	纬度	发动机转速	扭矩百分比	瞬时油耗	油门踏板开度	空燃比	发动机负荷百分比	进气流量
'''
df['GPS车速'] = df['GPS车速'].interpolate(method='linear')
df['X轴加速度'] = df['X轴加速度'].interpolate(method='linear')
df['Y轴加速度'] = df['Y轴加速度'].interpolate(method='linear')
df['Z轴加速度'] = df['Z轴加速度'].interpolate(method='linear')
df['经度'] = df['经度'].interpolate(method='linear')
df['纬度'] = df['纬度'].interpolate(method='linear')
df['发动机转速'] = df['发动机转速'].interpolate(method='linear')
df['扭矩百分比'] = df['扭矩百分比'].interpolate(method='linear')
df['瞬时油耗'] = df['瞬时油耗'].interpolate(method='linear')
# df['油门踏板开度'] = df['油门踏板开度'].interpolate(method='linear')
# df['空燃比'] = df['空燃比'].interpolate(method='linear')
# df['发动机负荷百分比'] = df['发动机负荷百分比'].interpolate(method='linear')
# df['进气流量'] = df['进气流量'].interpolate(method='linear')

print(df) # [518135 rows x 14 columns]   [518277 rows x 14 columns] [431782 rows x 14 columns]
# df.to_csv('./data/2019921data1.csv')



'''画图'''
# from matplotlib import pyplot as plt
# from matplotlib.font_manager import FontProperties
#
# fontP = FontProperties(fname=r"C:\\Windows\\Fonts\\SimHei.ttf") # 设置字体
# fontP.set_size('small')
#
# x = df['时间'].head(1000)
# y = df['GPS车速'].head(1000)
# plt.title("时间-GPS车速", fontproperties=fontP)
# plt.xlabel("x 时间", fontproperties=fontP)
# plt.ylabel("y 车速", fontproperties=fontP)
# plt.plot(x, y)
# plt.show()
# plt.savefig('./data/1.png', dip=200)
# plt.draw()

'''怠速'''
df1 = df.reset_index(drop=True)
# print('----------------------------------',df1['GPS车速'].argmax())
# print(max(df1['GPS车速']))
# print(df1)
v = []
tp_num = []
start_index = 0
for index, df_one_i in df1.iterrows():
    if df_one_i['GPS车速'] < 10.0:
        v.append(0)
        # print(v)
    if df_one_i['GPS车速'] >= 10.0:
        # print('车速小于10长度', len(v))
        if len(v) > 180:
            tp_num.append((start_index, index))
            start_index = index
        if len(v) <= 180:
            start_index = index
        v = []

    if df_one_i['GPS车速'] == 0 and df_one_i['发动机转速'] < 300:
        df1.drop(index=index)

print(tp_num)

for tp_num_one in tp_num:
    df1['GPS车速'][tp_num_one[0] + 90:tp_num_one[1] - 90].apply(lambda x: 0)
    df1.drop(index=df1.index[tp_num_one[0]+90:tp_num_one[1]-90], inplace=True)


print(df1) # [373412 rows x 14 columns]  [312299 rows x 14 columns] [299822 rows x 14 columns]
# df1.to_csv('./data/2019921data1_pass.csv')



v1 = []
tp_num1 = []
start_index1 = 0
for index, df_one_i in df1.iterrows():
    if df_one_i['GPS车速'] != 0:
        try:
            if df1.iloc[index + 1]['GPS车速'] == 0:
                v1.append((start_index1, index + 1))
                start_index1 = index + 1
        except:
            pass
print(v1)

L = []
new_df = pd.DataFrame(columns=['平均速度', '平均行驶速度', '平均加速度', '平均减速度', '怠速时间比',
                               '加速时间比', '减速时间比', '速度标准差', '加速度标准差'])
for v1_i in v1:
    if (v1_i[1] - v1_i[0]) > 50:
        df2 = df1[v1_i[0]:v1_i[1]]
        if ((df2['GPS车速'] > 0).astype(int).sum()) > 10 and (df2['进气流量'].isna().sum() / len(df2)) < 0.6:
            print(df2)
            print(df2['进气流量'].isna().sum() / len(df2))
            L.append(len(df2))

            df2['油门踏板开度'] = df2['油门踏板开度'].interpolate(method='linear')
            df2['空燃比'] = df2['空燃比'].interpolate(method='linear')
            df2['发动机负荷百分比'] = df2['发动机负荷百分比'].interpolate(method='linear')
            df2['进气流量'] = df2['进气流量'].interpolate(method='linear')

            new_df = get_data(new_df,df2)

            # get_drow(df2)
            # print(input('继续？：'))
            # df2.to_csv('./data/data1/{}.csv'.format(v1.index(v1_i)))

new_df.to_csv('./data/new_df3.csv')
new_df.to_excel('./data/new_df3.xls')
print(sum(L))

