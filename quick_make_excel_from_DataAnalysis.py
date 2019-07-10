import pandas as pd
import os
import datetime

WORK_PATH='YuanYin-20190706'
FILE_NAME='abc.txt'
RESULT_DIR='result'

path=os.path.join(os.getcwd(),WORK_PATH)
result_dir=os.path.join(os.getcwd(),RESULT_DIR,datetime.date.today().strftime('%y%m%d'))
try:
    os.makedirs(result_dir)
except:
    pass




def get_excel(dir_path,file_name,result_dir):
    '''dir_path means the directory of data, where your FILE_NAME can find a file;
    file_name means the name of result you would get;
    result_dir means the path where you would save your results in'''
    try:
        with open(dir_path,'r') as f:
            df=pd.DataFrame(columns=['化合物名称','面积'])
            for i in range(20):
                f.readline()
            while True:
                line=f.readline()
                if '-' in line:
                    break
                line_list=line.split(' ')
                clean_line=[]
                tmp={}
                for i in line_list:
                    if len(i)>1:
                        clean_line.append(i)
                try:
                    tmp['化合物名称']=clean_line[1]+' '+clean_line[2]
                    try:
                        tmp['面积']=clean_line[5]
                    except:
                        tmp['面积']=0
                    df=df.append(tmp,ignore_index=True)
                except:
                    print('%s in %s has some problem'%(clean_line[1],file_name))
                    #print('%s in %s has some problem'%(clean_line[1],file_name))
            df.to_excel(os.path.join(result_dir,file_name+'.xlsx'))
    except:
        print('somethine wrong in %s'%file_name)


files=os.listdir(path)
dirs=[]
for i in files:
    if os.path.isdir(os.path.join(path,i)):
        dirs.append(i)

for i in dirs:
    p=get_excel(os.path.join(path,i,FILE_NAME),i,result_dir)
