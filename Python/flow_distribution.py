import numpy as np
import sympy
from sympy import log

shape_list=['h_base','w_base','depth','h_pin','w_pin','n','side']
property_list=['k','epsilon']

class heatsink:
    def __init__(self,info):
        self.shape={}
        self.property={}
        for key, value in info.items():
            if (key in shape_list):
                self.shape[key]=value
            elif (key in property_list):
                self.property[key]=value
            else:
                raise KeyError
        if(not self.check()):
            need=[i for i in shape_list+property_list if i not in list(self.shape.keys())+list(self.property.keys())]
            print("Need More infomation :",need)

    def Add_info(self,info):
        for key, value in info.items():
            if (key in shape_list):
                self.shape[key]=value
            elif (key in property_list):
                self.property[key]=value
            else:
                raise KeyError

    def modify_info(self,info):
        for key, value in info.items():
            if (key in shape_list):
                self.shape[key]=value
            elif (key in property_list):
                self.property[key]=value
            else:
                raise KeyError

    def check(self):
        if(len(self.shape)!=len(shape_list) | len(self.property)!=len(property_list)):
            return False
        else:
            return True

    def friction(self,inlet):
        T=inlet['temperature']
        b=(self.shape['w_base']-self.shape['n']*self.shape['w_pin']-2*self.shape['side'])/(self.shape['n']-1)
        d=2*self.shape['h_pin']*b/(self.shape['h_pin']+b)
        Re=inlet['velocity']*inlet['fluid'].density(T)*d/inlet['fluid'].viscosity(T)
        L_star=self.shape['depth']/(d*Re)
        c=b/self.shape['h_pin']
        f_Re_D_h=(24-32.527*c+46.721*c**2-40.829*c**3+22.954*c**7-6.089*c**5)/Re
        f_app=((3.44/(L_star**0.5))**2+f_Re_D_h**2)**0.5/Re
        e=(self.shape['w_base']-self.shape['n']*self.shape['w_pin'])/self.shape['w_base']
        Kc=0.42*(1-e**2)
        Ke=(1-e**2)**2
        return (f_app*self.shape['n']*(2*self.shape['h_pin']*self.shape['depth']+b*self.shape['depth'])/(self.shape['h_pin']*self.shape['w_base'])+Kc+Ke)*0.5*inlet['fluid'].density(T)*inlet['velocity']**2

class fluid:
    def __init__(self,**info):
        self.density=info['density']
        self.viscosity=info['viscosity']

class system:
    def __init__(self,row,column,h_info):
        self.config=np.array([[heatsink(h_info) for j in range(column)] for i in range(row)])
        self.coef=np.zeros([row,column+1])
    def set_inlet(self,inlet):
        self.temp=inlet['temperature']
        self.fluid=inlet['fluid']
        self.m=inlet['velocity']*inlet['Area']*self.fluid.density(self.temp)
    def calculate_coef(self,row,column,inlet):
        return self.config[row][column].friction(inlet)
    

Air=fluid(density=lambda x: -1.0755E-14*x**5 + 4.3111E-11*x**4 - 6.6881E-08*x**3 + 5.0797E-05*x**2 - 1.9870E-02*x + 3.8841E+00, viscosity=lambda x: -1.4681E-12*x**2 + 5.2975E-09*x + 5.8459E-07)

heat={'h_base':0.003,'w_base':0.06,'depth':0.06,'h_pin':0.025,'w_pin':0.002,'n':9,'side':0.0024}

inlet={'fluid':Air,'temperature':300,'velocity':25,'Area':0.024**2*np.pi}

s=system(3,5,heat)
s.set_inlet(inlet)