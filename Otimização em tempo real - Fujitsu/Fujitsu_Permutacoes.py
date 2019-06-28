from itertools import accumulate
import itertools

def perm(L,agentes):

    W = list(itertools.permutations(L))
    P = []


    def partition(number):
        answer = set()
        answer.add((number,))
        for x in range(1, number):
            for y in partition(number - x):
                answer.add((x,) + y)
        return answer



    A = []
    K = partition(len(L))
    for k in K:
        if len(k) == agentes:
            A.append(list(k))
    for i in W:

        i = list(i)

        for q in A:
            # Using islice
            Output = [i[x - y: x] for x, y in zip(
                accumulate(q), q)]
            P.append(Output)

    return P


def perm_brute(L,agentes):

    W = list(itertools.permutations(L))
    P = []

    def partition(number):
        answer = set()
        answer.add((number,))
        for x in range(1, number):
            for y in partition(number - x):
                answer.add((x,) + y)
        return answer

    A = []
    K = partition(len(L))
    for k in K:
        if len(k) <= agentes:
            A.append(list(k))

    for i in W:

        i = list(i)

        for q in A:
            # Using islice
            Output = [i[x - y: x] for x, y in zip(
                accumulate(q), q)]
            P.append(Output)

    Final = []
    for i in P:
        if len(i) == agentes:
            Final.append(i)
        else:

            Q = agentes - len(i)
            for j in range(Q):
                i.append([])
            a = list(itertools.permutations(i))
            for l in a:
                if list(l) not in Final:
                    Final.append(list(l))
    return Final


def perm_uni(L,agentes):

    W = list(itertools.permutations(L))
    P = []


    def partition(number):
        answer = set()
        answer.add((number,))
        for x in range(1, number):
            for y in partition(number - x):
                answer.add((x,) + y)
        return answer

    def calcula_dif(A):
        max_dif = 0

        for i in range(len(A) - 1):
            for j in range(i + 1, len(A)):
                k = abs(A[i] - A[j])
                if k >= max_dif:
                    max_dif = k
        return max_dif

    A = []
    K = partition(len(L))
    for k in K:
        if len(k) == agentes and calcula_dif(k)<=1:
            A.append(list(k))
    for i in W:

        i = list(i)

        for q in A:
            # Using islice
            Output = [i[x - y: x] for x, y in zip(
                accumulate(q), q)]
            P.append(Output)

    return P
