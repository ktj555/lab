from TEG.material import *
from math import tanh
from sympy import log
import sympy
import numpy as np

epsilon={'Steel':0.046,'Iron':0.26,'Brass':0.002,'Plastic':0.0015,'Glass':0,'Concrete':0.04,'Rubber':0.01,'Wood':0.5}

class Heatsink:
    def __init__(self,info):
        self.material=info['material']
        self.condition=None
        self.base=info['base']
        self.fin=info['fin']

    def set_condition(self,inlet):
        # get environment and boundary condition
        # if getting condition is falled, return False
        self.condition=inlet
        pass

    def is_setting(self):
        # check setting is completed
        # return True of False
        if(self.condition==None):
            return False
        else:
            return True

    def friction(self):
        # calculate friction loss created because viscous during flow pass by heatsink inside
        # if condition is not setted, raise NotSetting Error
        pass

    def Thermal_Resistance(self):
        # calculate Termal Resistance if flow exist
        # if condition is not setted, raise NotSetting Error
        pass

class Plate_fin(Heatsink):
    def __init__(self,info):
        '''
        info : dict
        info's key : ['material' : material, 'base' : dict{'Width', 'Depth', 'Height'}, 'fin' : dict{'Width', 'Height', 'N_fin', 'Side}]
        '''
        super().__init__(info)
        self.Area=(self.base['Width']-self.fin['Width']*self.fin['N_fin'])*self.fin['Height']

    def friction(self):
        T=self.condition['fluid'].Temperature
        b=(self.base['Width']-self.fin['N_fin']*self.fin['Width']-2*self.fin['Side'])/(self.fin['N_fin']-1)
        d=2*self.fin['Height']*b/(self.fin['Height']+b)
        Re=self.condition['velocity']*self.condition['fluid'].Density*d/self.condition['fluid'].Viscosity
        L_star=self.base['Depth']/(d*Re)
        c=b/self.fin['Height']
        f_Re_D_h=(24-32.527*c+46.721*c**2-40.829*c**3+22.954*c**7-6.089*c**5)/Re
        f_app=((3.44/(L_star**0.5))**2+f_Re_D_h**2)**0.5/Re
        e=(self.base['Width']-self.fin['N_fin']*self.fin['Width'])/self.base['Width']
        Kc=0.42*(1-e**2)
        Ke=(1-e**2)**2
        return (f_app*self.fin['N_fin']*(2*self.fin['Height']*self.base['Depth']+b*self.base['Depth'])/(self.fin['Height']*self.base['Width'])+Kc+Ke)*0.5*self.condition['fluid'].Density*self.condition['velocity']**2

    def Thermal_Resistance(self):
        v=self.condition['velocity']
        b=(self.base['Width']-self.fin['N_fin']*self.fin['Width']-2*self.fin['Side'])/(self.fin['N_fin']-1)
        Re=v*b*self.condition['fluid'].Density/self.condition['fluid'].Viscosity
        Re_star=Re*b/self.base['Depth']
        Pr=self.condition['fluid'].Viscosity*self.condition['fluid'].Specificheat/self.condition['fluid'].Conductivity
        Nu_b=((Re_star*Pr/2)**(-3)+(0.664*Re_star**0.5*Pr**(1/3)*(1+3.65/Re_star**0.5)**0.5)**(-3))**(-1/3)
        h=Nu_b*self.condition['fluid'].Conductivity/b
        P_L=(self.fin['Width']+self.fin['Height'])*2
        A_c=self.fin['Width']*self.fin['Height']
        m=(h*P_L/self.material.Conductivity/A_c)**0.5
        R_fin=1/((h*P_L*self.material.Conductivity*A_c)**0.5*tanh(m*self.fin['Height']))
        return 1/(self.fin['N_fin']/R_fin+h*(self.fin['N_fin']-1)*b*self.base['Depth'])


class Pin_fin(Heatsink):
    def __init__(self,info):
        '''
        info : dict
        info's key : ['material' : material, 'base' : dict{'Width', 'Depth', 'Height'}, 'fin' : dict{'Radius', 'Height', 'N_fin'}]
        '''
        super().__init__(info)

    def friction(self):
        pass

    def Thermal_Resistance(self):
        pass

class Nofin(Heatsink):
    def __init__(self,info):
        '''
        info : dict
        info's key :['material' : material, 'duct' : dict{'Width', 'Depth', 'Height}]'''
        self.material=info['material']
        self.cnodition=None
        self.duct=info['duct']
        self.Area=self.duct['Width']*self.duct['Height']

    def friction(self,surf='Iron'):
        v=self.condition['velocity']
        L=2*self.duct['Width']*self.duct['Height']/(self.duct['Width']+self.duct['Height'])
        Re=v*L*self.condition['fluid'].Density/self.condition['fluid'].Viscosity
        re=epsilon[surf]/L

        x=sympy.Symbol('x')
        r=sympy.Symbol('r')
        f=(-2*log(r/3.7065-5.0272/x*log(r/3.827-4.567/x*log((r/7.7918)**0.9924+(5.3326/(208.815+x))**0.9345,10),10),10))**-2
        df=sympy.diff(f,x)

        if(Re<2000):
            return 64/Re
        elif(Re>3000):
            return f.subs([(x,Re),(r,re)]).evalf()
        else:
            A=np.array([[2000**3,2000**2,2000,1],
                        [3000**3,3000**2,3000,1],
                        [3*2000**2,2*2000,1,0],
                        [3*3000**2,2*3000,1,0]])
            B=np.array([64/2000,f.subs([(x,3000),(r,re)]).evalf(),-64/(2000**2),df.subs([(x,3000),(r,re)]).evalf()]).reshape(-1,1)
            [a,b,c,d]=np.dot(np.linalg.inv(A),B).reshape(-1)
            return a*Re**3+b*Re**2+c*Re+d

    def Thermal_Resistance(self):
        v=self.condition['velocity']
        Pr=self.condition['fluid'].Viscosity*self.condition['fluid'].Specificheat/self.condition['fluid'].Conductivity
        f_Pr=0.564/(1+(1.1664*Pr**(1/6))**4.5)**(2/9)
        L=2*self.duct['Width']*self.duct['Height']/(self.duct['Width']+self.duct['Height'])
        Re_L=v*L*self.condition['fluid'].Density/self.condition['fluid'].Viscosity
        z_star=self.duct['Depth']/(L*Re_L*Pr)
        Nu_l=4/z_star*f_Pr
        h=Nu_l*self.condition['fluid'].Conductivity/L
        return 1/(h*self.duct['Width']*self.duct['Height'])