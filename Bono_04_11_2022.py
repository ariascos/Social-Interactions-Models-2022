# Bono 4/11/2022 MIS

import numpy as np
import itertools as it

def v(subset,N):
    l = len(subset)
    n = len(N)
    if l>n/2:
        return 1
    else:
        return 0 

def veto(subset,N,j_veto = 0):
    if j_veto in subset:
        l = len(subset)
        n = len(N)
        if l>n/2:
            return 1
        else:
            return 0
    else:
        return 0
    
def correciones(tams,tamn):
    Num = (np.math.factorial(tams))*(np.math.factorial(tamn-tams-1))
    Den = np.math.factorial(tamn)
    return Num/Den

def shapley_value(i,N,value_fun):
    M = N.copy()
    M.pop(M.index(i))
    subsets = []
    for k in range(len(M)):
        subsets +=[list(j) for j in it.combinations(M,k)]
    sv = 0
    l0 = len(N)
    for subset in subsets:
        l1 = len(subset)
        sub1 = subset + [i]
        #print(subset,type(subset))
        #print(sub1)
        #print('.'*30)
        correccion = correciones(l1,l0)
        sv += (value_fun(sub1,N)-value_fun(subset,N))*correccion
    return sv

Jugadores = [u for u in range(10)]
Shapley_Values_Jugadores = {i:shapley_value(i,Jugadores,v) for i in Jugadores}
Shapley_Values_Jugadores_Veto = {i:shapley_value(i,Jugadores,veto) for i in Jugadores}

for i in Jugadores:
    print('El valor de Shapley para {} es {}'.format(i,shapley_value(i,Jugadores,v)))





