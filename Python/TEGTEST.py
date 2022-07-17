import TEG.Module
import TEG.heatsink
import TEG.material
import TEG.TEM

from copy import deepcopy
from time import sleep
import time

from sympy import diff, simplify
import sympy
import numpy as np

iron=TEG.material.Solid({'Density':7874,'Temperature':300,'Conductivity':202.4*4200/3600,'Specificheat':0.107*4.2*1000})
water=TEG.material.Fluid({'Density':998,'Temperature':300,'Conductivity':0.5918*4200/3600,'Specificheat':4184,'Viscosity':0.7670*1e-3,'Pressure':101.325})
Air=TEG.material.Fluid({'Density':1.2,'Temperature':550,'Conductivity':0.025*4200/3600,'Specificheat':1030,'Viscosity':1.79e-5,'Pressure':101.325})
PN=TEG.material.SemiConductor({'Seebeck':lambda x:0.123,'Conductivity':lambda x:1.25,'Resistance':lambda x:-7.9148e-6*391/161*x**2+0.00502*391/161*x+1.630327*391/161,
                                'Seebecktype':'constant','Conductivitytype':'constant','Resistancetype':'diff'})
heatsink1=TEG.heatsink.Plate_fin({'material':iron,'base':{'Width':0.06,'Height':0.003,'Depth':0.06},'fin':{'Width':0.002,'Height':0.025,'N_fin':9,'Side':0.0024}})
heatsink2=TEG.heatsink.Nofin({'material':iron,'duct':{'Width':0.06,'Depth':0.06,'Height':0.01}})
TEM1=TEG.TEM.TEM({'PN_couple':PN,'config':{'Width':0.06,'Depth':0.06,'Height':0.0033}})

Model=TEG.Module.Module({'TEM':TEM1,'Hot_side_heatsink':heatsink1,'Cold_side_heatsink':heatsink2})
Model.inlet({'fluid':Air,'velocity':16.3175},{'fluid':water,'velocity':0.1055})

result1=Model.return_eqation(ID=1,connect={'T_h_in':None,'T_h_out':None,'T_c_in':300,'T_c_out':None})
result2=Model.return_eqation(ID=2,connect={'T_h_in':None,'T_h_out':result1['various']['T_h_in'],'T_c_in':result1['various']['T_c_out'],'T_c_out':None})
result3=Model.return_eqation(ID=3,connect={'T_h_in':None,'T_h_out':result2['various']['T_h_in'],'T_c_in':result2['various']['T_c_out'],'T_c_out':None})
result4=Model.return_eqation(ID=4,connect={'T_h_in':None,'T_h_out':result3['various']['T_h_in'],'T_c_in':result3['various']['T_c_out'],'T_c_out':None})
result5=Model.return_eqation(ID=5,connect={'T_h_in':550,'T_h_out':result4['various']['T_h_in'],'T_c_in':result4['various']['T_c_out'],'T_c_out':None})

result=[result1,result2,result3,result4,result5]
 
# var=[]
# key=[]
# eqn=[]

# ratio=[]
# h=1
# for R in result:
#     var.append(list(R['various'].values()))
#     key.append(list(R['various'].keys()))
#     for i in range(2):
#         # eqn+=(sympy.cancel(R['equation'][i]))**2
#         eqn.append(R['equation'][i])
#     ratio.append(R['ratio'])

# x=[]
# r=[]
# for pred in var:
#     for i in pred:
#         x.append(i)

# for i in range(len(key)):
#     for j in key[i]:
#         t,s,o=j.split('_')
#         if(s=='h'):
#             r.append(ratio[i][1])
#         else:
#             r.append(ratio[i][0])

# print('start',time.ctime(time.time()))

# rr=sympy.solve_poly_system(eqn)

# print(rr)

# r=np.array(r)

# df=[diff(eqn,i) for i in x]

# size=200

# step=(r/r.sum())/(((r/r.sum())**2).sum())**0.5
# step=size*(1/step)/(((1/step)**2).sum())**0.5

# l=[[i,400] for i in x]

# error=1e-5
# Error=eqn.subs(l)

# j=1
# d=0

# while(Error>error):
#     if(d>10):
#         step*=1.02
#     gradient=np.array([i.subs(l) for i in df])
#     gradient/=((gradient**2).sum())**0.5
#     gradient*=step
#     for i in range(len(l)):
#         l[i][1]-=gradient[i]
#     last_Error=deepcopy(Error)
#     Error=eqn.subs(l)
#     if(last_Error<Error):
#         step*=0.85
#         d=0
#     j+=1
#     d+=1
#     print(j,'th Error :',Error)
#     print(l)


# print(l)





# # test
# error=1e-3

# T_h_in=550

# T_h_1=550
# T_h_2=545
# T_h_3=0

# Air.Temperature=T_h_1
# for j in range(5):
#     Model.inlet({'fluid':Air,'velocity':16.3175},{'fluid':water,'velocity':0.1055})
#     result=Model.solve(h_='out',c_='in',error=error,first_step=5,step_decrease=0.8)
#     Air.Temperature=result['T_h_pred']
#     water.Temperature=result['T_c_pred']
#     print(j)
# E1=((Air.Temperature-T_h_in)**2)**0.5

# print("first complete")

# i=2

# E2=E1
# while(E2>error):
#     Air.Temperature=T_h_2
#     water.Temperature=300
#     for j in range(5):
#         Model.inlet({'fluid':Air,'velocity':16.3175},{'fluid':water,'velocity':0.1055})
#         result=Model.solve(h_='out',c_='in',error=error,first_step=5,step_decrease=0.8)
#         Air.Temperature=result['T_h_pred']
#         water.Temperature=result['T_c_pred']
#         print(j)
#     E2=((Air.Temperature-T_h_in)**2)**0.5
#     print(i,"th complete. Pred :",Air.Temperature,'Error :',E2)
#     T_h_3=T_h_1-(T_h_2-T_h_1)/(E2-E1)*E1
#     T_h_1=T_h_2
#     T_h_2=T_h_3
#     i+=1

# print(T_h_1)