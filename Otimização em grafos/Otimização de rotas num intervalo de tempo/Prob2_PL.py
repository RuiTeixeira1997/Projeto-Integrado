from pulp import *
import numpy as np
import pickle
import time


def PL(dados,cidadeinicial,tempo):

    org=cidadeinicial
    CITY=cidadeinicial
    f = open(dados, 'rb')
    G = pickle.load(f)
    f.close()

    T=time.time()

    sites=G[0]
    distances=G[1]

    #create the problem
    prob=LpProblem("salesman",LpMaximize)
    x = LpVariable.dicts('x',distances, 0,1,LpBinary)
    cost = lpSum([x[(i,j)]*distances[(i,j)] for (i,j) in distances])
    prob+=cost

    #constraints
    for k in sites:
        #every site has exactly one inbound connection
        prob+= lpSum([ x[(i,k)] for i in sites if (i,k) in x]) ==1
        #every site has exactly one outbound connection
        prob+=lpSum([ x[(k,i)] for i in sites if (k,i) in x]) ==1

    #we need to keep track of the order in the tour to eliminate the possibility of subtours
    u = LpVariable.dicts('u', sites, 0, len(sites)-1, LpInteger)

    #subtour elimination
    N=len(sites)
    for i in sites:
        for j in sites:
            if i != j and (i != org and j!= org) and (i,j) in x:
                prob += u[i] - u[j] <= (N)*(1-x[(i,j)]) - 1

    prob.solve()

    sites_left = sites.copy()

    tour = []
    tour.append(sites_left.pop(sites_left.index(org)))

    while int(prob)<tempo:

        for k in sites_left:
            if x[(org, k)].varValue == 1:
                tour.append(sites_left.pop(sites_left.index(k)))
                org = k
                break

    tour.append(CITY)

    tour_legs = [distances[(tour[i - 1], tour[i])] for i in range(1, len(tour))]


    T=time.time()-T

    print('O menor caminho é', tour, 'e a peso é',sum(tour_legs) , 'e o tempo do algoritmo é', T)

    #return sum(tour_legs), T

PL('PLgrafo2.txt',1,1200)