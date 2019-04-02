from element import Elements
from my_array import My_array
import gcmstools
import re
from scipy.special import comb,binom
from copy import deepcopy
from decimal import Decimal


WorkPath=''
ELEMENTS=Elements()

class Formula:

    @classmethod
    def InputError(cls,t):
        print(t)

    def get_mass(self):
        mass=0
        for i in self.formula:
            mass+=ELEMENTS.element_normal_mass[i]*self.formula[i]
        self.mass=mass
        return mass

    def __init__(self,formula):
        if isinstance(formula,Formula) :
            self.formula=deepcopy(formula.formula)
            self.formula_str=deepcopy(formula.formula_str)
        elif isinstance(formula,dict):
            self.formula=deepcopy(formula)
            self.formula_str=str(formula)
        else:
            self.formula_str=formula
            if re.match(r'^(C\d*)(H\d*)?(N\d*)?(O\d*)?(P\d*)?(S\d*)?(Si\d*)?$',formula) !=None:
                num=re.findall(r'([A-Z][a-z]?)(\d*)?',formula)
                items={}
                for i in num:
                    if i[1]!='':
                        items[i[0]]=int(i[1])
                    else:
                        items[i[0]]=1
                self.formula=items
                self.mass=self.get_mass()
            else:
                raise Formula.InputError('you have input a error format of formula!:%s'%formula)

    def __str__(self):
        return self.formula_str
    




class Molecule:

    @classmethod
    def get_deep(cls,target):
        if len(target)==2:
            result=[]
            for i in range(len(target[0])):
                for j in range(len(target[1])):
                    mass=i+j
                    p=target[0][i]*target[1][j]
                    result.append((mass,p))
            return result
        if len(target)>2:
            result=[]
            a=target[0]
            b=Molecule.get_deep(target[1:])
            for i in a:
                for j in b:
                    mass=i+j[0]
                    p=a[i]*j[1]
                    result.append((mass,p))
            return result




    def __init__(self,name,formula,peaks,tracer='C'):
        #化合物名
        self.name=name
        #分子式
        self.formula=Formula(formula).formula
        #峰值读数
        self.peaks=peaks
        #分子量
        self.mass=self.get_mass()
        #所选用的tracer
        self.tracer=tracer
        #自然情况下每种元素的分布
        self.element_distribution={}
        self.get_element_distribution()      
        #自然情况下的分布
        self.distribution={}
        self.get_distribution()
        #天然同位素对每种峰的贡献情况
        self.iso_contribution={}
        #人工marker对峰的贡献情况
        self.tracer_contribution={}
        self.get_nature_iso_distribution()
        self.get_tracer_contribution()
        
        
        


    def get_mass(self):
        mass=0
        for i in self.formula:
            mass+=ELEMENTS.element_normal_mass[i]*self.formula[i]
        self.mass=mass
        return mass
    
    def get_element_distribution(self):
        e=ELEMENTS.element
        for i in self.formula:
            dimension=len(e[i])
            target=self.formula[i]
            dis_factor=My_array(target,dimension).array

            #开始计算元素的分布，before_total为之前的系数和，p为每一部分的概率，p_total为该情况的概率（的100倍），mass为该情况下的分子量增加
            #mass_and_p为数据的初步集合，mass_p是字典{mass：p*100}
            mass_and_p=[]
            mass_P={}
            for j in dis_factor:
                before_total=0
                p_total=Decimal(1)
                mass_total=0
                #t代表同位素的相对分子量，j[t]是该同位素取的系数，e[i][t]是该同位素的概率
                for t in range(dimension):
                    p=Decimal(comb(target-before_total,j[t])*e[i][t]**j[t])
                    p_total*=p
                    mass=t*j[t]
                    mass_total+=mass
                    before_total+=j[t]
                mass_and_p.append((mass_total,p_total))
            for k in mass_and_p:
                if k[0] in mass_P:
                    mass_P[k[0]]+=k[1]
                else:
                    mass_P[k[0]]=k[1]
            self.element_distribution[i]=deepcopy(mass_P)
        return self.element_distribution

    def get_distribution(self):
        e=self.element_distribution
        elements=deepcopy(list(e.values()))
        mass_and_p=Molecule.get_deep(elements)
        for i in mass_and_p:
            if i[0] in self.distribution:
                self.distribution[i[0]]+=i[1]
            else:
                self.distribution[i[0]]=i[1]
        
        return self.distribution

    def get_nature_iso_distribution(self):
        num=len(self.peaks)
        total_nature=Decimal(float(self.peaks[0]))/self.distribution[0]
        for i in range (num):
            self.iso_contribution[i]=total_nature*self.distribution[i]
        self.iso_contribution[0]=Decimal(self.peaks[0])
        for i in range(num):
            self.tracer_contribution[i]=Decimal(float(self.peaks[i]))-Decimal(float(self.iso_contribution[i]))
            if self.tracer_contribution[i]<0: self.tracer_contribution[i]=0
            lable=Labeled_molecule(self.formula,Decimal(self.tracer_contribution[i]),self.tracer,i)
            for t in range(len(lable.iso_distribution)):
                if i+t>=num:
                    break
                self.iso_contribution[i+t]+=lable.iso_distribution[t]
        return self.iso_contribution
    
    def get_tracer_contribution(self):
        for i in self.iso_contribution:
            self.tracer_contribution[i]=Decimal(self.peaks[i])-Decimal(self.iso_contribution[i])
        return self.tracer_contribution


class Labeled_molecule:
    def __init__(self,formula,intensity,tracer='C',label_num=0):
        self.formula=Formula(formula)
        self.label_formula=deepcopy(self.formula).formula
        self.label_formula[tracer]-=label_num
        self.intensity=intensity
        self.element_distribution={}
        self.get_element_distribution()
        self.distribution={}
        self.get_distribution()
        self.iso_distribution={}
        self.get_iso_dirtribution()

        


    def get_mass(self):
        mass=0
        for i in self.label_formula:
            mass+=ELEMENTS.element_normal_mass[i]*self.label_formula[i]
        self.mass=mass
        return mass
    
    def get_element_distribution(self):
        e=ELEMENTS.element
        for i in self.label_formula:
            dimension=len(e[i])
            target=self.label_formula[i]
            dis_factor=My_array(target,dimension).array

            #开始计算元素的分布，before_total为之前的系数和，p为每一部分的概率，p_total为该情况的概率（的100倍），mass为该情况下的分子量增加
            #mass_and_p为数据的初步集合，mass_p是字典{mass：p*100}
            mass_and_p=[]
            mass_P={}
            for j in dis_factor:
                before_total=0
                p_total=Decimal(1)
                mass_total=0
                #t代表同位素的相对分子量，j[t]是该同位素取的系数，e[i][t]是该同位素的概率
                for t in range(dimension):
                    p=Decimal(comb(target-before_total,j[t])*e[i][t]**j[t])
                    p_total*=p
                    mass=t*j[t]
                    mass_total+=mass
                    before_total+=j[t]
                mass_and_p.append((mass_total,p_total))
            for k in mass_and_p:
                if k[0] in mass_P:
                    mass_P[k[0]]+=k[1]
                else:
                    mass_P[k[0]]=k[1]
            self.element_distribution[i]=deepcopy(mass_P)
        return self.element_distribution
    
    def get_distribution(self):
        e=self.element_distribution
        elements=deepcopy(list(e.values()))
        mass_and_p=Molecule.get_deep(elements)
        for i in mass_and_p:
            if i[0] in self.distribution:
                self.distribution[i[0]]+=i[1]
            else:
                self.distribution[i[0]]=i[1]
        
        return self.distribution
    
    def get_iso_dirtribution(self):
        total=self.intensity/self.distribution[0]
        for i in self.distribution:
            self.iso_distribution[int(i)]=total*self.distribution[i]
        self.iso_distribution[0]=0
        return self.iso_distribution






           







    