# import win32com.client
# from win32com.client import gencache, Dispatch, constants, DispatchEx

# invapp=win32com.client.Dispatch("Inventor.Application")
# invapp.Visible=True
# mod=gencache.EnsureModule('{D98A091D-3A0F-4C3E-B36E-61F62068D488}',0,1,0)
# invapp=mod.Application(invapp)
# Doc=invapp.ActiveDocument
# Doc=mod.PartDocument(Doc)
# # Doc=mod.AssemblyDocument(Doc)
# prop=invapp.ActiveDocument.PropertySets.Item("Design Tracking Properties")

import TEG.Module
import TEG.heatsink
import TEG.material
import TEG.TEM

from copy import deepcopy

from sympy import diff
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

var=[]
eqn=0

ratio=[]

for R in result:
    var.append(list(R['various'].values()))
    for i in range(2):
        eqn+=(R['equation'][i])**2
    ratio.append(R['ratio'])

x=[]
r=[]

for pred in var:
    for i in pred:
        x.append(i)

print(x)