import pandas as pd
import os
from element import Elements
from molecule import Molecule,Formula
import re



class Metabolite :
    __Metabolite_file='mocules.dat'

    def __init__(self):
        '''
        这个类中有一个属性，即为metabolites，是一个字典,{molecule_name:{'mass':{releative_mass:rf_time},'formula':formula(Formula对象),'derive_formula':derive_formula}}
        '''
        data=pd.read_csv(self.__Metabolite_file)
        metabolites={}
        for index,row in data.iterrows():
            name_mass=row['name'].lower()
            rf_time=row['rf_time']
            formula=str(row['formula'])
            derive_formula=str(row['derive_formula'])
            names_list=re.findall(r'([0-9a-zA-Z\-]+?)\s[Mm]\+(\d+)',name_mass)[0]
            try:
                if names_list[0] in metabolites:
                    metabolites[names_list[0]]['mass'][int(names_list[1])]=float(rf_time)
                    if formula != 'nan':
                        metabolites[names_list[0]]['formula']=Formula(formula)
                        metabolites[names_list[0]]['derive_formula']=Formula(derive_formula)
                else:
                    metabolites[names_list[0]]={'mass':{},'formula':'','derive_formula':'',}
                    metabolites[names_list[0]]['mass'][int(names_list[1])]=float(rf_time)
                    if formula != 'nan':
                        metabolites[names_list[0]]['formula']=Formula(formula)
                        metabolites[names_list[0]]['derive_formula']=Formula(derive_formula)
            except:
                print(metabolites)
        self.metabolites=metabolites

        
