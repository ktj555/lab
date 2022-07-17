from TEG.Module import *
from copy import deepcopy

class system:
    def __init__(self,info):
        '''
        info : dict{module:module, size:list}
        info's key : ['module', 'size']'''
        self.map=[[deepcopy(info['module']) for j in info['size'][1]] for i in info['size'][0]]

    def set_module(self,info):
        '''
        info : dict{position:module}'''
        for position, module in info.items():
            self.map[position[0]][position[1]]=module

    def set_flow_path(self,flow_path_link):
        '''
        flow_list : dict{values:link}
        key : ['hot', 'cold']'''
        self.hot_path=flow_path_link['hot']
        self.cold_path=flow_path_link['cold']
        self.hot_start,self.hot_end=self.hot_path.find_start_and_end
        self.cold_start,self.cold_end=self.cold_path.find_start_and_end

    def inlet(self,hot_side,cold_side):
        '''
        hot_side, cold_side : dict{podition:condition}
        condition : dict{keys:values}
        keys : ['fluid', 'velocity']'''

    def solve(self,standard='cold',error=1e-3,first_step=1,step_decrease=0.5,print_process=False):
        '''
        residual:float, first_step:float, step_decrease:0~1, print_process:TF'''
        if(standard=='hot'):
            pass

class link:
    def __init__(self,*link):
        '''link : tuple (start,end)'''
        self.link={}
        for start, end in link:
            if(start not in self.link.keys()):
                self.link[start]=[end]
            else:
                if(end not in self.link[start]):
                    self.link[start].append(end)

    def find_start_and_end_point(self):
        given=[]
        spend=[]
        point_list=[]

        for keys, values in self.link.items():
            if(keys not in point_list):
                point_list.append(keys)
            if(keys not in spend):
                spend.append(keys)
            for point in values:
                if(point not in given):
                    given.append(point)
                if(point not in point_list):
                    point_list.append(point)

        start=[]
        end=[]

        for p in point_list:
            if(p not in given):
                start.append(p)
        for p in given:
            if(p not in spend):
                end.append(p)

        return (start,end)