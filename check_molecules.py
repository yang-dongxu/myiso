#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import re


# In[13]:


def check_formula(df):
    try:
        for index,row in df.iterrows():
            try:
                if re.match(r'^(C\d*)(H\d*)?(N\d*)?(O\d*)?(P\d*)?(S\d*)?(Si\d*)?$',row['formula']):
                    if re.match(r'^(C\d*)(H\d*)?(N\d*)?(O\d*)?(P\d*)?(S\d*)?(Si\d*)?$',row['derive_formula']):
                        continue
                print('here: %s, in the line %d the formula or derive_formula has something wrong!'%(row['name'],index+2) )
            except:
                print(row)
    except:
        print('iter in check_formula_failed')

# In[14]:


def check_order(df):
    names=df['name']
    clean=pd.DataFrame(columns=['name','num'])
    for i in names:
        try:
            tmp={}
            tmp['name']=i.split('+')[0]
            tmp['num']=int(i.split('+')[1])
            clean=clean.append(tmp,ignore_index=True)
        except:
            print(i)
    kinds=list(set(clean['name']))
    for i in kinds:
        nums=clean[clean['name']==i]
        nums=nums.reset_index(drop=True)
        max_num=max(nums['num'])
        if max_num==len(nums)-1:
            continue
        else:
            print('%s has something wrong,maybe loss some index'%i)


# In[16]:


try:
    df=pd.read_csv('mocules.dat')
    try:
        check_order(df)
    except:
        print ('check_order_fail')
    try: 
        check_formula(df)
    except:
        print('check_formula_fail')
except:
    print('no mocules.dat,does it named rightly? attention please, not molecule,but mocule,not .csv but .dat')


# In[ ]:




