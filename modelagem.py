#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 04:20:34 2019

@author: laura
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
  
def edp_model(y, t, *args):
    Vmax = args[0]
    km = args[1]
    St = args[2]
    P = y[0]
    S = St - P
     
    dP = Vmax * (S / (S+km))
    return dP
 
# Parameters MM
Vmax = 1
km = 3
St = 10
mm_params = (Vmax, km, St)
 
  
# Initial Conditions MM
P_0 = 0
  
# Timesteps
n_steps = 100
t = np.linspace(0, 50, n_steps)
  
num_P = odeint(edp_model, P_0, t, args = (mm_params)).flatten()

# Create experimental data.  Just take the regular simulation data and add some gaussian noise to it.
exp_P=[0,2,3.8,5.4,7,7.5,9.2,9,10.1,9.4,9.4,9.1,10.2,10.3,9,10,8.9,9.5,10,10.2]

plt.plot(t[::5], exp_P, 'ro')
plt.xlabel('Time')
plt.ylabel('Product Concentration')
plt.legend(['Experimental Data'], loc = 'best')
plt.show()

def residuals(p):
    p = tuple(p)
    sim_P = odeint(edp_model, P_0, t, args = p).flatten()
    res = sim_P[::5] - exp_P
    return res.flatten()

    
from scipy.optimize import leastsq
initial_guess = [1, 2, 5]
fitted_params = leastsq(residuals, initial_guess)[0]

print('initial_guess')
print('Vmax = ',initial_guess[0])
print('Km = ',initial_guess[1])
print('St = ',initial_guess[2])

print(' ')

print('fitted_params')
print('Vmax = ',fitted_params[0])
print('Km = ',fitted_params[1])
print('St = ',fitted_params[2])

#plt.plot(t[::5], exp_P, 'ro')
#plt.plot(t, odeint(edp_model, P_0, t, args = tuple(fitted_params)), 'b-')
#plt.legend(['Experimental Data' , 'Fitted Parameters'], loc = 'best')
#plt.xlabel('Time')
#plt.ylabel('Product Concentration')


#################################################
#################################################
num = len(exp_P)

vP = np.zeros(num-1)

for i in range(num-1):
    vP[i] = exp_P[i+1] - exp_P[i]


print(num,len(t[::5]),len(exp_P))
a2, a1, a0 = np.polyfit(exp_P[:num-1], vP,2)
print(a2,a1,a0)

curvaP = a2*t**2 + a1*t + a0

Pn = np.zeros(num)
Pn[0] = 0
print("*******",exp_P[0])
for k in range(0,num-1):
    Pn[k+1] = a2*Pn[k]**2 + a1*Pn[k] + a0 + Pn[k]






#plt.scatter(exp_P[:num-1],vP)
#plt.plot(t[:22],curvaP[:22])
plt.scatter(t[::5],Pn,c='r')
plt.scatter(t[::5],exp_P,c='b')







plt.show()