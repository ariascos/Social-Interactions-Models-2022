#----------------------------------------#
#         Calificador Taller 3           #
#                  MIS                   #
#    Mateo Alejandro Rodríguez Ramírez   #
#----------------------------------------#

import os
import itertools as it
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
directorio = r'C:\Users\mateo\OneDrive\Desktop\MATEO\TRANSITORIO\Personal\2022_2\Complementarias\MIS'
os.chdir(directorio)

import Solucion_T3_MIS as MSOL
#import T3_201618789_201923192_201728877_201616830 as SSOL
import T3_202013547_200520722_201815146_20122801 as SSOL
import networkx as nx

#-------------------------------------------
# Punto 1
Calif1 = [1 for i in range(6)]
def pp_0():
    G0 = nx.Graph()
    G0.add_edges_from([(1,2),(1,3),(2,3),(2,4),(4,5),(4,6),(4,7),(5,6),(6,7)])
    G0 = G0.to_directed()
    return G0
def pp_1():
    G1 = nx.Graph()
    G1.add_edges_from([(0,1),(0,2),(0,3),(1,2),(2,3),(1,4),(1,5),(0,5),(3,6),(3,7),(4,8),(4,9),(5,9),(5,10),(6,10),(7,10),(8,11),(9,11),(10,11)])
    G1 = G1.to_directed()
    return G1
# 1.1:
G0 = pp_0()
G1 = G0.copy()
#G1 = pp_1()

no_sigue = False 
for red in [G0,G1]:
    for nodo in red.nodes:
        MRed = MSOL.gn_p1(nodo,red)
        SRed = SSOL.gn_p1(nodo,red)
        if nx.is_isomorphic(MRed,SRed):
            pass
        else:
            SRed = SRed.to_directed()
            MRed = MRed.to_directed()
            if nx.is_isomorphic(MRed,SRed):
                pass
            else:
                Calif1[0] = 0
                no_sigue = True
                break
    if no_sigue:
        break

Calif1
# 1.2:
G0 = pp_0()
G1 = G0.copy()
#G1 = pp_1()
no_sigue = False 
att = 'n_caminos'
for red in [G0,G1]:
    for i in list(red.nodes):
        arbol = MSOL.gn_p1(i,red)
        A = MSOL.gn_p2(i,arbol)
        B = SSOL.gn_p2(i,arbol)
        #nx.draw(A)
        #plt.show()
        print(A is None)
        print(B is None)
        DA = dict(A.nodes)
        DB = dict(B.nodes)
        for nodo in DA:
            if nodo in DB:
                if DA[nodo][att] != DB[nodo][att]:
                    Calif1[1] = 0 
                    no_sigue = True
                    break   
            else:
                Calif1[1] = 0
                no_sigue = True
                break
        if no_sigue:
            break
    if no_sigue:
        break
Calif1
# 1.3:
G0 = pp_0()
G1 = G0.copy()
#G1 = pp_1()
no_sigue = False 
att = 'pesos'
for red in [G0,G1]:
    for i in list(red.nodes):
        dicccionario1 = {i:False for i in G0.nodes}
        dicccionario1 [i] = True
        nx.set_node_attributes(G0,dicccionario1,'root')
        print('Pasa mio')
        nx.set_node_attributes(G1,dicccionario1,'root')
        arbol = MSOL.gn_p1(i,red)
        A = MSOL.gn_p3(i,arbol)
        B = SSOL.gn_p3(i,arbol)
        print(A is None)
        print(B is None)
        DA = dict(A.nodes)
        DB = dict(B.nodes)
        for nodo in DA:
            if nodo in DB:
                if DA[nodo][att] != DB[nodo][att]:
                    Calif1[2] = 0 
                    no_sigue = True
                    break   
            else:
                Calif1[2] = 0
                no_sigue = True
                break
        if no_sigue:
            break
    if no_sigue:
        break

Calif1

# 1.4:
G0 = pp_0()
G1 = G0.copy()
#G1 = pp_1()
no_sigue = False 
att = 'e_pesos'
for red in [G0,G1]:
    red_C = red.copy()
    MSOL.gn_peso_enlace(red)
    SSOL.gn_peso_enlace(red_C)
    DM = dict(red.edges)
    DS = dict(red_C.edges)
    for enlace in DM:
        if enlace in DS:
            if DM[enlace][att] != DS[enlace][att]:
                Calif1[3] = 0
                no_sigue = True
                break
    if no_sigue:
        break
Calif1

# 1.5:
G0 = pp_0()
#MSOL.gn_peso_enlace(G0)
#dict(G0.edges)
G1 = G0.copy()
#G1 = pp_1()
att = "e_pesos"
no_sigue = False
for umbral in [10,13,16,20]:
    for red in [G0,G1]:
        MSOL.gn_peso_enlace(red)
        red_C = red.copy()
        RM = MSOL.gn_comunidades(red,att,umbral)
        RS = SSOL.gn_comunidades(red_C,att,umbral)
        #RM.to_undirected()
        #RS.to_undirected()
        EM = dict(RM.edges)
        ES = dict(RS.edges)
        for enlace in EM:
            if enlace in ES:
                if EM[enlace][att] != ES[enlace][att]:
                    Calif1[4] = 0
                    no_sigue = True
                    break
        if no_sigue:
            break
    if no_sigue:
        break
Calif1

# 1.6:

if no_sigue:
    Calif1[5] = 0

Calif1


#-------------------------------------------
# Punto 2

Calif2 = [1 for i in range(4)]

# Pruebas
def probador():
    G = nx.Graph()
    {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'J':8,'K':9,'L':10,'M':11,'N':12}
    G.add_edges_from([('A','B'),('A','C'),('A','D'),('A','E'),('A','F'),('B','H'),('B','L'),('B','M'),('B','N'),('C','D'),('C','E'),('C','F'),('D','E'),('F','G'),('F','J'),('G','J'),('G','H'),('G','K'),('H','K'),('H','L'),('L','M'),('L','N'),('M','N')])
    diccionario = {('A','B'):False,('A','C'):True,('A','D'):True,('A','E'):True,('A','F'):False,('B','H'):False,('B','L'):True,('B','M'):True,('B','N'):True,('C','D'):True,('C','E'):True,('C','F'):False,('D','E'):False,('F','G'):True,('F','J'):True,('G','J'):True,('G','H'):False,('G','K'):False,('H','K'):True,('H','L'):False,('L','M'):True,('L','N'):True,('M','N'):False}
    nx.set_edge_attributes(G,diccionario,'relacion')
    G = G.to_directed()
    return G

G = probador()
GG = G.copy()
MSOL.cp_puentes(G)
SSOL.cp_puentes(GG)

MSOL.cp_ctf(G)
SSOL.cp_ctf(GG)

EM = dict(G.edges) 
ES = dict(GG.edges)

NM = dict(G.nodes)
NS = dict(GG.nodes)

# 2.1:
att = "puente"
for enlace in EM:
    if enlace in ES:
        if EM[enlace][att] != ES[enlace][att]:
            Calif2[0] = 0
            break
    elif (enlace[1],enlace[0]) in ES:
        enlace1 = (enlace[1],enlace[0])
        if EM[enlace][att] != ES[enlace1][att]:
            Calif2[0] = 0
            break
    else:
        Calif2[0] = 0
        break

Calif2




# 2.2:
att = "ctf"
for nodo in EM:
    if nodo in ES:
        if EM[nodo][att] != ES[nodo][att]:
            Calif2[1] = 0
            break
    else:
        Calif2[1] = 0
        break

Calif2

# 2.3:

RTAM = MSOL.cp_revision(G)
RTAS = SSOL.cp_revision(G)
if RTAM != RTAS:
    Calif2[2] = 0

Calif2

# 2.4:

G = probador()
GG = G.copy()
RTAM = MSOL.cp_construccion(G)
RTAS = SSOL.cp_construccion(GG)
if RTAM != RTAS:
    Calif2[3] = 0

Calif2


