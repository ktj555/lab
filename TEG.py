import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import time
import random

alpha=0.123 ; k=1.5 ; C_c=264.17694 ; C_h=21.1768 ; R_c=0.413119 ; R_h=0.684

def find_Th(T_cin,T_cout):
    
    a,b,c=-7.9148e-6*391/161, 0.00502*391/161, 1.630327*391/161
    
    q_c = C_c*(T_cout-T_cin)
    T_TEGc = (T_cin+T_cout)/2+q_c*R_c
    ax,bx,cx,dx=k*a,k*b+alpha**2/8-q_c*a,k*c+alpha**2/2*T_TEGc-q_c*b,-q_c*c
    
    error=1e-10
    
    def f(x):
        return ax*x**3+bx*x**2+cx*x+dx
    
    def df(x):
        return 3*ax*x**2+2*bx*x+cx

    x=0
    
    while(math.fabs(f(x))>error):
        x-=f(x)/df(x)

    T_TEGh=T_TEGc+x
    R_in=a*x**2+b*x+c
    I=alpha*x/(2*R_in)

    q_h=alpha*I*T_TEGh+k*x-0.5*I**2*R_in
    T_hin=T_TEGh+q_h*(1/(2*C_h)+R_h)
    T_hout=T_TEGh+q_h*(-1/(2*C_h)+R_h)
    
    return T_hin,T_hout

def first_section(T_cin,T_cout):
    T_hin,T_hout=find_Th(T_cin,T_cout)
    
    temp={'T_cin':T_cin,
         'T_cout':T_cout,
         'T_hin':T_hin,
         'T_hout':T_hout}
    return temp

def other_section(T_cin,T_hout):
    T_cout1=T_cin+0.5
    T_cout2=T_cin+0.6
    error=1e-7
    E2=1
    while(math.fabs(E2)>error):
        E1=T_hout-find_Th(T_cin,T_cout1)[1]
        E2=T_hout-find_Th(T_cin,T_cout2)[1]
        T_cout3=T_cout1-(T_cout2-T_cout1)/(E2-E1)*E1
        T_cout1=T_cout2
        T_cout2=T_cout3
    temp={'T_cin':T_cin,
         'T_cout':T_cout2,
         'T_hin':find_Th(T_cin,T_cout2)[0],
         'T_hout':T_hout}
    return temp

def last_section(T_cin,T_hout,T_hin):
    T_cout1=T_cin+0.5
    T_cout2=T_cin+0.6
    error=1e-7
    E2=1
    while(math.fabs(E2)>error):
        E1=T_hout-find_Th(T_cin,T_cout1)[1]
        E2=T_hout-find_Th(T_cin,T_cout2)[1]
        T_cout3=T_cout1-(T_cout2-T_cout1)/(E2-E1)*E1
        T_cout1=T_cout2
        T_cout2=T_cout3
    temp={'T_cin':T_cin,
         'T_cout':T_cout2,
         'T_hin':find_Th(T_cin,T_cout2)[0],
         'T_hout':T_hout}
    ERROR=T_hin-temp['T_hin']
    return temp, ERROR

def calculate_section(T_cin,T_hin,T_cout_p,num_section):
    temp=[first_section(T_cin,T_cout_p)]
    for i in range(2,num_section):
        temp.append(other_section(temp[i-2]['T_cout'],temp[i-2]['T_hin']))
    temp.append(last_section(temp[num_section-2]['T_cout'],temp[num_section-2]['T_hin'],T_hin)[0])
    return temp, last_section(temp[num_section-2]['T_cout'],temp[num_section-2]['T_hin'],T_hin)[1]

def sort_temp(temp):
    n=len(temp)
    T_c=[temp[i]['T_cin'] for i in range(n)]
    T_c.append(temp[n-1]['T_cout'])
    T_h=[temp[i]['T_hout'] for i in range(n)]
    T_h.append(temp[n-1]['T_hin'])
    return T_c,T_h

def predict_section(T_cin,T_hin,num_section,first_pred,lamda):
    ERROR=1e-10
    T_cout_pf=first_pred
    temp,error=calculate_section(T_cin,T_hin,T_cout_pf,num_section)
    MSE=error**2
    p_and_E_list=[[T_cout_pf,MSE]]
    step=1e-3
    h=step
    i=1
    while(MSE>ERROR):
        T_cout_pf2=T_cout_pf+h
        temp2,error2=calculate_section(T_cin,T_hin,T_cout_pf2,num_section)
        MSE2=error2**2
        delMSE=(MSE2-MSE)/h
        T_cout_pf-=delMSE/math.fabs(delMSE)*step
        temp,error=calculate_section(T_cin,T_hin,T_cout_pf,num_section)
        MSE=error**2
        print("repeat "+str(i)+"th complete")
        i+=1
        T_c,T_h=sort_temp(temp)
        print("T_c:",T_c)
        print("T_h",T_h)
        print("MSE:",MSE)
        print('='*100)
        p_and_E_list.append([T_cout_pf,MSE])
        if(i>2):
            if(p_and_E_list[-1][1]>=p_and_E_list[-2][1]):
                step*=lamda
                h=step
    return p_and_E_list

T_cin=301.92936 # True
T_hin=550.88912
n=5

# m=100

# nn=30

# Time=[[] for i in range(1,10)]
# st=[]
# for i in range(nn):

#     list_T_cin=[300+random.randrange(-50,50)/10 for i in range(m)]
#     j=0
#     for lamda in [i/10 for i in range(1,10)]:

#         print("lamda :",lamda)

#         for T_cin in list_T_cin:

#             start_time=time.time()
#             record=predict_section(T_cin,T_hin,n,T_cin,lamda)
#             end_time=time.time()

#             st.append(end_time-start_time)

#             # x=len(record)

#             # T_cout=[record[i][0] for i in range(x)]
#             # T_c,T_h=sort_temp(calculate_section(T_cin,T_hin,T_cout[-1],n)[0])

#             # print("Time :",end_time-start_time,"sec")
#             # print("T_h :",T_h)
#             # print("T_c :",T_c)
#             # print('-'*100)
#         Time[j].append(st)
#         j+=1
#         print("least time :",np.array(st).min())
#         print("max time :",np.array(st).max())
#         print("average time :",np.array(st).mean())
#         print('='*100)
#         st=[]

# data=pd.DataFrame(Time,index=[i/10 for i in range(1,10)],columns=['data'+str(i) for i in range(1,nn+1)])

# data.to_csv("Time_result.csv")

record=predict_section(T_cin,T_hin,n,T_cin,0.5)

x=len(record)

T_cout=[record[i][0] for i in range(x)]
MSE=[record[i][1] for i in range(x)]

x=[i for i in range(1,x+1)]

T_c,T_h=sort_temp(calculate_section(T_cin,T_hin,T_cout[-1],n)[0])

T=pd.DataFrame([T_c,T_h],columns=[1,2,3,4,5,6],index=['T_c','T_h'])
T.to_csv('temperature.csv')

n=np.arange(1,n+2)

plt.figure(1)
plt.plot(x,T_cout,label='T_cout')
plt.legend()
plt.figure(2)
plt.plot(x,MSE,label='MSE')
plt.legend()
plt.figure(3)
plt.plot(n,T_c,label='T_c')
plt.plot(n,T_h,label='T_h')
plt.legend()
plt.show()