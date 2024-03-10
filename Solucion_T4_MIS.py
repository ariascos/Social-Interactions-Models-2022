#----------------------------------------#
#           Solución Taller 4            #
#                  MIS                   #
#    Mateo Alejandro Rodríguez Ramírez   #
#----------------------------------------#

#----------------------------------------
# Cargue de paquetes
import networkx as nx
import numpy as np
import pandas as pd
import itertools as it 
import matplotlib.pyplot as plt

# Importar la librería de Google OR-Tools
from ortools.linear_solver import pywraplp

#----------------------------------------
# Punto 1: Caminos más Cortos

def revision_bcc(grafo,source,target):
    retorna = False
    if source in grafo:
        if target in grafo:
            retorna = True
    return retorna

def optimizador(red,source,target,begin=True):
    att1 = 'asignacion'
    att2 = 'costos'
    if begin:
        hojas = [i for i in red.nodes if (list(red.successors(i))==0)]
        for hoja in hojas:
            red.nodes[hoja][att1] = ([],np.infty)
        red.nodes[target][att1] = ([],0) # (nodo_siguiente,value)
    if source != target:
        predecesores = list(red.predecessors(target))
        for predecesor in predecesores:
            sucesores = list(red.successors(predecesor))
            pasa = True
            for i in sucesores:
                if red.nodes[i][att1] is None:
                    pasa = False
                    break
            if pasa:
                costo_elegido = np.inf
                nodos_elegidos = []
                for nodo in sucesores:
                    costo_enlace = red.edges[(predecesor,nodo)][att2]
                    costo_acumulado = red.nodes[nodo][att1][1]
                    ct = costo_enlace + costo_acumulado
                    if ct<costo_elegido:
                        costo_elegido = ct
                        nodos_elegidos = [nodo]
                    elif ct==costo_elegido:
                        nodos_elegidos += [nodo]
                red.nodes[predecesor][att1] = (nodos_elegidos,costo_elegido)
        for predecesor in predecesores:
            optimizador(red,source,predecesor,False)

def bellman_caminos_cortos(red,source,target):
    if revision_bcc(red,source,target):
        att1 = 'asignacion'
        nx.set_node_attributes(red,{i:None for i in red.nodes},att1)
        optimizador(red,source,target,True)
    else:
        raise Exception('Source o Target no están en el grafo')

# Ejemplo:
#G = nx.DiGraph()
#G.add_edges_from([('A','C'),('A','D'),('A','B'),('B','D'),('B','E'),('C','F'),('D','F'),('D','G'),
#('E','G'),('F','G')])
#nx.set_edge_attributes(G,{('A','C'):5,('A','D'):3,('A','B'):1,('B','D'):9,('B','E'):6,('C','F'):2,('D','F'):4,('D','G'):8,
#('E','G'):4,('F','G'):1},'costos')

# Prueba:
#optimizador(G,'A','G',True)
#bellman_caminos_cortos(G,'A','G')
#dict(G.nodes)

#----------------------------------------
# Punto 2: Juegos de Transporte

#list(nx.all_simple_paths(G,'A','G'))

#----------------------------------------
# Punto 3: Flujos de Transporte

def creador_matriz_costos(red):
    att1 = 'tipo'
    att2 = 'costos'
    nodos = dict(red.nodes)
    enlaces = dict(red.edges)
    orden_of = {}
    orden_de = {}
    cont_of = 0
    cont_de = 0
    total_of = len([1 for i in nodos.values() if i[att1]=='O'])
    total_de = len(nodos)-total_of
    matriz = np.zeros((total_of,total_de))
    #print(matriz)
    for nodo in nodos:
        if nodos[nodo][att1] == 'O':
            orden_of[cont_of] = nodo
            cont_of += 1
        else:
            orden_de[cont_de] = nodo
            cont_de += 1
    for pos_of in orden_of:
        for pos_de in orden_de:
            oferente = orden_of[pos_of]
            demandante = orden_de[pos_de]
            matriz[pos_of][pos_de] = enlaces[(oferente,demandante)][att2]
    #print(matriz)
    return matriz,orden_of,orden_de


def transporte_optimo(red):
    #att1 = 'tipo'    
    att1 = 'valor'
    att2 = 'transferencia'
    #att2 = 'costos'
    nodos = dict(red.nodes)
    # Creación de la matrix de costos e identificación de los productores
    matriz,orden_of,orden_de = creador_matriz_costos(red)
    # Declarar el solucionador que abordará el modelo
    solver = pywraplp.Solver.CreateSolver('SCIP')
    # Variables del modelo
    x = {}
    for i in orden_of:
        for j in orden_de:
            x[i, j] = solver.IntVar(0, solver.infinity(), '')
    # Restricciones de oferta
    for i in orden_of:
        solver.Add(solver.Sum([x[i, j] for j in orden_de]) <= nodos[orden_of[i]][att1]) 
    # Restricciones de demanda
    for j in orden_de:
        solver.Add(solver.Sum([x[i, j] for i in orden_of]) >= nodos[orden_de[j]][att1])
    # Función objetivo con criterio de optimización: minimizar
    objective_terms = []
    for i in orden_of:
        for j in orden_de:
            costo_enlace = matriz[i][j]
            objective_terms.append(costo_enlace*x[i,j])
    solver.Minimize(solver.Sum(objective_terms))

    # Invoca el solucionador
    status = solver.Solve()

    # Se crea la nueva red:

    red1 = red.copy()
    enlaces = dict(red1.edges)
    nx.set_edge_attributes(red1,{i:-1 for i in enlaces},att2)

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    #    print('Costo total = ', solver.Objective().Value(), '\n')

        for i in orden_of:
            for j in orden_de:
                of = orden_of[i]
                de = orden_de[j]
                if x[i, j].solution_value()<=0:
                    red1.remove_edges_from([(of,de)])
                else:
                    red1.edges[(of,de)][att2] = x[i, j].solution_value()
        return red1

    #            print('|{:^20} -> {:^20} | Cantidad: {:^20}|'.format(
    #            orden_of[i],
    #            orden_de[j],
    #            x[i, j].solution_value())) 
    else:
        raise Exception('Imposible realizar la optimización')

# Ejemplo
#G =  nx.DiGraph()
#G.add_edges_from([(0,3),(0,4),(1,3),(1,4),(2,3),(2,4)])
#nx.set_node_attributes(G,{0:'O',1:'O',2:'O',3:'D',4:'D'},'tipo')
#nx.set_node_attributes(G,{0:1000,1:1500,2:1200,3:2300,4:1400},'valor')
#nx.set_edge_attributes(G,{(0,3):1000,(0,4):2690,(1,3):1250,(1,4):1350,(2,3):1275,(2,4):850},'costos')
#nx.draw(G,with_labels = True)
#plt.show()

# Prueba:
#transporte_optimo(G)