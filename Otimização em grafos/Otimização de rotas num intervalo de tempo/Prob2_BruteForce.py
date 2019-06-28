import networkx as nx
import matplotlib.pyplot as plt
import time

def brutep2(grafo,inicio,tempo):
    G = nx.read_edgelist(grafo)
    T = time.time()

    A = G.nodes()

    Caminhos=[]
    for j in A:
        for path in nx.all_simple_paths(G, source=inicio, target=j):
            W = nx.dijkstra_path(G, source=j, target=inicio)
            Caminhos.append(path+W[1:])

    Final=[]

    for path in Caminhos:
        vertices=[]
        vertices.append(path[0])
        custo=G.edges[path[0],path[1]]['weight']
        custo_vertices=0
        for i in range(1,len(path)-1):

            custo=custo+G.edges[path[i],path[i+1]]['weight']
            if path[i] not in vertices:
                custo=custo+G.edges[path[i], path[i]]['weight']
                custo_vertices+=G.edges[path[i], path[i]]['weight']

            vertices.append(path[i])
        Final.append([path,custo,custo_vertices])


    Final_tempo=[]

    for j in Final:
        if j[1]<=tempo:
            Final_tempo.append(j)

    K=Final_tempo[0]
    for j in Final_tempo:
        if j[2]>=K[2]:
            K=j

    print(K)
    print(time.time()-T)






brutep2('grafo.txt','1',2000)