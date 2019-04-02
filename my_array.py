import copy

class My_array:
    '''
    这个类通过属性array来形成一个列表，列表中的每一项是一个各项和为target的长为dimension的列表
    '''
    def __init__(self,target,dimension):
        self.dimension=dimension
        self.target=target
        self.array=self.get_array(self.target,self.dimension)
    
    def get_array(self,target,dimension):
        if dimension==1:
            result=[]
            result.append([target,])
            return result
        if dimension==2:
            new_array=[]
            result=[]
            for i in range(target+1):
                new_array=[i,target-i]
                result.append(new_array)
            return result
        if dimension>2:
            new_array=[]
            result=[]
            for i in range(target+1):
                new_low_array=self.get_array(i,dimension-1)
                for j in new_low_array:
                    #这里很啰嗦，但是一改就会有bug，我也不知道为啥？？？？？
                    new_array=copy.deepcopy(j)
                    new_array.append(target-i)
                    result.append(copy.deepcopy(new_array))
            return result


                
            
