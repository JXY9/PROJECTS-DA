
# coding: utf-8

# In[182]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mooc_jp = pd.read_csv('C:/Users/dell/Desktop/mooc_jp.csv')


# In[183]:


mooc_jp


# In[184]:


mooc_jp.info()


# In[185]:


"""
两个发现：
1. web-scraper-order ，web-scraper-start-url 是两个无效字段--->删除
2. 字段 frequency 缺失，需查看原因
"""


# In[186]:


mooc_jp = mooc_jp.drop(['web-scraper-order','web-scraper-start-url'],axis = 1)


# In[187]:


mooc_jp[mooc_jp.frequency.isnull()==True]


# In[188]:


"""
在mooc上查看，对应的frequency字段信息如下：
创业：道与术       第1次开课
算法设计与分析     第1次开课
宝石加工工艺学     第7次开课
学习工程与管理     第1次开课
四门课程的共同点是 当前开课信息 均为 '当前开课已结束'
抽样（包含'当前开课已结束'的课程）观察其它课程的frequency字段信息
抽样记录为：
无机化学（上）-4193， 大学物理4：光学、近代物理， c语言程序设计-8696， 药物分析-4280， c#程序设计-11609；
并未发现问题
"""


# In[189]:


mooc_jp[mooc_jp.rate == '当前开课已结束']


# In[190]:


"""
抽样序号为：
17，24，29，136，142，799，805；并未发现错误，所以推测 字段frequency的四个缺失值 是没有爬取到，
可能是由于web scraper的两个时间设置的问题。问题不大，采取的措施为 手动补全缺失值
"""


# In[191]:


# 这里需要注意课程名有重复的问题，检查完，这四门课程在国家精品课程里没有重复


# In[192]:


mooc_jp.frequency[mooc_jp['getinto-link'] == '创业：道与术'] = '第1次开课'
mooc_jp.frequency[mooc_jp['getinto-link'] == '算法设计与分析'] = '第1次开课'
mooc_jp.frequency[mooc_jp['getinto-link'] == '宝石加工工艺学'] = '第7次开课'
mooc_jp.frequency[mooc_jp['getinto-link'] == '学习工程与管理'] = '第1次开课'


# In[193]:


mooc_jp[mooc_jp.frequency.isnull()==True]  # 检查


# In[194]:


"""
上面frequency、number、课程评价数三个字段可以直接抽取其中的数字转化成目标字段
"""


# In[195]:


mooc_jp.frequency  = mooc_jp.frequency.str.extract('(\d+)')
mooc_jp.number     = mooc_jp.number.str.extract('(\d+)')
mooc_jp.课程评价数 = mooc_jp.课程评价数.str.extract('(\d+)') 


# In[196]:


mooc_jp.head(3)


# In[197]:


dura = mooc_jp.duration
dura = dura.str.replace('年','-')
dura = dura.str.replace('月','-')
dura = dura.str.replace('日','')
dura_left = dura.str.slice(stop=11)
dura_right = dura.str.slice(start=13)
mooc_jp['开课日期'] = dura_left
mooc_jp['结课日期'] = dura_right


# In[198]:


d = mooc_jp.rate
d_now = d.str.slice(start=4,stop=5)
d_all = d.str.slice(start=8,stop=10)
d_now


# In[199]:


d.value_counts()


# In[200]:


"""
字段 rate 数据不规范，稍微有些麻烦，可能需要使用正则，不过发现可以通过 duration 字段生成该字段
的数据信息 ，所以这里删除该字段信息
"""


# In[201]:


# --------------------


# In[202]:


f = mooc_jp.学时安排

f_1 = f.str.extract('(\d\.\d)\-(\d\.\d)')
index_234567 = f_1.index[f_1.isnull().any(1).values==True].tolist()
mooc_jp_234567 = f.iloc[index_234567]

f_2 = mooc_jp_234567.str.extract('(\d)\-(\d\.\d)')
index_34567 = f_2.index[f_2.isnull().any(1).values==True].tolist()
mooc_jp_34567 = f.iloc[index_34567]

f_3 = mooc_jp_34567.str.extract('(\d\.\d)\-(\d)')
index_4567 = f_3.index[f_3.isnull().any(1).values==True].tolist()
mooc_jp_4567 = f.iloc[index_4567]

f_4 = mooc_jp_4567.str.extract('(\d)\-(\d)')
index_567 = f_4.index[f_4.isnull().any(1).values==True].tolist()
mooc_jp_567 = f.iloc[index_567]

f_5 = mooc_jp_567.str.extract('(\d)\~(\d)')
index_67 = f_5.index[f_5.isnull().any(1).values==True].tolist()
mooc_jp_67 = f.iloc[index_67]

f_6 = mooc_jp_67.str.extract('(\d+)')
index_7 = f_6.index[f_6.isnull().any(1).values==True].tolist()
mooc_jp_7= f.iloc[index_7]

f_7 = mooc_jp_7.str.extract('(\d)\.(\d)')
index_other = f_7.index[f_7.isnull().any(1).values==True].tolist()
mooc_jp_other= f.iloc[index_other]



f_1 = f_1.rename(columns = {0:'atleast',1:'atmost'})
f_2 = f_2.rename(columns = {0:'atleast',1:'atmost'})
f_3 = f_3.rename(columns = {0:'atleast',1:'atmost'})
f_4 = f_4.rename(columns = {0:'atleast',1:'atmost'})
f_5 = f_5.rename(columns = {0:'atleast',1:'atmost'})
f_6 = f_6.rename(columns = {0:'atleast',1:'atmost'})
f_7 = f_7.rename(columns = {0:'atleast',1:'atmost'})
# 接下来在未抽取的记录中抽取 d+ 类别 


# In[203]:


# f_ceui = f.str.extract('(\d\.\d)\~(\d\.\d)').dropna()
# f_ceui  # 分别测试发现，没有 d.d~d.d 这种情况


# In[204]:


# f_c = f.str.extract('(\d.\d)')   # 结果和f_1 一样， 


# In[205]:


result_1234567 = pd.concat([f_1.dropna(), f_2.dropna(), f_3.dropna(), f_4.dropna(), f_5.dropna(), 
                          f_6.dropna(), f_7.dropna()]).reset_index()
result_1234567 = result_1234567.rename(columns ={'index':'rank'})
result_1234567.sort_values('rank')


# In[206]:


mooc_jp_other


# In[207]:


result_1234567['atleast'] = result_1234567['atleast'].astype('float64')
result_1234567['atmost']  = result_1234567['atmost'].astype('float64')

result_1234567['length of study'] = result_1234567['atleast'][result_1234567.atmost.isna() == True]
aver = result_1234567.iloc[:,1:3][result_1234567.atmost.isna() == False]
result_1234567['length of study'][result_1234567['length of study'].isna() == True] = aver.mean(1)
result_1234567.sort_values('rank')


# In[208]:


result_l = result_1234567.loc[:,['rank','length of study']]


# In[209]:


mooc_jp = mooc_jp.reset_index() # mooc_jp['rank'] = mooc_jp.index
mooc_jp = mooc_jp.rename(columns = {'index':'rank'})
mooc_jp = pd.merge(mooc_jp,result_l,how = 'left',on = 'rank' )
mooc_jp


# In[210]:


mooc_jp.iloc[:,[8,14]] # 检查


# In[211]:


mooc_jp.iloc[:,14][mooc_jp.iloc[:,14].isna() == True] = round(result_l.iloc[:,1].mean(),1) 
# 这里将 值为“待定”的记录取为 平均值


# In[212]:


# 因为不需要构建模型，所以字段- active state 不做处理


# In[213]:


mooc_jp['university_s'] = mooc_jp['getinto-link-href'].str.slice(start=34).str.extract('([A-Z]+)')
name_lowercase = mooc_jp['getinto-link-href'].str.slice(start=34).str.extract('([a-z]+)[\-]')
# s.str.extract(r'[ab](\d)', expand=True)
# mooc_jp['university_s']= mooc_jp['getinto-link-href'].str.slice(start=34).str.extract('([a-z]+)[\-]',expand=True)
# mooc_jp['university_s'] = name_lowercase.dropna()
name_lowercase.dropna()


# In[214]:


mooc_jp['university_s'][mooc_jp.university_s.isna() == True] = 'icourse'
mooc_jp.iloc[[213,560],15] = 'sues'


# In[215]:


# mooc_jp[mooc_jp.university_s == 'sues'] 
# mooc_jp.iloc[[213,560],14]


# In[216]:


pd.set_option('max_rows',100) 
mooc_jp.university_s.value_counts()


# In[217]:


dict_all = pd.read_csv('C:/Users/dell/Desktop/dict_all.csv')


# In[218]:


# # college = dict_all.iloc[:,2:4]
college = dict_all.iloc[:,2:4]
college 


# In[219]:


college.columns = college.columns.to_series().apply(lambda x: x.strip())
data_proof = college.set_index('u_s').to_dict()
data_proof


# In[220]:


mooc_jp.university_s = mooc_jp.university_s.replace(data_proof['name'])
mooc_jp


# In[221]:


college_rest = pd.read_csv('C:/Users/dell/Documents/college_rest.csv',engine='python')
college_rest


# In[222]:


data_proof_1 = college_rest[['e','c']]
data_proof_1


# In[223]:


data_proof_1 = data_proof_1.set_index('e').to_dict()
data_proof_1


# In[224]:


mooc_jp.university_s = mooc_jp.university_s.replace(data_proof_1['c'])
mooc_jp


# In[225]:


mooc_jp.info()


# In[226]:


mooc_jp['开课日期'] = pd.to_datetime(mooc_jp['开课日期'], infer_datetime_format=True)
mooc_jp['结课日期'] = pd.to_datetime(mooc_jp['结课日期'], infer_datetime_format=True)
mooc_jp


# In[227]:


mooc_jp['持续周数'] = pd.DataFrame((mooc_jp.结课日期 - mooc_jp.开课日期).dt.days//7 + 1)  


# In[228]:


mooc_jp


# In[229]:


mooc_jp_1 = mooc_jp


# In[230]:


mooc_jp_1 = mooc_jp_1.drop(['getinto-link-href','duration','rate','学时安排','rank'],axis = 1)
mooc_jp_1 = mooc_jp_1.rename(columns={'getinto-link':'课程名','class':'专业类别','frequency':'开课次数',
                                      'average':'学时安排','number':'参加人数', 'university_s':'所属大学',
                                      'length of study':'学时安排','active state':'当前状态'})
mooc_jp_1


# In[231]:


mooc_jp_1.columns


# In[232]:


mooc_jp_1 = mooc_jp_1[['课程名', '专业类别', '所属大学','开课次数',
       '开课日期', '结课日期', '学时安排','持续周数' , '当前状态','参加人数', '课程评价数', '授课教师' ]]
mooc_jp_1


# In[260]:


a = mooc_jp_1.授课教师.str.replace('\\r','')
a = a.str.replace('\\n','')
a = a.str.replace('\n','')
a = a.str.replace('\\','')
a = a.str.lstrip('授课老师')
mooc_jp_1.授课教师 = a
mooc_jp_1


# In[261]:


mooc_jp_1.to_csv('mooc_jp_done.csv')

