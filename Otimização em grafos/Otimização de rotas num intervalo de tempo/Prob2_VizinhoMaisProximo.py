import networkx as nx
import matplotlib.pyplot as plt
import time





def tempo_minimo(grafo,cidade,tempo):

    def comprimentos(path):
        vertices=[]
        vertices.append(path[0])
        custo_comprimento=G.edges[path[0],path[1]]['weight']
        for i in range(1,len(path)-1):

            custo_comprimento=custo_comprimento+G.edges[path[i],path[i+1]]['weight']
            if path[i] not in vertices:
                custo_comprimento=custo_comprimento+G.edges[path[i], path[i]]['weight']

            vertices.append(path[i])
        return custo_comprimento


    custo=0
    G = nx.read_edgelist(grafo)
    caminho=[]
    caminho.append(cidade)
    visitados = [cidade] #vértices visitados
    n_visitados=list(G.nodes()) #vértices não visitados
    n_visitados.remove(cidade)

    while custo < tempo:

        A = []  # lista de vértices adjacentes
        for n in G.adj[cidade]:
            if n not in visitados:
                A.append(n)

        if len(A)==0:
            min = float('inf')
            for i in n_visitados:
                tam = nx.dijkstra_path_length(G, source=cidade, target=i) + G.edges[i,i]['weight']
                if tam<min:
                    min=tam
                    cidademenor=i
            W=nx.dijkstra_path(G, source=cidade, target=cidademenor)
            caminho+=W[1:-1]
        else:
            for i in A:
                min = float('inf')
                if G.edges[cidade,i]['weight']<min:
                    min=G.edges[cidade,i]['weight']+ G.edges[i,i]['weight']
                    cidademenor=i

        caminho.append(cidademenor)
        n_visitados.remove(cidademenor)
        if len(n_visitados)==0:
            break
        if cidademenor not in visitados:
            visitados.append(cidademenor)

        cidade = cidademenor
        custo=custo+min
    caminho_novo = caminho

    while True:
        W=nx.dijkstra_path(G, source=caminho_novo[-1], target=caminho_novo[0])
        caminho_novo=caminho+W[1:]
        a=comprimentos(caminho_novo)
        if comprimentos(caminho_novo)>tempo:
            caminho_novo=caminho[:-1]
            caminho.remove(caminho[len(caminho)-1])
        else:
            break


    print(caminho_novo)
    print(comprimentos(caminho_novo))


tempo_minimo('grafo6.txt','1',1075)

