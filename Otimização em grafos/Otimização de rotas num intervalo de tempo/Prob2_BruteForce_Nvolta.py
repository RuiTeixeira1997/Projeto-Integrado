import networkx as nx
import matplotlib.pyplot as plt
import time

def brutep2(grafo,inicio,tempo):
    G = nx.read_edgelist(grafo)
    T = time.time()

    A = G.nodes()

    caminho=[]
    custo_min=0
    custo_vertices_max=0
    for j in A:
        for path in nx.all_simple_paths(G, source=inicio, target=j):
            vertices = []
            vertices.append(path[0])
            custo = G.edges[path[0], path[1]]['weight']
            custo_vertices = 0
            for i in range(1, len(path) - 1):

                custo = custo + G.edges[path[i], path[i + 1]]['weight']
                if path[i] not in vertices:
                    custo = custo + G.edges[path[i], path[i]]['weight']
                    custo_vertices += G.edges[path[i], path[i]]['weight']

                vertices.append(path[i])

            if custo<=tempo:
                if custo_vertices>=custo_vertices_max:
                    caminho=path
                    custo_min=custo
                    custo_vertices_max=custo_vertices

    print('O menor caminho é', caminho, 'cujo custo é', custo_min, '. E o tempo de trabalho é', custo_vertices_max,'.')
    print(time.time() - T)

brutep2('grafo2.txt','1',1075)