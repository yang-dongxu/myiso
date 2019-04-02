
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


class Elements:
    '''
    Element类中实例有两三个属性，一个是element，为一字典，字典的键为元素，键值为另一字典，其键元素相对标准型的分子量，键值为自然丰度
    即为{element:{relative mass:abundance}}
    element_in_mass_abundance为mass而不是relative mass
    element_normal_mass元素最常见的原子量，用于计算分子量{element:mass}
    '''

    def __init__(self):
        p=pd.read_csv('Isotopes.dat')
        
        element_abundance={}
        element=p['element']
        mass=p['mass']
        abundance=p['abundance']
        for i in range(0,len(mass)):
            if element[i] in element_abundance:
                element_abundance[element[i]].append([mass[i],abundance[i]])
            else:
                element_abundance[element[i]]=[[mass[i],abundance[i]]]
        
        element_dict={}
        for i in element_abundance:
            item={}
            for t in element_abundance[i]:
                item[t[0]]=round(t[1],8)
            element_dict[i]=item
            
        element_normalized={}
        element_normal_mass={}
        for i in element_dict:
            max_abun=[0,0]
            item={}
            for t in element_dict[i]:
                if element_dict[i][t]>max_abun[1]:
                    max_abun=[t,element_dict[i][t]]
            element_normal_mass[i]=max_abun[0]
            for t in element_dict[i]:
                item[int(t-max_abun[0]+0.5)]=element_dict[i][t]
            element_normalized[i]=item
  
        
        self.element=element_normalized
        self.element_in_mass_abundance=element_dict
        self.element_normal_mass=element_normal_mass

        

    

