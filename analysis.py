import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_csv('train.csv')

data.info()


data.shape

data_copy=data.copy()
data_copy.drop(['Id'],axis=1,inplace=True)
data_copy



data_copy.isna().sum()


data_copy.hist(bins=50,figsize=(20,15))



max(data_copy['Sold Price'])


var = 'Year built'
data = pd.concat([data_copy['Sold Price'], data_copy[var]], axis=1)
f, ax = plt.subplots(figsize=(16, 8))
fig = sns.boxplot(x=var, y="Sold Price", data=data)
fig.axis(ymin=0, ymax=8000000)
plt.xticks(rotation=90)


num_f = [f for f in data_copy.columns if data_copy.dtypes[f] != 'object']
num_f.remove('Sold Price')
num_f



def jointplot(x,y,**kwargs):
    try:
        sns.regplot(x=x,y=y)
    except Exception:
        print(x.value_counts())
f = pd.melt(data_copy, id_vars=['Sold Price'], value_vars=num_f)
g = sns.FacetGrid(f,col='variable',col_wrap=3,sharex=False,sharey=False,height=5)
g = g.map(jointplot,'value','Sold Price')
# g.get_figure()
g.savefig('picture/多维关系图.jpg')

fig=plt.figure()
ax = sns.histplot(np.log10(data_copy['Sold Price']))
ax.set_xlim([3, 8])
ax.set_xticks(range(3, 9))
ax.set_xticklabels(['%.0e'%a for a in 10**ax.get_xticks()]);
fig.savefig('picture/成交价位分布图.jpg')

fig=plt.figure()
ax = sns.histplot(np.log10(data_copy['Listed Price']))
ax.set_xlim([3, 8])
ax.set_xticks(range(3, 9))
ax.set_xticklabels(['%.0e'%a for a in 10**ax.get_xticks()]);
fig.savefig('picture/定价分布图.jpg')

data_copy['Type'].value_counts()[0:20]


types = data_copy['Type'].isin(['SingleFamily', 'Condo', 'MultiFamily', 'Townhouse'])
fig=sns.displot(pd.DataFrame({'Sold Price':np.log10(data_copy[types]['Sold Price']),
                              'Type':data_copy[types]['Type']}),
                x='Sold Price', hue='Type', kind='kde');
fig.savefig('picture/前四个数量最多的房型密度图.jpg', dpi = 400)

data_copy['Price per living sqft'] = data_copy['Sold Price'] / data_copy['Total interior livable area']
fig=plt.figure()
fig = sns.boxplot(x='Type', y='Price per living sqft', data=data_copy[types], fliersize=0)
fig.set_ylim([0, 2000]);
boxplot=fig.get_figure()
boxplot.savefig('picture/前四个数量最多的房型的单位房价箱式图.jpg')

data_copy['Price per living sqft']

data = pd.concat([data_copy['Sold Price'], data_copy['Total interior livable area']], axis=1)
fig=plt.figure()
fig=data.plot.scatter(x='Total interior livable area', y='Sold Price',xlim=(0,20000), ylim=(0,20000000))
plt.savefig('picture/面积与成交价的关系图.jpg')

d = data_copy[data_copy['Zip'].isin(data_copy['Zip'].value_counts()[:20].keys())]
fig=plt.figure()
fig = sns.boxplot(x='Zip', y='Price per living sqft', data=d, fliersize=0)
fig.set_ylim([0, 2000])
# fig.set_xticklabels(ax.get_xticklabels(), rotation=90);
boxplot=fig.get_figure()
boxplot.savefig('picture/邮编与单位面积房价关系图.jpg')


data_copy.dtypes


num_f.append('Sold Price')


num_f


fig, ax = plt.subplots(figsize=(20,20))
sns.heatmap(data_copy[num_f].corr(),annot=True,cmap='RdYlGn', ax=ax);
fig.savefig('picture/热力图.jpg')


x=data_copy['Bedrooms'].value_counts()[0:5].index[:5]
x


y=[]
for i in range(5):
    y.append(data_copy['Bedrooms'].value_counts()[0:5][i])
y



fig, ax = plt.subplots(figsize=(10, 7))
ax.bar(x=x, height=y)
ax.set_title("Bedroom Situation", fontsize=15)
fig.savefig('picture/卧室个数情况图.jpg')

plt.scatter(data_copy['Elementary School Score'],data_copy['Sold Price'],c='r',alpha=0.5)
plt.scatter(data_copy['Middle School Score'],data_copy['Sold Price'],c='b',alpha=0.5)
plt.scatter(data_copy['High School Score'],data_copy['Sold Price'],c='g',alpha=0.5)
plt.title('School Score and Sold Price')
plt.savefig('picture/学校分数与成交价的关系.jpg')
plt.show()


x=data_copy['Elementary School Score'].value_counts()
x.iloc[0]


l=len(x)
l


def avedata(x,y):
    sum1=0
    num1=0
    for i in range(len(data_copy)):
        if(data_copy[y][i]==x):
            sum1=sum1+data_copy['Sold Price'][i]
            num1=num1+1
    if(num1==0):
        ave1=0
    else:
        ave1=sum1/num1
    return ave1
avex=[]
for j in range(1,11):
    avex.append(avedata(j,'Elementary School Score'))
avey=[]
for j in range(1,11):
    avey.append(avedata(j,'Middle School Score'))
avez=[]
for j in range(1,11):
    avez.append(avedata(j,'High School Score'))
score=[]
for i in range(1,11):
    score.append(i)

 #用来正常显示中文标签
plt.title('School Score and Average Price')
plt.plot(score,avex,label='Primary School')
plt.plot(score,avey,label='Middle School')
plt.plot(score,avez,label='High School')
plt.legend(loc=0)
plt.savefig('picture/学校分数与平均价格折线图.jpg')
plt.show()

plt.scatter(data_copy['Elementary School Distance'],data_copy['Sold Price'],c='r')
plt.scatter(data_copy['Middle School Distance'],data_copy['Sold Price'],c='b')
plt.scatter(data_copy['High School Distance'],data_copy['Sold Price'],c='g')
plt.title('School Distance and Sold Price')
plt.savefig('picture/学校距离与成交价散点图.jpg')
plt.show()