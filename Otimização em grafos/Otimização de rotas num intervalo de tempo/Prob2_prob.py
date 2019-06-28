import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import matplotlib.pyplot as plt



def AlgoritmoProb(grafo,inicial,tempo):
    G = nx.read_edgelist(grafo)
    T = time.time()

    K=G.number_of_nodes()

    Vertice_inic=inicial
    max=50000
    contador=0
    contador_final=0
    X=[]
    Y=[]
    min =0
    caminho_final=[]
    while contador < max:
        inicial=Vertice_inic
        Caminho=[]
        Caminho.append(inicial)
        custo=0
        custo_vertices=0
        visitados=[Vertice_inic]
        while custo<tempo:
            A=[] #lista de vértices adjacentes
            for n in G.adj[inicial]:
                if n!=inicial:
                    A.append(n)
            #p=len(A)
            #q=random.randint(0,p-1)
            q=random.choice(A)
            M=G.edges[inicial,q]['weight']
            custo=custo+M
            if q not in visitados:
                visitados.append(q)
                custo=custo+G.edges[q,q]['weight']
                custo_vertices+=G.edges[q,q]['weight']
            inicial=q
            Caminho.append(q)
        caminho_novo=Caminho
        while True:
            if custo>tempo:
                custo = custo - G.edges[caminho_novo[-1], caminho_novo[-2]]['weight']
                ulti=Caminho[-1]
                caminho_novo=Caminho[:-1]
                Caminho.remove(Caminho[len(Caminho)-1])
                if ulti not in caminho_novo:
                    custo = custo - G.edges[ulti,ulti]['weight']
                    custo_vertices-=G.edges[ulti,ulti]['weight']




            else:
                break

        if custo_vertices>=min:
            min=custo_vertices
            caminho_final=caminho_novo
            custo_final=custo
            contador=0
            X.append(contador_final)
            Y.append(min)
        contador=contador+1
        contador_final=contador_final+1





    T=time.time()-T
    print('No algoritmo probabilistico o contador o final é ',contador_final)
    print('O melhor caminho é ', caminho_final, ', e o peso é ', custo_final, 'e o tempo do algoritmo é ', T,'e o custo dos vertices',min)
    plt.plot(X, Y, 'r-')
    plt.show()


AlgoritmoProb('grafo1234.txt','1',2000)