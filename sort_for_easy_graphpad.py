#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[9]:


files=os.listdir()
tmp=[]
for i in files:
    if i[-4:]=='xlsx':
        tmp.append(i)
files=tmp


# In[15]:


result=pd.DataFrame(data={'name':pd.read_excel(files[0])['name']})

for i in files:
    df=pd.read_excel(i)
    result[i]=df['percent']*100


# In[17]:


result.to_csv('result.csv')


# In[ ]:




