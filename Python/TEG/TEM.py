from TEG.material import *

class TEM:
    def __init__(self,info):
        '''
        info : dict
        info's key : ['PN_couple' : material, 'config' : dict{'Width', 'Depth', 'Height'}]'''
        self.pn=info['PN_couple']
        self.config=info['config']
        self.config['Area']=self.config['Width']*self.config['Depth']