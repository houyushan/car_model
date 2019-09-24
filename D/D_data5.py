# -*- coding: utf-8 -*-

"""
@Time    : 2019/9/22 13:41
@User    : HouYushan
@Author  : xueba1521
@FileName: D_data5.py
@Software: PyCharm
@Blog    ：http://---
"""
import pandas as pd

def K_means():
    from sklearn.cluster import KMeans  # https://blog.csdn.net/playgoon2/article/details/77326045
    # 利用KMeans进行聚类，分为3类
    X_data = pd.read_excel('./data/data_out_new.xls')
    X_data = X_data.loc[:,'减速时间比':'']
    kmeans = KMeans(n_clusters=3,random_state=0).fit(X_data)
    # labels为分类的标签
    labels = kmeans.labels_
    #把标签加入到矩阵中用DataFrame生成新的df，index为类别的编号，这里是0,1,2
    dataDf = pd.DataFrame(X_data,index=labels,columns=['x1','x2','x3','x4','x5'])

    dataDf.to_excel('./data/k_means_data.xls')
    print(kmeans.explained_variance_ratio_)

df1 = pd.read_excel('./data/juleijuli.xlsx')
print(df1.head())
df1_1 = df1[df1['类别'] == 1]
df1_2 = df1[df1['类别'] == 2]
df1_3 = df1[df1['类别'] == 3]

df1_1_10 = df1_1.sort_values(by='距离', ascending=True).head(10)
df1_2_10 = df1_2.sort_values(by='距离', ascending=True).head(10)
df1_3_10 = df1_3.sort_values(by='距离', ascending=True).head(10)


V = df1_1_10['v1'].tolist() + df1_2_10['v1'].tolist() + df1_3_10['v1'].tolist()
print(len(V))

import random
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
# plt.figure(dpi=160)
# plt.figure(figsize=(16,8))

L_df = []
L = []

def get_drow(dff):
    fontP = FontProperties(fname=r"C:\\Windows\\Fonts\\SimHei.ttf")  # 设置字体
    fontP.set_size('small')

    x = dff['时间'].head(1300)

    y = dff['GPS车速'].head(1300)
    plt.title("时间-GPS车速", fontproperties=fontP)
    plt.xlabel("x 时间", fontproperties=fontP)
    plt.ylabel("y 车速", fontproperties=fontP)
    plt.plot(x, y)
    plt.show()
    # plt.savefig('./data/1.png', dip=200)
    # plt.draw()

def get_all():
    df_new_1200 = pd.DataFrame(columns=['时间','GPS车速','X轴加速度','Y轴加速度','Z轴加速度','经度','纬度','发动机转速','扭矩百分比','瞬时油耗','油门踏板开度','空燃比','发动机负荷百分比','进气流量'])
    random.shuffle(V)
    for i in V:
        print('i',i)
        path = "./data/new_data/{}.csv".format(i)
        print(path)

        df_new = pd.read_csv(path)
        L.append(len(df_new))
        L_df.append(df_new)
        print('sumL',sum(L))
        if 1300 > sum(L) > 1200:
            df_new_1200.append(L_df,ignore_index=True)
            # print(df_new_1200)
            result_df=pd.concat(L_df)
            print(result_df)
            result_df['油门踏板开度'] = result_df['油门踏板开度'].interpolate(method='linear')
            result_df['空燃比'] = result_df['空燃比'].interpolate(method='linear')
            result_df['发动机负荷百分比'] = result_df['发动机负荷百分比'].interpolate(method='linear')
            result_df['进气流量'] = result_df['进气流量'].interpolate(method='linear')

            # result_df.rename(columns = {'Unnamed: 0':})
            result_df.to_excel('./data/result_df.xls')
            return result_df

for i in range(100):
    new_df = get_all()
    get_drow(new_df)
    break



# path_new = "./data/new_data/"
# filelist_new = os.listdir(path_new) #该文件夹下的所有文件

# t_time = []
# U = []
# df_new_1200_L = []
# for j in range(1000):
#     i = random.randint(0, 30)
#     U.append(i)
#     N = set(U)
#     # print(N)
#
#     df_new_1200 = pd.DataFrame(columns=['时间','GPS车速','X轴加速度','Y轴加速度','Z轴加速度','经度','纬度','发动机转速','扭矩百分比','瞬时油耗','油门踏板开度','空燃比','发动机负荷百分比','进气流量'])
#     for z in N:
#         print('z',z)
#         path = "./data/new_data/{}.csv".format(V[z])
#         print(path)
#         df_new = pd.read_csv(path)
#         print('-----------------',df_new)
#         t_time.append(len(df_new))
#         if sum(t_time) < 1200:
#             # df_new_1200.merge(df_new)
#             df_new_1200 = df_new_1200.append(df_new.T)
#             print('sum_t_time',sum(t_time))
#             print('df_new_1200',len(df_new_1200))
#         else:
#             df_new_1200_L.append(df_new_1200)
#
#     if len(df_new_1200_L) > 10:
#         print('df_new_1200_L',df_new_1200_L)
#         break
#
# ran_i = random.randint(0,30)



# path1="./data/data11/" #文件路径
# path2 = "./data/data22/"
# filelist1 = os.listdir(path1) #该文件夹下的所有文件
# filelist2 = os.listdir(path2)
# filelist = filelist1 + filelist2
# print(filelist)



# for file in filelist: #遍历所有文件 包括文件夹
#         filename = os.path.splitext(file)[0]  #文件名
#         print(filename)

# import os
# def rename():
#     path="./data/data2/" #文件路径
#     path1 = "./data/data22"
#     filelist = os.listdir(path) #该文件夹下的所有文件
#     count =308
#
#     for file in filelist: #遍历所有文件 包括文件夹
#         Olddir = os.path.join(path,file)#原来文件夹的路径
#         if os.path.isdir(Olddir):#如果是文件夹，则跳过
#             continue
#         filename = os.path.splitext(file)[0]  #文件名
#         filetype = ".csv"#os.path.splitext(file)[1]   文件扩展名
#         print(path)
#         Newdir = os.path.join(path1,str(count)+filetype) #新的文件路径
#         os.rename(Olddir,Newdir) #重命名
#         count += 1
# rename()