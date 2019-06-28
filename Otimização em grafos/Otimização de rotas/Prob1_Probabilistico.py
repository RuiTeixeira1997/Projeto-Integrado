import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import matplotlib.pyplot as plt



def AlgoritmoProb(grafo,inicial,max):
    G = nx.read_edgelist(grafo)
    T = time.time()

    K=G.number_of_nodes()

    Vertice_inic=inicial
    contador=0
    contador_final=0
    X=[]
    Y=[]
    min = float('inf')
    caminho_final=[]
    while contador < max:
        inicial=Vertice_inic
        L=[] # vértices visitados
        L.append(inicial)
        Caminho=[]
        Caminho.append(inicial)
        custo=0
        while len(L)<K:
            A=[] #lista de vértices adjacentes
            for n in G.adj[inicial]:
                A.append(n)
            #p=len(A)
            #q=random.randint(0,p-1)
            q=random.choice(A)
            M=G.edges[inicial,q]['weight']
            custo=custo+M
            inicial=q
            Caminho.append(q)

            if inicial not in L:
                L.append(inicial)
        W = nx.dijkstra_path(G, inicial, L[0])
        Caminho=Caminho+W[1:]
        custo += nx.dijkstra_path_length(G, source=inicial, target=L[0])
        if custo<min:
            min=custo
            caminho_final=Caminho
            contador=0
            X.append(contador_final)
            Y.append(custo)
        contador=contador+1
        contador_final=contador_final+1


    T=time.time()-T
    #print('No algoritmo probabilistico o contador o final é ',contador_final)
    print('O melhor caminho é ', caminho_final, ', e o peso é ', min, 'e o tempo do algoritmo é ', T)
    #plt.plot(X, Y, 'r-')
    #plt.show()
    #print(min, T)
    return min, T

#AlgoritmoProb('grafoteste.txt','1',50000)




