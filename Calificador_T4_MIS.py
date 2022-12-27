#----------------------------------------#
#         Calificador Taller 4           #
#                  MIS                   #
#    Mateo Alejandro Rodríguez Ramírez   #
#----------------------------------------#

import os
import itertools as it
import networkx as nx
import numpy as np
directorio = r'C:\Users\mateo\OneDrive\Desktop\MATEO\TRANSITORIO\Personal\2022_2\Complementarias\MIS'
os.chdir(directorio)

import Solucion_T4_MIS as MSOL
import Solucion_T4_MIS as SSOL
import networkx as nx


#-------------------------------------------
# Punto 1
G = nx.DiGraph()
G.add_edges_from([('A','C'),('A','D'),('A','B'),('B','D'),('B','E'),('C','F'),('D','F'),('D','G'),
('E','G'),('F','G')])
nx.set_edge_attributes(G,{('A','C'):5,('A','D'):3,('A','B'):1,('B','D'):9,('B','E'):6,('C','F'):2,('D','F'):4,('D','G'):8,
('E','G'):4,('F','G'):1},'costos')
GG = G.copy()

MSOL.bellman_caminos_cortos(G,'A','G')
nodos = dict(G.nodes)
att = 'asignacion'
for nodo in nodos:
    print(SSOL.bellman_caminos_cortos(G,'A',nodo))
print(nodos)


#-------------------------------------------
# Punto 2

def prueba_to(tipo):
    if tipo == 'bien':
        G =  nx.DiGraph()
        G.add_edges_from([(0,3),(0,4),(1,3),(1,4),(2,3),(2,4)])
        nx.set_node_attributes(G,{0:'O',1:'O',2:'O',3:'D',4:'D'},'tipo')
        nx.set_node_attributes(G,{0:1000,1:1500,2:1200,3:2300,4:1400},'valor')
        nx.set_edge_attributes(G,{(0,3):1000,(0,4):2690,(1,3):1250,(1,4):1350,(2,3):1275,(2,4):850},'costos')
    elif tipo == 'eo':
        G =  nx.DiGraph()
        G.add_edges_from([(0,3),(0,4),(1,3),(1,4),(2,3),(2,4)])
        nx.set_node_attributes(G,{0:'O',1:'O',2:'O',3:'D',4:'D'},'tipo')
        nx.set_node_attributes(G,{0:1100,1:1600,2:1300,3:2300,4:1400},'valor')
        nx.set_edge_attributes(G,{(0,3):1000,(0,4):2690,(1,3):1250,(1,4):1350,(2,3):1275,(2,4):850},'costos')
    elif tipo == 'ed':
        G =  nx.DiGraph()
        G.add_edges_from([(0,3),(0,4),(1,3),(1,4),(2,3),(2,4)])
        nx.set_node_attributes(G,{0:'O',1:'O',2:'O',3:'D',4:'D'},'tipo')
        nx.set_node_attributes(G,{0:1000,1:1500,2:1200,3:2400,4:1800},'valor')
        nx.set_edge_attributes(G,{(0,3):1000,(0,4):2690,(1,3):1250,(1,4):1350,(2,3):1275,(2,4):850},'costos')
    return G

att = 'transferencia'
no_sigue = False
embarrada = []
for tipo in ['bien','eo']:
    G = prueba_to(tipo)
    GG = G.copy()
    MOPT = MSOL.transporte_optimo(G)
    SOPT = SSOL.transporte_optimo(GG)
    EM = dict(MOPT.edges)
    ES = dict(SOPT.edges)
    for i in EM:
        if i in ES:
            if abs(EM[i][att]-ES[i][att])>=(1/100):
                print('Fallo')
                no_sigue = True
                embarrada+=[tipo]
                break
        else:
            print('Fallo')
            no_sigue = True
            embarrada+=[tipo]
            break
    if no_sigue:
        break

if no_sigue==False:
    print('Bien el punto')
else:
    print('Mal el punto')
print(embarrada)

G = prueba_to('ed')
SSOL.transporte_optimo(G)



#-------------------------------------------
# Punto 3