import networkx as nx
import time

def path_bruteforce(grafo,cidade):
    G = nx.read_edgelist(grafo)
    T=time.time()
    K = G.number_of_nodes()
    min=float('inf')
    caminho=[]
    D={}
    for n, nbrs in G.adj.items():
        for nbr, eattr in nbrs.items():
            wt = eattr['weight']
            D[(n,nbr)]=wt
    A = G.nodes()
    for j in A:
        for path in nx.all_simple_paths(G, source=cidade, target=j):
            if len(path)==K:
                W=nx.dijkstra_path(G,path[-1],path[0])
                F=path+W[1:]
                comp = 0
                for i in range(len(F) - 1):
                    j = i + 1
                    N = (F[i], F[j])
                    comp=comp+D[N]
                if comp<min:
                    min=comp
                    caminho=F
    T = time.time() - T
    #print('O menor caminho é',caminho,'e a peso é',min,'e o tempo do algoritmo é',T)
    return min,T
#path_bruteforce('grafoteste.txt','1')