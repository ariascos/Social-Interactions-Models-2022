#----------------------------------------#
#         Script Funciones T2 MIS        #
#   Mateo Alejandro Rodríguez Ramírez    #
#----------------------------------------#

#-----------------------------------------
# Cargue de paquetes.

import itertools as it
import networkx as nx
import numpy as np




#-------------------------------------------
# Funciones Punto 1.
#-------------------------------------------

# Función: matriz_ef
def matriz_ef(np_matrix):
    dimensiones = np_matrix.shape
    test = True
    tolerancia = 1/10000
    for i in range(dimensiones[0]):
        if ((np_matrix[i,:])<0).any():
            test = False
            return test
        else:
            if abs(((np_matrix[i,:]).sum())-1)>tolerancia:
                test = False
                return test
    return test

# Función: list_subsets
def list_subsets(listado,lenght):
    error = False
    if isinstance(lenght,(int,float)):
        if (lenght>=1) and (lenght<=len(listado)):
            if lenght//1 == lenght/1:
                subconjuntos = list(map(lambda x: list(x),it.combinations(listado,lenght)))
                return subconjuntos
            else:
                error = True
        else:
            error = True
    else:
        error = True 
    if error:
        raise Exception('Argumentos no validos')

# Función: mcd
def MCD(listado,numero = 1):
    minimo = int(min(listado))
    if minimo!=1:
        recorre = list(range(2,(minimo//2)+4))
        recorre+=[minimo]
        for i in recorre:
            if all([((j//i) == (j/i)) for j in listado]):
                listado = [j/i for j in listado]
                #print(listado)
                return numero*MCD(listado,i)
        return numero 
    else:
        return numero

def mcd(listado):
    return MCD(listado)

# Función: grafo_aperiodico
def grafo_aperiodico(grafo,conj_nodes):
    sub_grafo = nx.subgraph(grafo,conj_nodes)
    listado = list(nx.simple_cycles(sub_grafo))
    aperiodico = True
    if listado == []:
        aperiodico = False
        return aperiodico
    else:
        listado = [len(i) for i in listado]
        mcd_ = mcd(listado)
        #print(mcd,listado)
        if mcd_>1:
            aperiodico = False
    return aperiodico

# Función: grafo_fc 
def grafo_fc(grafo,conj_nodes):
    sub_grafo = nx.subgraph(grafo,conj_nodes)
    n = len(conj_nodes)
    termina_test = False
    for i in range(n):
        for j in range(i+1,n):
            if nx.has_path(sub_grafo,conj_nodes[i],conj_nodes[j])==False:
                termina_test = True
                break
            else:
                if nx.has_path(sub_grafo,conj_nodes[j],conj_nodes[i])==False:
                    termina_test = True
                    break
        if termina_test:
            break
    return not termina_test

# Función: grafo_cc
def grafo_cc(grafo,conj_nodes):
    conj_cerrado = True
    nodos = set(conj_nodes)
    for nodo in nodos:
        sucesores = set(list(grafo.successors(nodo)))
        if len(sucesores-nodos) != 0:
            conj_cerrado = False
            break
    return conj_cerrado

# Función: g_convergente 
def adj_modificator(matriz):
    dimensiones = matriz.shape
    matrix = matriz.copy()
    for i in range(dimensiones[0]):
        for j in range(dimensiones[1]):
            if matriz[i,j]>0:
                matrix[i,j] = 1
            else:
                matrix[i,j] = 0
    return matrix

def g_convergente(grafo):
    m_adj_w = nx.adjacency_matrix(grafo).todense
    if matriz_ef(m_adj_w):
        m_adj = adj_modificator(m_adj_w)
        grafo_nuevo = nx.from_numpy_matrix(m_adj,create_using=nx.DiGraph)
        nodos = list(grafo_nuevo.nodes)
        N = len(nodos)
        convergente = True
        for tamano in range(N):
            if tamano!=0:
                subconjuntos = list_subsets(listado = nodos,lenght = tamano)
                for conjunto in subconjuntos:
                    if grafo_cc(grafo = grafo_nuevo,conj_nodes = conjunto):
                        if grafo_fc(grafo = grafo_nuevo,conj_nodes = conjunto):
                            if grafo_aperiodico(grafo = grafo_nuevo,conj_nodes = conjunto) == False:
                                convergente = False
                                return convergente
        return convergente
    else:
        raise Exception('Matriz no es estocástica por filas')

#-------------------------------------------
# Funciones Punto 2. 
#-------------------------------------------

def limpiador(texto,diccionario):
    texto = texto.lower()
    for i in diccionario:
        texto = texto.replace(i,diccionario[i])
    return texto

def add_elem_dict(diccionario,listado):
    for i in listado:
        diccionario[i] = ""
    return diccionario

def limpieza_txt(listado):
    caracteres = ["¿","?","*","!","¡",",",";"]
    diccionario = {"á":"a","é":"e","í":"i","ó":"o","ú":"u"}
    diccionario = add_elem_dict(diccionario,caracteres)
    return list(map(lambda x : limpiador(texto = x,diccionario=diccionario),listado))

def palabras_txt(listado):
    palabras = set()
    for texto in listado:
        texto = texto.replace('.','')
        texto = [i.replace(' ','') for i in texto.split(' ')]
        palabras = palabras.union(texto)
    palabras = palabras - {''}
    palabras = list(palabras)
    return palabras

def frases_txt(listado):
    frases = set()
    for texto in listado:
        texto = [i.strip() for i in texto.split('.')]
        frases = frases.union(texto)
    frases = frases - {''}
    frases = list(frases)
    return frases

def frecuencia_txt(listaPalabras,listaFrases):
    Vectores_Frecuencia = []
    for frase in listaFrases:
        Vector = [frase.count(i) for i in listaPalabras]
        Vectores_Frecuencia.append(Vector)
    Vectores_Frecuencia = [np.matrix(i) for i in Vectores_Frecuencia]
    return Vectores_Frecuencia

def idf_calc(listaPalabras,listaTextosLimpios):
    n_i = []
    for palabra in listaPalabras:
        bool_apariciones = [(palabra in texto) for texto in listaTextosLimpios]
        suma_apariciones = sum(bool_apariciones)
        n_i.append(suma_apariciones)
    N_docs = len(listaTextosLimpios)
    idf = [np.log(N_docs/numero) for numero in n_i]
    idf = np.matrix(idf).T
    return idf

def idf_mod_cosine(frase1,frase2,idf):
    # Numerador
    N1 = np.multiply(frase1,frase2)
    print(N1.size)
    N2 = np.multiply(idf,idf)
    Numerador = (N1@N2)[0,0]
    # Denominador
    D1 = np.multiply(frase1,idf)
    D2 = np.multiply(frase2,idf)
    D1 = (D1@D1.T)[0,0]
    D2 = (D2@D2.T)[0,0]
    Denominador = D1*D2
    # Calculo la distancia
    distancia_idf_mod_cos = Numerador/Denominador
    return distancia_idf_mod_cos

def aprox_cosine(frase1,frase2):
    Numerador = (frase1@frase2.T)
    Denominador = (np.linalg.norm(frase1))*(np.linalg.norm(frase2))
    cosine = Numerador/Denominador
    result = (cosine+1)/2
    return result

def aprox_len(frase1,frase2):
    f1_normalizada = frase1*(1/(np.linalg.norm(frase1)))
    f2_normalizada = frase2*(1/(np.linalg.norm(frase2)))
    diff = np.linalg.norm(f1_normalizada-f2_normalizada)
    return 1-(diff/2)

def lex_rank(vectoresFrecuencia,simFun):
    # Matriz de pesos
    n = len(vectoresFrecuencia)
    Matriz = np.zeros((n,n))
    for i in range(n):
        for j in range(i,n):
            if simFun == 'idf':
                Matriz[i,j] = idf_mod_cosine(vectoresFrecuencia[i],vectoresFrecuencia[j],idf)
            elif simFun == 'cos':
                Matriz[i,j] = aprox_cosine(vectoresFrecuencia[i],vectoresFrecuencia[j])
            elif simFun == 'len':
                Matriz[i,j] = aprox_len(vectoresFrecuencia[i],vectoresFrecuencia[j])
            else:
                raise Exception('Introduzca una función de similaridad apropiada')
    Matriz = Matriz + Matriz.T - np.diag(np.diag(Matriz))
    # PageRank
    G = nx.from_numpy_matrix(Matriz)
    PageRank = nx.pagerank(G)
    return PageRank



#T1 = 'Hola, cómo vas? Este texto trata sobre una conversanción entre dos personas que se acaban de conocer'
#T2 = 'POr otro lado, este texto habla de cómo los dinosaurios eran los seres vivos que mandaban la parada hace millones de años'
#T3 = 'EsTE TexTO está diseñado para! poner a prueba, las cosas que cómo mínimo se; debían Quétar de los!¿?¡ textos'
#T4 = 'Acá solo diré que no me gusta el futbol. Sin embargo, me gusta el volley. No me gusta el Basquetball, pero si el tennis. Ayer ví un partido de Basquetball buenisimo entre la Universidad de los Andes y la Universidad Central'
#listado = [T1,T2,T3,T4]

#listado = limpieza_txt(listado=listado)
#palabras = palabras_txt(listado=listado)
#frases = frases_txt(listado=listado)
#vectoresFrecuencia = frecuencia_txt(listaPalabras=palabras,listaFrases=frases)
#idf = idf_calc(listaPalabras=palabras,listaTextosLimpios=listado)
#N = len(vectoresFrecuencia)
#for i in range(N):
#    for j in range(i,N):
#        idf_mod_cosine(vectoresFrecuencia[i],vectoresFrecuencia[j],idf)
#        aprox_cosine(vectoresFrecuencia[i],vectoresFrecuencia[j])
#        aprox_len(vectoresFrecuencia[i],vectoresFrecuencia[j])