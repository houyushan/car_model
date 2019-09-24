# -*- coding: utf-8 -*-

"""
@Time    : 2019/9/21 14:52
@User    : HouYushan
@Author  : xueba1521
@FileName: D_data4.py
@Software: PyCharm
@Blog    ：http://---
"""
import pandas as pd

# 合并两个文件中的运动学特征数据
def get2one():
    df1 = pd.read_csv('./data/new_df1.csv')
    df2 = pd.read_csv('./data/new_df2.csv')
    df3 = pd.read_csv('./data/new_df3.csv')

    res=pd.concat([df1,df2],axis=0, ignore_index=True)

    print(res)
    res.to_csv('./data/data_out.csv')
    res.to_excel('./data/data_out.xls')


'''主成分分析'''

# from sklearn.decomposition import PCA
# import numpy as np # 如果使用numpy的array作为参数的数据结构就需要，其他type没试过是否可以
#
# X_pca= pd.read_csv('./data/data_out.csv')
# X_pca=np.array(X_pca)
#
# a=PCA(n_components=3) # 设置降维后的特征数目
# a.fit(X_pca) # 传入我们的数据
#
# X_new=a.transform(X_pca) # 得到降维后的新数据，仍然是numpy的array形式
# print(a.explained_variance_ratio_) # 查看降维后的各主成分的方差值占总方差值的比例
# print(a.explained_variance_) #查看降维后的各主成分的方差值


from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

df1 = pd.read_csv('./data/data_out.csv', encoding='utf8')

df1 = df1.loc[:, '减速时间比':]
# print(X)
# 查看特征相关性
# corr_matrix = df1.corr(method='pearson')

# df1 = df1.drop(df1.columns[1],axis=1)
X = df1.values


# 中心标准化
from sklearn import preprocessing
X = preprocessing.scale(X)
print('标准化',X)



pca = PCA(n_components= 0.85) # mle  https://www.cnblogs.com/pinard/p/6243025.html
X_data = pca.fit_transform(X)
# print(X_data)
# for i in range(len(data)):

print(pca.explained_variance_ratio_)# 返回单个变量方差贡献率
print(pca.explained_variance_) # 方差的具体的值
Ureduce = pca.components_# 特征矩阵
print(Ureduce)
Ureduce_df = pd.DataFrame(Ureduce,columns=['减速时间比','加速度标准差','加速时间比','匀速时间比','平均减速度','平均加速度',
                                           '平均行驶速度','平均速度','怠速时间比','持续时间','最大速度','行驶距离','速度标准差'])

print(Ureduce_df)
Ureduce_df.to_excel('./data/Ureduce_df.xls')




# 转化后的数据分布散点图
plt.scatter(X_data[:, 0], X_data[:, 1],marker='o')
plt.show()

xSrc = X[:, 0]
ySrc = X[:, 1]
# print(xSrc)
# print(ySrc)
# plt.scatter(xSrc, ySrc, marker='o', c='r', alpha=0.5)  # 原坐标点的图

# xInverse = X_data[:, 0]
# yInverse = X_data[:, 1]
# plt.scatter(xInverse, yInverse, marker='o', c='b', alpha=0.5)  # 降为一维后再变为二维的图
# plt.show()

x2Inverse = X_data[:,0]
y2Inverse = X_data[:,1]

plt.scatter(x2Inverse, y2Inverse, marker='o',c='g',alpha=0.5) # 降为二维后再变为二维的图
plt.show()

from sklearn.cluster import KMeans  # https://blog.csdn.net/playgoon2/article/details/77326045
def K_Means():
    # 利用KMeans进行聚类，分为3类
    kmeans = KMeans(n_clusters=3,random_state=0).fit(X_data)
    # labels为分类的标签
    labels = kmeans.labels_
    #把标签加入到矩阵中用DataFrame生成新的df，index为类别的编号，这里是0,1,2
    dataDf = pd.DataFrame(X_data,index=labels,columns=['x1','x2','x3','x4','x5'])

    dataDf.to_excel('./data/k_means_data.xls')
    print(pca.explained_variance_ratio_)