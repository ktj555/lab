from TEG.heatsink import *
from sympy import Symbol, diff, simplify
import time

class Module:
    def __init__(self,info):
        '''
        info : dict
        info's key : ['TEM':TEM, *'Hot_side_heatsink':heatsink, *'Cold_side_heatsink':heatsink]'''
        self.TEM=info['TEM']
        self.Hot_side_heatsink=None
        self.Cold_side_heatsink=None

        key_list=list(info.keys())
        if('Hot_side_heatsink' in key_list):
            self.Hot_side_heatsink=info['Hot_side_heatsink']
        if('Cold_side_heatsink' in key_list):
            self.Cold_side_heatsink=info['Cold_side_heatsink']

    def inlet(self,hot_side,cold_side):
        '''
        inlet : dict
        inlet's key : ['fluid', 'velocity']'''
        # if(self.Hot_side_heatsink == None):
        #     self.Hot_side_heatsink=Nofin(self.TEM.pn)
        # if(self.Cold_side_heatsink == None):
        #     self.Cold_side_heatsink=Nofin(self.TEM.pn)
        self.Hot_side_heatsink.set_condition(hot_side)
        self.Cold_side_heatsink.set_condition(cold_side)

    def solve(self,h_,c_,error=1e-3,first_step=1,step_decrease=0.5,print_b=False):
        f_h=self.Hot_side_heatsink.friction()
        f_c=self.Cold_side_heatsink.friction()

        # heat analysis

        R_h=self.Hot_side_heatsink.Thermal_Resistance()
        R_c=self.Cold_side_heatsink.Thermal_Resistance()
        C_h=self.Hot_side_heatsink.condition['fluid'].Specificheat*self.Hot_side_heatsink.condition['velocity']*self.Hot_side_heatsink.condition['fluid'].Density*self.Hot_side_heatsink.Area
        C_c=self.Cold_side_heatsink.condition['fluid'].Specificheat*self.Cold_side_heatsink.condition['velocity']*self.Cold_side_heatsink.condition['fluid'].Density*self.Cold_side_heatsink.Area

        if(h_=='in'):
            T_h_in=self.Hot_side_heatsink.condition['fluid'].Temperature
            T_h_out=Symbol('T_h_out')
        else:
            T_h_out=self.Hot_side_heatsink.condition['fluid'].Temperature
            T_h_in=Symbol('T_h_in')

        if(c_=='in'):
            T_c_in=self.Cold_side_heatsink.condition['fluid'].Temperature
            T_c_out=Symbol('T_c_out')
        else:
            T_c_out=self.Cold_side_heatsink.condition['fluid'].Temperature
            T_c_in=Symbol('T_c_in')

        T_TEM_h=0.5*(T_h_in+T_h_out)-R_h*C_h*(T_h_in-T_h_out)
        T_TEM_c=0.5*(T_c_in+T_c_out)+R_c*C_c*(T_c_out-T_c_in)
        del_T=T_TEM_h-T_TEM_c

        if(self.TEM.pn.Seebecktype=='average'):
            T_a=0.5*(T_TEM_h+T_TEM_c)
        elif(self.TEM.pn.Seebecktype=='diff'):
            T_a=del_T
        else:
            T_a=0
        if(self.TEM.pn.Resistancetype=='average'):
            T_R=0.5*(T_TEM_h+T_TEM_c)
        elif(self.TEM.pn.Resistancetype=='diff'):
            T_R=del_T
        else:
            T_R=0
        if(self.TEM.pn.Conductivitytype=='average'):
            T_k=0.5*(T_TEM_h+T_TEM_c)
        elif(self.TEM.pn.Conductivitytype=='diff'):
            T_k=del_T
        else:
            T_k=0

        a=self.TEM.pn.Seebeck
        R=self.TEM.pn.Resistance
        k=self.TEM.pn.Conductivity
        A=self.TEM.config['Area']
        L=self.TEM.config['Height']
        
        I=a(T_a)*del_T*0.5/R(T_R)

        q_h_H=C_h*(T_h_in-T_h_out)
        q_c_H=C_c*(T_c_out-T_c_in)
        q_h_E=a(T_a)*I*T_TEM_h+k(T_k)*A/L*del_T-0.5*I**2*R(T_R)
        q_c_E=a(T_a)*I*T_TEM_c+k(T_k)*A/L*del_T+0.5*I**2*R(T_R)

        eqn1=q_h_H-q_h_E
        eqn2=q_c_H-q_c_E

        ee=error
        Error=1e100
        r_h=C_h/(C_h+C_c)
        step_h=first_step*(1-r_h)
        step_c=first_step*r_h

        if(h_=='in'):
            T_h_pred=T_h_in
        else:
            T_h_pred=T_h_out
        if(c_=='in'):
            T_c_pred=T_c_in
        else:
            T_c_pred=T_c_out

        eqn=(eqn1**2+eqn2**2)**0.5
        if(h_=='in'):
            eqn_h=diff(eqn,T_h_out)
        else:
            eqn_h=diff(eqn,T_h_in)
        if(c_=='in'):
            eqn_c=diff(eqn,T_c_out)
        else:
            eqn_c=diff(eqn,T_c_in)

        i=1

        if(h_=='in'):
            T_h_=T_h_out
        else:
            T_h_=T_h_in
        if(c_=='in'):
            T_c_=T_c_out
        else:
            T_c_=T_c_in

        t_s=time.time()
        if(print_b):
            while(Error>ee):
                last_Error=Error
                Error=eqn.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)])
                print(i,Error,'T_h_pred :',T_h_pred,'T_c_pred :',T_c_pred)
                if(last_Error<Error):
                    step_h*=step_decrease
                    step_c*=step_decrease
                gradient=[eqn_h.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)]),eqn_c.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)])]
                T_h_pred-=step_h*gradient[0]/(gradient[0]**2+gradient[1]**2)**0.5
                T_c_pred-=step_c*gradient[1]/(gradient[0]**2+gradient[1]**2)**0.5
                i+=1
        else:
            while(Error>ee):
                last_Error=Error
                Error=eqn.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)])
                if(last_Error<Error):
                    step_h*=step_decrease
                    step_c*=step_decrease
                gradient=[eqn_h.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)]),eqn_c.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)])]
                T_h_pred-=step_h*gradient[0]/(gradient[0]**2+gradient[1]**2)**0.5
                T_c_pred-=step_c*gradient[1]/(gradient[0]**2+gradient[1]**2)**0.5
                i+=1

        t_f=time.time()

        result={"T_h_pred":T_h_pred,'T_c_pred':T_c_pred,
                'T_TEM_h':T_TEM_h.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)]),'T_TEM_c':T_TEM_c.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)]),
                'I':I.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)]),'W':(q_h_H-q_c_H).subs([(T_h_,T_h_pred),(T_c_,T_c_pred)]),
                'Other':{'Error':{'eqn1':eqn1.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)]),'eqn2':eqn2.subs([(T_h_,T_h_pred),(T_c_,T_c_pred)])},'time cost':t_f-t_s}}
 
        return result

    def return_eqation(self,ID,connect):
        # heat analysis

        R_h=self.Hot_side_heatsink.Thermal_Resistance()
        R_c=self.Cold_side_heatsink.Thermal_Resistance()
        C_h=self.Hot_side_heatsink.condition['fluid'].Specificheat*self.Hot_side_heatsink.condition['velocity']*self.Hot_side_heatsink.condition['fluid'].Density*self.Hot_side_heatsink.Area
        C_c=self.Cold_side_heatsink.condition['fluid'].Specificheat*self.Cold_side_heatsink.condition['velocity']*self.Cold_side_heatsink.condition['fluid'].Density*self.Cold_side_heatsink.Area

        tem={'T_h_in':0,'T_h_out':0,'T_c_in':0,'T_c_out':0}

        pred={}

        for keys,values in connect.items():
            if(values is None):
                tem[keys]=Symbol(keys+'_'+str(ID))
                pred[keys]=tem[keys]
            else:
                tem[keys]=values

        T_h_in=tem['T_h_in']
        T_h_out=tem['T_h_out']
        T_c_in=tem['T_c_in']
        T_c_out=tem['T_c_out']

        T_TEM_h=0.5*(T_h_in+T_h_out)-R_h*C_h*(T_h_in-T_h_out)
        T_TEM_c=0.5*(T_c_in+T_c_out)+R_c*C_c*(T_c_out-T_c_in)
        del_T=T_TEM_h-T_TEM_c

        if(self.TEM.pn.Seebecktype=='average'):
            T_a=0.5*(T_TEM_h+T_TEM_c)
        elif(self.TEM.pn.Seebecktype=='diff'):
            T_a=del_T
        else:
            T_a=0
        if(self.TEM.pn.Resistancetype=='average'):
            T_R=0.5*(T_TEM_h+T_TEM_c)
        elif(self.TEM.pn.Resistancetype=='diff'):
            T_R=del_T
        else:
            T_R=0
        if(self.TEM.pn.Conductivitytype=='average'):
            T_k=0.5*(T_TEM_h+T_TEM_c)
        elif(self.TEM.pn.Conductivitytype=='diff'):
            T_k=del_T
        else:
            T_k=0

        a=self.TEM.pn.Seebeck
        R=self.TEM.pn.Resistance
        k=self.TEM.pn.Conductivity
        A=self.TEM.config['Area']
        L=self.TEM.config['Height']
        
        I=a(T_a)*del_T*0.5/R(T_R)

        q_h_H=C_h*(T_h_in-T_h_out)
        q_c_H=C_c*(T_c_out-T_c_in)
        q_h_E=a(T_a)*I*T_TEM_h+k(T_k)*A/L*del_T-0.5*I**2*R(T_R)
        q_c_E=a(T_a)*I*T_TEM_c+k(T_k)*A/L*del_T+0.5*I**2*R(T_R)

        eqn1=q_h_H-q_h_E
        eqn2=q_c_H-q_c_E

        return {'various':pred,'equation':[simplify(eqn1),simplify(eqn2)],'ratio':[C_c,C_h]}


def sym2fun(sym):
    pass