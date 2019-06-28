import networkx as nx
import pickle
import random
import matplotlib.pyplot as plt
G = nx.Graph()

def Gerar_grafo(vertices,arestas,nome,completo=False,lacetes=False,preencher=True):
    original=nome
    B=[]
    D={}
    #numero de arestas é n*(n-1)/2 no caso de lacetes=False
    A=[] #arestas usadas
    if completo==False:
        for j in range(arestas):
            a=random.randint(1,vertices)
            b=random.randint(1,vertices)
            c=random.randint(30,200)
            while (a,b) in A or a==b: #para termos um grafo completo
                a = random.randint(1, vertices)
                b = random.randint(1, vertices)
            A.append((a,b))
            A.append((b,a))
            B.append((a,b,c))
            B.append((b,a,c))

    if completo==True:
        for i in range(1,vertices):
            for j in range(i+1,vertices+1):
                c = random.randint(30, 200) #distancia
                B.append((i, j, c))
                B.append((j, i, c))


    if lacetes==True:
        for j in range(1,vertices+1):
            B.append((j,j,random.randint(30,200)))
        B.sort()


    G.add_weighted_edges_from(B)
    nx.write_edgelist(G, nome)

    if preencher==True:
        for i in range(1,vertices):
             for j in range(1+i,vertices+1):
                if (i,j) not in A:
                    B.append((i,j,2000000000000000000000))
                    B.append((j,i,2000000000000000000000))

    i=1
    while True:
        C={}
        for element in B:
            if element[0]==i:
                C[element[1]]=element[2]
        D[i]=C
        i=i+1
        if len(D)==vertices:
            break







    G.add_weighted_edges_from(B)

    nome='chris'+original
    f=open(nome,'wb')
    pickle.dump(D,f)
    f.close()

    #Programação Linear

    verticesPL=[]
    for i in range(1,vertices+1):
        verticesPL.append(i)

    distances={}
    for i in B:
        distances[(i[0], i[1])] = i[2]

    nome = 'PL' + original
    f = open(nome, 'wb')
    pickle.dump([verticesPL,distances], f)
    f.close()





Gerar_grafo(10,30,'grafo2.txt',completo=True,lacetes=True,preencher=False)
