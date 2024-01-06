#----------------------------------------#
#           Solución Taller 3            #
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

#----------------------------------------
# Punto 1: Betweeness y Girvan-Newman (Recordar: Para grafos NO dirigidos en formato DiGraph)

# 1.1: Generación del "Árbol"

def bfs(nodos,red,arbol,att):
    '''
    -----------------------------------------------
    inputs:
        nodos (list): Listado con los nodos que se agregan en un nivel del recorrido BFS.
        red (nx.DiGraph): El gráfo inicial que se quiere modificar. Este debe contener nodos y un atributo de nodos que 
        permita identificar si un nodo ya fue o no asignado al árbol.
        arbol (nx.DiGraph): Un grafo dirigido que tiene forma de árbol. Valen grafos vacíos.
        att (str): Nombre del atributo que permite identificar si los nodos de red ya han sido asignados.
        
    -----------------------------------------------
    outputs:
        arbol (nx.DiGraph): El árbol deseado.
    '''
    nivel = set()
    for nodo in nodos:
        sucesores = list(red.successors(nodo))
        for i in sucesores:
            if red.nodes[i][att] == False:
                arbol.add_edge(nodo,i)
                nivel = nivel.union({i})
    if nivel == set():
        return arbol
    else:
        for nodo in nivel:
            red.nodes[nodo][att] = True
        #print(nx.get_node_attributes(red,att))
        #fig0 = plt.figure()
        #nx.draw(arbol,with_labels=True)
        #plt.show()
        return bfs(list(nivel),red,arbol,att)
    
def gn_p1(nodo,red):
    '''
    -----------------------------------------------
    inputs:
        nodo (int/str): El identificador de un nodo en red desde el cual se va a construir el árbol BFS.
        red (nx.DiGraph): El gráfo inicial que se quiere modificar. Este debe contener nodos y enlaces.
        
    -----------------------------------------------
    outputs:
        tree (nx.DiGraph): El árbol deseado.
    '''
    atributo = 'asignado'
    red1 = red.copy()
    if nodo in red1:
        arbol = nx.DiGraph()
        arbol.add_node(nodo)
        nx.set_node_attributes(red1,{i:False for i in list(red1.nodes)},atributo)
        red1.nodes[nodo][atributo] = True
        arbol = bfs(nodos=[nodo],red=red1,arbol=arbol,att=atributo)
        del red1
        return arbol
    else:
        print('Please, introduce a node included into the network')
        return None

# 1.2: Número de caminos

def asignador_caminos(root,tree,atribute1 = 'root',atribute2 = 'n_caminos',begin = True):
    '''
    -----------------------------------------------
    inputs:
        root (int): Nodo distinguido que será la raíz del árbol tree
        tree (nx.DiGraph): Un grafo dirigido que tiene forma de árbol. No valen grafos vacíos.
        atribute1 (str): Nombre del atributo de nodo que permite identificar si es raiz o no.
        atribute2 (str): Nombre del atributo de nodo que permite decir cuantos caminos más 
        cortos hay del mismo a la raíz.
        begin (bool): Dice si se está en el nodo raíz del árbol a armar.

    -----------------------------------------------
    outputs:
        No hay.
    '''
    if begin:
        if tree.nodes[root][atribute1] != True:
            raise Exception('Ponga una raíz del árbol')
        else:
            tree.nodes[root][atribute2] = 1
            #print('Nodo({})->{}'.format(root,tree.nodes[root][atribute2]))
    #print('Nodo a evaluar: {}'.format(root))
    sucesores = list(tree.successors(root))
    if len(sucesores) != 0:
        for node in sucesores:
            if tree.nodes[node][atribute2] == -1:
                predecesores = list(tree.predecessors(node))
                prueba = [tree.nodes[node_pred][atribute2]!=-1 for node_pred in predecesores]
                #print(prueba)
                if all(prueba):
                    valores_previos = [tree.nodes[node_pred][atribute2] for node_pred in predecesores]
                    #print(valores_previos)
                    tree.nodes[node][atribute2] = sum(valores_previos)
                    #print('Nodo({})->{}'.format(node,tree.nodes[node][atribute2]))
        for node in sucesores:
            asignador_caminos(node,tree,atribute1,atribute2,False)

def gn_p2(nodo,arbol):
    '''
    -----------------------------------------------
    inputs:
        nodo (int): Nodo distinguido que será la raíz del árbol.
        arbol (nx.DiGraph): Un grafo dirigido que tiene forma de árbol. No valen grafos vacíos.

    -----------------------------------------------
    outputs:
        arbol con el número de caminos más cortos de la raiz a cada uno de sus nodos.
    '''
    att1 = 'root'
    att2 = 'n_caminos'
    nx.set_node_attributes(arbol,{i:False for i in arbol.nodes},att1)
    arbol.nodes[nodo][att1] = True
    nx.set_node_attributes(arbol,{i:-1 for i in arbol.nodes},att2)
    asignador_caminos(nodo,arbol,att1,att2,True)
    return arbol

# 1.3: Peso de los enlaces

def asignador_pesos(root,tree,atribute1 = 'root',atribute2 = 'pesos',atribute3 = 'herencia',atribute4 = 'e_pesos',begin = True):
    '''
    -----------------------------------------------
    inputs:
        root (int): Nodo distinguido que será la raíz del árbol tree
        tree (nx.DiGraph): Un grafo dirigido que tiene forma de árbol. No valen grafos vacíos.
        atribute1 (str): Nombre del atributo de nodo que permite identificar si es raiz o no.
        atribute2 (str): Nombre del atributo de nodo que permite decir cuál es el peso del nodo.
        atribute3 (str): Nombre del atributo de nodo que permite decir cuál es el peso que el 
        nodo puede heredar a sus predecesores.
        atribute4 (str): Nombre del atributo de enlace que permite decir cuál es el peso que el 
        enlace obtiene.
        begin (bool): Dice si se está en el nodo raíz del árbol a armar.

    -----------------------------------------------
    outputs:
        No hay.
    '''
    if begin:
        if tree.nodes[root][atribute1] != True:
            raise Exception('Ponga una raíz del árbol')
        hojas = [leaf for leaf in tree.nodes() if []==list(tree.successors(leaf))]
        for hoja in hojas:
            predecesores = list(tree.predecessors(hoja))
            tree.nodes[hoja][atribute2] = 1
            if len(predecesores) != 0:
                valor_e = 1/(len(predecesores))
                tree.nodes[hoja][atribute3] = valor_e 
                for l in predecesores:
                    tree.edges[(l,hoja)][atribute4] = valor_e
            else:
                tree.nodes[hoja][atribute3] = 0
        for hoja in hojas:
            asignador_pesos(hoja,tree,atribute1,atribute2,atribute3,atribute4,False)
    else:
        sucesores = list(tree.successors(root))
        prueba = [tree.nodes[node_succ][atribute2]!=-1 for node_succ in sucesores]
        if all(prueba):
            tree.nodes[root][atribute2] = sum([tree.nodes[node_succ][atribute3] for node_succ in sucesores])+1
            predecesores = list(tree.predecessors(root))
            if len(predecesores)!=0: 
                valor_e = (tree.nodes[root][atribute2])/(len(predecesores))
                tree.nodes[root][atribute3] = valor_e
                for node in predecesores:
                    tree.edges[(node,root)][atribute4] = valor_e
                    asignador_pesos(node,tree,atribute1,atribute2,atribute3,atribute4,False)
            else:
                tree.nodes[root][atribute3] = tree.nodes[root][atribute2]

def gn_p3(nodo,arbol):
    '''
    -----------------------------------------------
    inputs:
        nodo (int): Nodo distinguido que será la raíz del árbol.
        arbol (nx.DiGraph): Un grafo dirigido que tiene forma de árbol. No valen grafos vacíos.

    -----------------------------------------------
    outputs:
        arbol con los pesos de cada uno de los enlaces.
    '''
    att0 = 'root'
    att1 = 'pesos'
    att2 = 'herencia'
    att3 = 'e_pesos'
    nx.set_node_attributes(arbol,{i:-1 for i in arbol.nodes},att1)
    nx.set_node_attributes(arbol,{i:-1 for i in arbol.nodes},att2)
    nx.set_edge_attributes(arbol,{i:0 for i in arbol.edges},att3)
    asignador_pesos(nodo,arbol,att0,att1,att2,att3,True)
    return arbol

# 1.4: Recorrido Girvan-Newman pasos 1-3

def gn_peso_enlace(red):
    '''
    -----------------------------------------------
    inputs:
        red (nx.DiGraph): Un grafo tipo nx.DiGraph que representa un grafo NO dirigido (i.e. si (A,B)\inE \to (B,A)\inE ). No valen grafos vacíos.
        El algoritmo adimite la representación de un grafo dirigido, pero NO se construyó para esto.

    -----------------------------------------------
    outputs:
        El árbol con el atributo de "e_pesos" con los pesos de los enlaces que resultan de Girvan-Newman, en los pasos 1-3.
    '''
    att1 = "e_pesos"
    nx.set_edge_attributes(red,{i:0 for i in red.edges},att1)
    nodos = list(red.nodes)
    for nodo in nodos:
        arbol = gn_p1(nodo,red)
        arbol = gn_p2(nodo,arbol)
        arbol = gn_p3(nodo,arbol)
        enlaces = dict(arbol.edges)
        for enlace in enlaces:
            red.edges[enlace][att1] += enlaces[enlace][att1]
            try:
                red.edges[(enlace[1],enlace[0])][att1] += enlaces[enlace][att1]
            except:
                pass

# 1.5: Creando las comunidades dado un Umbral

def gn_comunidades(red,atributo,umbral):
    '''
    -----------------------------------------------
    inputs:
        red (nx.DiGraph): Un grafo tipo nx.DiGraph que representa un grafo NO dirigido (i.e. si (A,B)\inE \to (B,A)\inE ). No valen grafos vacíos.
        atributo (str): El nombre del atributo al cuál se le quieren aplicar los cortes.
        umbral (float): El punto de corte para generar las comunidades.

    -----------------------------------------------
    outputs:
        red_copia (nx.DiGraph): Un grafo tipo nx.DiGraoh que representa un grafo NO dirigido (i.e. si (A,B)\inE \to (B,A)\inE ).
                                Representa las comunidades que se generan dado Girvan-Newman P1-P3 y el umbral. Es el paso previo a la implementación en una sola función.
    '''
    red_copia = red.copy()
    enlaces = dict(red_copia.edges)
    for enlace in enlaces:
        if enlaces[enlace][atributo]>=umbral:
            red_copia.remove_edge(enlace[0],enlace[1])
    return red_copia

# 1.6: Girvan Newman para una red y un umbral dados.

def gn_definitivo(red,umbral):
    '''
    -----------------------------------------------
    inputs:
        red (nx.DiGraph): Un grafo tipo nx.DiGraph que representa un grafo NO dirigido (i.e. si (A,B)\inE \to (B,A)\inE ). No valen grafos vacíos.
        umbral (float): El punto de corte para generar las comunidades.

    -----------------------------------------------
    outputs:
        red_nueva (nx.DiGraph): Un grafo tipo nx.DiGraoh que representa un grafo NO dirigido (i.e. si (A,B)\inE \to (B,A)\inE ).
                                Representa las comunidades que se generan dado Girvan-Newman P1-P3 y el umbral.
    '''
    atributo = "e_pesos"
    gn_peso_enlace(red)
    red_nueva = gn_comunidades(red,atributo,umbral)
    return red_nueva


#----------------------------------------
# Punto 2: Clausura Triadica Fuerte y Puentes Locales (Recordar: Para grafos NO dirigidos en formato DiGraph)

# 2.1: Revisión de un enlace como puente local.

def cp_puentes(red):
    att1 = "puente"
    enlaces = dict(red.edges)
    nx.set_edge_attributes(red,{i:None for i in enlaces},att1)
    for enlace in enlaces:
        if enlaces[enlace][att1] is None:
            A = enlace[0]
            B = enlace[1]
            Conj_A = set(red.successors(A))
            Conj_B = set(red.successors(B))
            if ((Conj_A & Conj_B) - {A,B}) == set():
                enlaces[enlace][att1] = True
                enlaces[(B,A)][att1] = True
            else:
                enlaces[enlace][att1] = False
                enlaces[(B,A)][att1] = False



# 2.2: Revisión de un nodo que cumpla CTF.

def cp_ctf(red):
    att1 = 'relacion'
    att2 = 'ctf'
    nodos = list(red.nodes)
    enlaces = dict(red.edges)
    nx.set_node_attributes(red,{i:True for i in nodos},att2)
    for A in nodos:
        vecinos = list(red.successors(A))
        l_vecinos = len(vecinos)
        if l_vecinos<2:
            pass
        else:
            for i in range(l_vecinos):
                B = vecinos[i]
                if enlaces[(A,B)][att1] == True:
                    for j in range(i+1,l_vecinos):
                        C = vecinos[j]
                        if enlaces[(A,C)][att1] == True:
                            if (B,C) not in enlaces:
                                red.nodes[A][att2] = False

# 2.3: Teorema.

def cp_revision(red):
    att1 = 'ctf'
    att2 = 'relacion'
    att3 = 'puente'
    nodos = dict(red.nodes)
    enlaces = dict(red.edges)
    bien_construido = True
    for nodo in nodos:
        if nodos[nodo][att1] == True:
            vecinos = list(red.successors(nodo))
            l_vecinos = len(vecinos)
            for i in range(l_vecinos):
                B = vecinos[i]
                if enlaces[(nodo,B)][att2] == True:
                    for j in range(i+1,l_vecinos):
                        C = vecinos[j]
                        if enlaces[(nodo,C)][att2] == True:
                            for nodo2 in vecinos:
                                if enlaces[(nodo,nodo2)][att3] == True:
                                    if enlaces[(nodo,nodo2)][att2] == True:
                                        return False
    return bien_construido

# 2.4: Implementación Completa.

def cp_construccion(red):
    att1 = 'relacion'
    if nx.get_edge_attributes(red,att1) == {}:
        if len(list(red.nodes))==0:
            return True
        else:
            raise Exception('Introduzca red con atributo relación')
    else:
        cp_puentes(red)
        cp_ctf(red)
        return cp_revision(red)





#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# End of Script


#G =  nx.Graph()
#G.add_edges_from([(1,2),(1,3)])
#nx.set_edge_attributes(G,{i:False for i in G.edges},'relacion')
#G = G.to_directed()
#dict(G.edges)
#cp_puentes(G)

#'ctf' in dict(G.edges)[(1,2)]
#len(dict(G.nodes))

##
##
# Pruebas Punto 1
##
#G = nx.DiGraph()
#G = nx.Graph()
#G.add_edges_from([(1,2),(1,3),(2,3),(2,4),(4,5),(4,6),(4,7),(5,6),(6,7)])
#G = G.to_directed()


#G = nx.Graph()
#G.add_edges_from([(0,1),(0,2),(0,3),(1,2),(2,3),(1,4),(1,5),(0,5),(3,6),(3,7),(4,8),(4,9),(5,9),(5,10),(6,10),(7,10),(8,11),(9,11),(10,11)])
#G = G.to_directed()
#gn_peso_enlace(G)
#Comunidades = gn_comunidades(G,'e_pesos',20)
#for umbral in [10,14,16,20]:
#    Comunidades = gn_comunidades(G,'e_pesos',umbral)
#    fig1 = plt.figure()
#    nx.draw(Comunidades,with_labels=True)
#    plt.show()


#Comunidades = gn_definitivo(G,4)
#fig1 = plt.figure()
#nx.draw(Comunidades,with_labels=True)
#plt.show()


#GG = gn_p1(0,G)
#GG = gn_p2(0,GG)
#GG = gn_p3(0,GG)

#del G.edges[(5,1)]

#G.remove_edge()
#nx.set_node_attributes(G,{1:1,2:2},'asignado')
#nx.set_node_attributes(G,{1:'hoa',2:2},'asignado')
#nx.get_node_attributes(G,'asignado')[1] = False
#G.nodes[1]['asignado'] = 'hoa'
#list(G.successors(1))
#G.add_edge(100,200)
#set() | set(G.neighbors(1))
#G.has_node(20)


#gn_peso_enlace(G)


#dict(G.edges)

#G = nx.DiGraph()
#G.add_node(0)

#GG = gn_p1(0,G)
#GG = gn_p2(0,GG)
#GG = gn_p3(0,GG)

#GG.edges[(5,9)]
#GG.nodes[9]

#dict(GG.edges)

#for i in GG.edges:
#    print(i)
#GG.edges[(0,1)]

#nx.get_node_attributes(GG,'n_caminos')
#nx.get_node_attributes(GG,'e_pesos')


#G.nodes[0]
#GG.edges
#fig0 = plt.figure()
#nx.draw(G,with_labels=True)
#plt.show()


#fig1 = plt.figure()
#nx.draw(Comunidades,with_labels=True)
#plt.show()

#fig2 = plt.figure()
#nx.draw(GGG,with_labels=True)
#plt.show()

    
    