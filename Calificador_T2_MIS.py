#-------------------------------------------
# Cargue paquetes y directorios.
#-------------------------------------------
import os
import itertools as it
import networkx as nx
import numpy as np

directorio = r'C:\Users\mateo\OneDrive\Desktop\MATEO\TRANSITORIO\Personal\2022_2\Complementarias\MIS'
os.chdir(directorio)

import Solucion_T2_MIS as MSOL
import G5_202013547_200520722_201815146_201228081 as SSOL

#------------------------------------------- 
# Funciones Punto 1.
#-------------------------------------------
Calif_P1 = []
# Función: matriz_ef
matrices_ef = [np.matrix([[0.3,0.3,0.4],[0.5,0.5,0],[1,0,0]]),np.matrix([[0.5,0.5],[1,0]]),np.identity(50)] 
matrices_nef = [np.matrix([[0.3,0.3,0.3],[0.5,0.5,0],[1,0,0]]),np.matrix([[0.5,0.5],[-1,0]]),-np.identity(50)]
test_ef = all([MSOL.matriz_ef(matriz)==SSOL.matriz_ef(matriz) for matriz in matrices_ef])
test_nef = all([MSOL.matriz_ef(matriz)==SSOL.matriz_ef(matriz) for matriz in matrices_nef])
#test_ef = all([MSOL.matriz_ef(matriz)==SSOL.matrix_ef(matriz) for matriz in matrices_ef])
#test_nef = all([MSOL.matriz_ef(matriz)==SSOL.matrix_ef(matriz) for matriz in matrices_nef])
Calif_P1.append((test_ef+test_nef)/2) 

# Función: list_subsets
Nota = 0
for k in range(1,10):
    listado = [i for i in range(k)]
    for j in range(1,k):
        Nota+=(len(MSOL.list_subsets(listado,j)) == len(SSOL.list_subsets(listado,j)))
        #Nota+=(len(MSOL.list_subsets(listado,j)) == len(SSOL.subsets(listado,j)))
Calif_P1.append(Nota/36)

# Función: mcd
Prueba = [[i*k for i in range(1,10)] for k in [1,2,3,5,7,11,13,14,17,19]]
for i in Prueba:
    print(i)
    print(MSOL.mcd(i))
    print(SSOL.mcd(i))
    print('_'*50)
r = sum([MSOL.mcd(i) == SSOL.mcd(i) for i in Prueba]) / 10
Calif_P1.append(r)

# Grafos para pruebas
G_Sin_Ciclos = nx.DiGraph()
G_Sin_Ciclos.add_edges_from([(i,i-1) for i in range(1,20)])

G_Con_Ciclos_NAP = nx.DiGraph()
G_Con_Ciclos_NAP.add_edges_from([(i,i-1) for i in range(1,20)]+[(19,0),(15,7)])

G_Con_Ciclos_AP = G_Con_Ciclos_NAP.copy()
G_Con_Ciclos_AP.add_edge((1,0))

G_Convergente = nx.DiGraph()
G_Convergente.add_edges_from([(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)])

G_Generico = nx.DiGraph()
G_Generico.add_edges_from([(0,1),(0,2),(0,3),(1,2),(2,3),(1,4),(1,5),(0,5),(3,6),(3,7),(4,8),(4,9),(5,9),(5,10),(6,10),(7,10),(8,11),(9,11),(10,11)])


grafos = [G_Sin_Ciclos,G_Con_Ciclos_NAP,G_Con_Ciclos_AP,G_Convergente,G_Generico]
# Función: grafo_aperiodico, grafo_fc, grafo_cc
punt_cc = 1
punt_fc = 1
punt_ap = 1
n_graph = 1
primos = [1,2,3,5,7,17,19]
for grafo in grafos:
    nodos = list(grafo.nodes())
    N = len(grafo.nodes())
    print('Grafo N: {}'.format(n_graph))
    for j in [l for l in primos if l<=N]:
        print(j)
        for subset in MSOL.list_subsets(nodos,j):
            if punt_cc == 1:
                pass
                #if (MSOL.grafo_cc(grafo,subset) != SSOL.grafo_cc(grafo,subset)):
                #if (MSOL.grafo_cc(grafo,subset) != SSOL.cc(grafo,subset)):
                #    punt_cc = 0
            if punt_fc == 1:
                pass
                #if (MSOL.grafo_fc(grafo,subset) != SSOL.grafo_fc(grafo,subset)):
                #if (MSOL.grafo_fc(grafo,subset) != SSOL.fc(grafo,subset)):
                #    punt_fc = 0
            if punt_ap == 1:
                if (MSOL.grafo_aperiodico(grafo,subset) != SSOL.grafo_aperiodico(grafo,subset)):
                    punt_ap = 0
    n_graph += 1
#n_corridas = 288491
Calif_P1.append(punt_cc)
Calif_P1.append(punt_fc)
Calif_P1.append(punt_ap)

# Función: g_convergente
M1 = np.identity(10)
M2 = np.matrix([[.4,.5,.1],[.3,0,.7],[.5,.3,.2]])
M3 = np.matrix([[1/3 for i in range(3)] for j in range(3)])
M4 = np.matrix([[0,1],[1,0]])
matrices = [M1,M2,M3,M4]
grafos = [nx.from_numpy_matrix(i,create_using=nx.DiGraph) for i in matrices]
calif = 1
for grafo in grafos:
    if calif == 1:
        if (MSOL.g_convergente(grafo)) != (SSOL.g_convergente(grafo)):
            calif = 0
Calif_P1.append(calif)

print(Calif_P1)
print('La nota del grupo en el punto 1 es {}'.format(5*sum(Calif_P1)/7))

#-------------------------------------------
# Funciones Punto 2.
#-------------------------------------------

# Textos Base
T1 = 'Hola, cómo vas? Este texto trata sobre una conversanción entre dos personas que se acaban de conocer'
T2 = 'POr otro lado, este texto habla de cómo los dinosaurios eran los seres vivos que mandaban la parada hace millones de años'
T3 = 'EsTE TexTO está diseñado para! poner a prueba, las cosas que cómo mínimo se; debían Quétar de los!¿?¡ textos'
T4 = 'Acá solo diré que no me gusta el futbol. Sin embargo, me gusta el volley. No me gusta el Basquetball, pero si el tennis. Ayer ví un partido de Basquetball buenisimo entre la Universidad de los Andes y la Universidad Central'
tolerancia = 1/(10**5)
Nota = 0
# Listado de textos
listado = [T1,T2,T3,T4]
# Lipieza de texto
listado = MSOL.limpieza_txt(listado=listado)
[listado[i] == SSOL.limpieza_txt(listado)[i] for i in range(len(listado))]
# Palabras
palabras = MSOL.palabras_txt(listado=listado)
set(palabras)==(set(SSOL.palabras_txt(listado)))
# Frases
frases = MSOL.frases_txt(listado=listado)
set(frases)==(set(SSOL.frases_txt(listado)))
# Vectores de frecuencia
vectoresFrecuencia = MSOL.frecuencia_txt(listaPalabras=palabras,listaFrases=frases)
vectoresFrecuenciaS = SSOL.frecuencia_txt(palabras,frases)
[np.matrix(i) for i in SSOL.frecuencia_txt(palabras,frases)][0]
vectoresFrecuencia[0] 

vectoresFrecuencia[0]
vectoresFrecuenciaS[0]

# IDF
idf = MSOL.idf_calc(listaPalabras=palabras,listaTextosLimpios=listado)
idfs = SSOL.idf_calc(palabras,listado)
np.linalg.norm(idf-np.matrix(SSOL.idf_calc(palabras,listado)).T)
# Revisión idf:mod_cos, aprox_cos, aprox_len
N = len(vectoresFrecuencia)
for i in range(N):
    for j in range(i,N):
        # idf_mod_cos
        AA = MSOL.idf_mod_cosine(vectoresFrecuencia[i],vectoresFrecuencia[j],idf)
        #AB = SSOL.idf_mod_cosine(vectoresFrecuenciaS[i],vectoresFrecuenciaS[j],idfs)
        #AB = SSOL.idf_midfied_cosine(vectoresFrecuenciaS[i],vectoresFrecuenciaS[j],np.matrix(idfs))
        #AB = SSOL.idf_mod_cos(vectoresFrecuenciaS[i],vectoresFrecuenciaS[j],idfs)
        # cos
        BA = MSOL.aprox_cosine(vectoresFrecuencia[i],vectoresFrecuencia[j])
        BB = SSOL.aprox_cosine(vectoresFrecuenciaS[i],vectoresFrecuenciaS[j])
        # len
        CA = MSOL.aprox_len(vectoresFrecuencia[i],vectoresFrecuencia[j])
        CB = SSOL.aprox_len(vectoresFrecuenciaS[i],vectoresFrecuenciaS[j])

        #print(np.abs(AA-AB)<tolerancia,np.abs(BA-BB)<tolerancia,np.abs(CA-CB)<tolerancia)
        print(np.abs(BA-BB)<tolerancia,np.abs(CA-CB)<tolerancia)

# Lex Rank
MSOL.lex_rank(vectoresFrecuencia=vectoresFrecuencia,simFun='cos').values()
MSOL.lex_rank(vectoresFrecuencia=vectoresFrecuencia,simFun='len').values()

SSOL.lex_rank(SSOL.frecuencia_txt(palabras,frases),'cos')
SSOL.lex_rank(SSOL.frecuencia_txt(palabras,frases),'len')