import networkx as nx
import matplotlib.pyplot as plt
import time


#nx.draw_shell(G, with_labels=True, font_weight='bold')
#plt.show()

def vizinhoproximo(grafo,cidade):

    G=nx.read_edgelist(grafo)
    T = time.time()

    K = G.number_of_nodes() #número de vértices do gráfico

    custo=0
    caminho=[cidade]

    visitados = [cidade] #vértices visitados
    n_visitados=list(G.nodes()) #vértices não visitados
    n_visitados.remove(cidade)
    while len(visitados)<K:
        # Encontrar a menor aresta
        menor = float('inf')

        A = []  # lista de vértices adjacentes
        for n in G.adj[cidade]:
            if n not in visitados:
                A.append(n)

        if len(A)==0:
            min = float('inf')
            for i in n_visitados:
                tam = nx.dijkstra_path_length(G, source=cidade, target=i)
                if tam<min:
                    min=tam
                    cidademenor=i
            W=nx.dijkstra_path(G, source=cidade, target=cidademenor)
            caminho+=W[1:-1]
        else:
            for i in A:
                min = float('inf')
                if G.edges[cidade,i]['weight']<min:
                    min=G.edges[cidade,i]['weight']
                    cidademenor=i


        caminho.append(cidademenor)
        n_visitados.remove(cidademenor)

        if cidademenor not in visitados:
            visitados.append(cidademenor)

        cidade=cidademenor
        custo += min

    #Voltar ao ponto de partida
    W = nx.dijkstra_path(G, source=caminho[-1], target=caminho[0])  # encontrar o menor caminho entre o vertice final e o vertice inicial, para voltarmos ao ponto de partida
    custo+= nx.dijkstra_path_length(G, source=caminho[-1], target=caminho[0])
    caminho+=W[1:]
    T = time.time() - T
    #print('O melhor caminho é ',caminho,', e o peso é ',custo,'e o tempo do algoritmo é ',T)
    return custo,T
#vizinhoproximo('grafoteste.txt','1')
