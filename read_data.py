from metabolite import Metabolite
from molecule import Molecule
from element import Elements
import pandas as pd
import re
from decimal import Decimal
import os
from gcmstools.filetypes import AiaFile

class Data_CDF:
    
    def __init__(self,dataname,derivated=True, A=0.1,W=5,TH=1.2):
        self.file_name=dataname
        '''dataname为输入的文件名，derivated为True表示衍生化，A表示保留时间的振幅'''
        self.data=AiaFile(dataname)
        self.A=A
        self.W=W
        self.TH=1.1
        #self.metabolite={name:{'mass':{mass:rf_time},'formula':formula,'derive_formula':derive_formula}}
        self.metabolite=Metabolite().metabolites
        #是否衍生化
        self.derivated=derivated
        if derivated==True:
            self.type='derive_formula'
        else:
            self.type='formula'
        #self.rf_time={name:[(mass,rf_time)]}
        self.rf_times={}
        self.get_rf_times()
        #all_peaks={name:{mass:peak}}
        self.all_peaks={}
        self.get_all_peaks()
        #self.moolecules={name:Molecule}
        self.molecules={}
        self.get_molecules()

   
        
    
    def get_rf_times(self):
        if self.derivated:
            type='derive_formula'
        else:
            type='formula'

        for i in self.metabolite:
            mass=int(self.metabolite[i][type].mass)
            index=[]
            for t in self.metabolite[i]['mass']:
                index.append((mass+t,self.metabolite[i]['mass'][t]))
            self.rf_times[i]=index
        return self.rf_times

    def get_index(self,info):
        mass,rf_time=info
        time_index=self.data.index(self.data.times,rf_time)
        mass_index=self.data.index(self.data.masses,mass)
        return (mass_index,time_index)

    def get_intensity(self,info):
        '''info=(mass,rf_time)'''
        info_min=(info[0],info[1]-self.A)
        info_max=(info[0],info[1]+self.A)
        index_min=self.get_index(info_min)
        index_max=self.get_index(info_max)
        index=self.get_index(info)
        '''
        try:
            num=[t[index[0]] for t in self.data.intensity]
            for i in range(index[1]-int(self.W/2),index_min[1]-1,-1):
                if num[i]>num[i-1]:
                    pass
                else:
                    if sum([num[t] for t in range(i,i+self.W+1)])/ (sum([num[t] for t in range(i-self.W,i+1)])+1)>self.TH:
                        pass
                    else:
                        break
        except:
            print(self.data.intensity)
        rf_time_min_index=i
        for i in range(index[1]+int(self.W/2),index_max[1]+1,1):
            if num[i]>num[i+1]:
                pass
            else:
                if (sum([num[t] for t in range(i,i-self.W,-1)]))/ (sum([num[t] for t in range(i,i+self.W+1)])+1)>self.TH:
                    pass
                else:
                    break
        rf_time_max_index=i
        '''

        rf_time_min_index=index_min[1]
        rf_time_max_index=index_max[1]
        intensity=[]
        for i in range (rf_time_min_index,rf_time_max_index,1):
            intensity.append(self.data.intensity[i][index_min[0]])
        intensity_area=sum([i for i in intensity])
        return intensity_area




    def get_all_peaks(self):
        all_peaks={}
        for i in self.rf_times:
            mass_peaks={}
            for t in self.rf_times[i]:                                
                mass=int(t[0]-int(self.metabolite[i][self.type].mass+0.5))
                if t[1]>0:
                    mass_peaks[mass]=self.get_intensity(t)
                else:
                    mass_peaks[mass]=0
            all_peaks[i]=mass_peaks
        self.all_peaks=all_peaks

    def get_molecules(self):
        for i in self.all_peaks:
            name=i
            formula=self.metabolite[i][self.type]
            peaks=self.all_peaks[i]
            self.molecules[i]=Molecule(name,formula,peaks)
        return self.molecules

    def output(self):
        m=pd.DataFrame(columns=['name','tracer_contribution','nature_iso_contribution','total_peakarea','percent'])
        li=[]
        for i in self.molecules:
            total=sum([max(self.molecules[i].tracer_contribution[j],0) for j in self.molecules[i].tracer_contribution])
            total+=Decimal(self.molecules[i].peaks[0])
            for j in self.molecules[i].iso_contribution:
                new_row={}
                new_row['name']=i+'  M+%d'%j
                new_row['tracer_contribution']=self.molecules[i].tracer_contribution[j]
                new_row['nature_iso_contribution']=max(self.molecules[i].iso_contribution[j],0)
                new_row['total_peakarea']=self.molecules[i].peaks[j]
                new_row['percent']=max(self.molecules[i].tracer_contribution[j],0)/(Decimal(total)+Decimal(1))
                if j==0:
                    new_row['tracer_contribution']=0
                    new_row['nature_iso_contribution']=self.molecules[i].peaks[0]
                    new_row['percent']=Decimal(self.molecules[i].peaks[0])/(Decimal(total)+Decimal(1))
                li.append(new_row)

        m=m.append(li,ignore_index=True)
        try:
            os.makedirs('result')
        except:
            pass
        name=self.file_name.split('/')[-1]
        m.to_excel('result\\'+name+'.xlsx')

  

class Data:
    def __init__(self,file_name,tracer='C',name='化合物名称',peak_area='面积',type='xls',derivated=True):
        if type=='xls':
            p=pandas.read_excel(file_name,'QRes')
        elif type=='csv':
            p=pandas.read_csv(file_name)
        
        if derivated==True:
            self.form='derive_formula'
        else:
            self.form='formula'
        
        self.metabolite=Metabolite().metabolites
        self.molecules={}
        self.data={}
        self.file_name=file_name
        
        for index,i in p.iterrows():
            molecule_name=i[name]
            area=i[peak_area]
            try:
                names_list=re.findall(r'([0-9a-zA-Z\-]+?)\s[Mm]\+(\d+)',molecule_name)[0]
            except:
                if molecule_name=='C13':
                    continue
            if names_list[0].lower() in self.data:
                self.data[names_list[0].lower()][int(names_list[1])]=area
            else :
                self.data[names_list[0].lower()]={int(names_list[1]):area}
        for i in self.data:
            self.molecules[i]=Molecule(i,self.metabolite[i][self.form],self.data[i],tracer=tracer)

    def output(self):
        m=pd.DataFrame(columns=['name','tracer_contribution','nature_iso_contribution','total_peakarea','percent'])
        li=[]
        for i in self.molecules:
            total=sum([max(self.molecules[i].tracer_contribution[j],0) for j in self.molecules[i].tracer_contribution])
            total+=Decimal(self.molecules[i].peaks[0])
            for j in self.molecules[i].iso_contribution:
                new_row={}
                new_row['name']=i+'  M+%d'%j
                new_row['tracer_contribution']=self.molecules[i].tracer_contribution[j]
                new_row['nature_iso_contribution']=max(self.molecules[i].iso_contribution[j],0)
                new_row['total_peakarea']=self.molecules[i].peaks[j]
                new_row['percent']=max(self.molecules[i].tracer_contribution[j],0)/(Decimal(total)+Decimal(1))
                if j==0:
                    new_row['tracer_contribution']=0
                    new_row['nature_iso_contribution']=self.molecules[i].peaks[0]
                    new_row['percent']=Decimal(self.molecules[i].peaks[0])/(Decimal(total)+Decimal(1))
                li.append(new_row)

        m=m.append(li,ignore_index=True)
        try:
            os.makedirs('result')
        except:
            pass
        name=self.file_name.split('/')[-1]
        m.to_excel('result\\'+name+'.xlsx')



#以下函数已经没用了，是因为之前拿到过一次特殊的格式创建的
class Data_mul:
    def __init__(self,file_name,tracer='C',type='xls',derivated=True,sheet='QRes'):
        if type=='xls':
            p=pandas.read_excel(file_name,sheet)
        elif type=='csv':
            p=pandas.read_csv(file_name)
        
        if derivated==True:
            self.form='derive_formula'
        else:
            self.form='formula'
        
        self.data=p
        self.metabolite=Metabolite().metabolites
        self.molecules=[]
        data_list=[]
        name=p.columns
        for index,i in p.iterrows():
            data={}
            for j in name:                
                molecule_name=j
                area=i[j]
                try:
                    names_list=re.findall(r'([0-9a-zA-Z\-]+?)\s[Mm]\+(\d+)',molecule_name)[0]
                except:
                    if molecule_name=='C13':
                        continue
                if names_list[0].lower() in data:
                    data[names_list[0].lower()][int(names_list[1])]=area
                else :
                    data[names_list[0].lower()]={int(names_list[1]):area}
            data_list.append(data)
        self.data_list=data_list
        for t in data_list:
            molecules={}
            for i in t:
                molecules[i]=Molecule(i,self.metabolite[i][self.form],t[i],tracer=tracer)
            self.molecules.append(molecules)    

        pass


    def output(self,file_name):
        result_file=pandas.DataFrame(columns=[i for i in range(len(self.data.columns))])
        result=[]
        for i in self.molecules:
            for j in i:
                row={}
                total=0
                for num in i[j].tracer_contribution:
                    if num==0:
                        #total+=0
                        total+=i[j].peaks[0]
                        continue
                    total+=i[j].tracer_contribution[num]
                for num in i[j].tracer_contribution:
                    if num==0:
                        row[0]=i[j].peaks[0]
                        #row[0]=i[j].peaks[0]/total
                        continue
                    row[num]=i[j].tracer_contribution[num]
                    #row[num]=i[j].tracer_contribution[num]/total
            result.append(row)
        result_file=result_file.append(result)
        result_file.to_excel(file_name)
                
def readdata(name):
    if name[-1]=='F':
        p=Data_CDF(name)
        p.output()
    elif name[-4:]=='xlsx':
        p=Data(name)
        p.output()


        


