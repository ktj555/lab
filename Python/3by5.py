import TEG.Module
import TEG.heatsink
import TEG.material
import TEG.TEM

iron=TEG.material.Solid({'Density':7874,'Temperature':300,'Conductivity':202.4*4200/3600,'Specificheat':0.107*4.2*1000})
water=TEG.material.Fluid({'Density':998,'Temperature':300,'Conductivity':0.5918*4200/3600,'Specificheat':4184,'Viscosity':0.7670*1e-3,'Pressure':101.325})
Air=TEG.material.Fluid({'Density':1.2,'Temperature':500,'Conductivity':0.025*4200/3600,'Specificheat':1030,'Viscosity':1.79e-5,'Pressure':101.325})
PN=TEG.material.SemiConductor({'Seebeck':lambda x:0.123,'Conductivity':lambda x:1.25,'Resistance':lambda x:-7.9148e-6*391/161*x**2+0.00502*391/161*x+1.630327*391/161,
                                'Seebecktype':'constant','Conductivitytype':'constant','Resistancetype':'diff'})
heatsink1=TEG.heatsink.Plate_fin({'material':iron,'base':{'Width':0.06,'Height':0.003,'Depth':0.06},'fin':{'Width':0.002,'Height':0.025,'N_fin':9,'Side':0.0024}})
heatsink2=TEG.heatsink.Plate_fin({'material':iron,'base':{'Width':0.06,'Height':0.003,'Depth':0.06},'fin':{'Width':0.002,'Height':0.025,'N_fin':9,'Side':0.0024}})
TEM1=TEG.TEM.TEM({'PN_couple':PN,'config':{'Width':0.06,'Depth':0.06,'Height':0.0033}})

Model=TEG.Module.Module({'TEM':TEM1,'Hot_side_heatsink':heatsink1,'Cold_side_heatsink':heatsink2})