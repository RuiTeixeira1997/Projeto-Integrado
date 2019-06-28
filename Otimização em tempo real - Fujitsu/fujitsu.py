from cmd import *
from fujitsu_engine import Fuj
from Fujitsu_Permutacoes import *
import time
import numpy as np
import csv
import math
import matplotlib.pyplot as plt

class Fujitsu(Cmd):

    intro = 'Interpretador de comandos para Fujitsu. Escrever help ou ? para listar os comandos disponíveis.\n'
    prompt = 'Fujitsu> '

    def do_criar_agente(self,arg):
        lista = arg.split()
        nome = lista[0]
        #skill,custo ,
        tempo_final=Fuj.tempo_inicial
        atrib={}
        atrib['nome']=nome
        atrib['tempo_final']=tempo_final
        Fuj.Agentes.append(atrib)

    def do_atualizar_tempo_agente(self,arg):
        lista = arg.split()
        nome = lista[0]
        tempo=lista[1]
        for i in Fuj.Agentes:
            if i['nome']==nome:
                i['tempo_final']=tempo

    def do_ordena_agente(self,arg):
        if len(Fuj.Agentes)<=1:
            pass
        else:
            n=len(Fuj.Agentes)
            for i in range(n-1):
                for j in range(1+i,n):
                    if int(Fuj.Agentes[j]['tempo_final'])<int(Fuj.Agentes[i]['tempo_final']):
                        temp=Fuj.Agentes[i]
                        Fuj.Agentes[i]=Fuj.Agentes[j]
                        Fuj.Agentes[j]=temp

    def do_criar_ticket(self,arg):
        lista = arg.split()
        id = lista[0]
        tempo_tarefa = lista[1]
        prioridade = lista[2]
        c_p=lista[3]
        tempo_limite=lista[4]
        penalizacao=lista[5]
        nome={}
        nome['id']=id
        if Fuj.inicio==True:
            nome['t_call']=Fuj.tempo_inicial
        if Fuj.inicio==False:
            nome['t_call']=time.time()
        nome['tempo_tarefa']=tempo_tarefa
        nome['prioridade']=prioridade
        nome['constante_p']=c_p
        nome['tempo_inicio_tarefa']=9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        nome['Tempo_limite']=int(tempo_limite) + time.time()
        nome['penalizacao']=penalizacao
        nome['prioridade_alterada']=prioridade
        Fuj.Tickets.append(nome)
        Fuj.L.append(nome)
        self.do_ordenar_tickets(arg)

    def do_ler_ticket(self,arg):
        with open("Tickets_teste3.csv", "r") as f:
            reader = csv.reader(f, delimiter="\t")
            TICKET = []
            for i, line in enumerate(reader):
                TICKET.append(line[0].split(';'))
        Fuj.lidos = Fuj.lidos + len(TICKET)-1
        W=TICKET[0]
        TICKET.remove(W)
        for i in TICKET:
            self.do_criar_ticket(i[0] + str(' ') + i[1] + str(' ') + i[2] + str(' ') + i[3] + str(' ') + i[4] + str(
                    ' ') + i[5])
        Fuj.inicio = False

    def do_atualiza_ficheiro(self,arg):
        with open("Tickets_teste3.csv", "r") as f:
            reader = csv.reader(f, delimiter="\t")
            TICKET = []
            for i, line in enumerate(reader):
                TICKET.append(line[0].split(';'))
        k=len(TICKET)-1
        W = TICKET[0]
        TICKET.remove(W)
        if k>Fuj.lidos:
            J=TICKET[Fuj.lidos:]
            for i in J:
                self.do_criar_ticket(i[0] + str(' ') + i[1] + str(' ') + i[2] + str(' ') + i[3] + str(' ') + i[4] + str(
                    ' ') + i[5])

    def do_ordenar_tickets(self,arg):
        if len(Fuj.Tickets)<=1:
            pass
        else:
            n=len(Fuj.Tickets)
            for i in range(n-1):
                for j in range(1+i,n):
                    if int(Fuj.Tickets[j]['prioridade'])>int(Fuj.Tickets[i]['prioridade']):
                        temp=Fuj.Tickets[i]
                        Fuj.Tickets[i]=Fuj.Tickets[j]
                        Fuj.Tickets[j]=temp

    def do_atualiza_realizadas(self,arg):
        T=int(time.time())
        Fuj.Tarefas_realizadas=[]
        Fuj.Tarefas_nrealizadas=[]
        for tarefa in Fuj.Tickets:
            if int(tarefa['tempo_inicio_tarefa'])<T:
                Fuj.Tarefas_realizadas.append(tarefa)
            else:
                Fuj.Tarefas_nrealizadas.append(tarefa)

    def do_tarefas(self,arg):
        T=time.time()
        try:
            lista = arg.split()
            tempo_adicional=lista[0]


            self.do_atualiza_ficheiro(arg)
            Fuj.Tarefas_atribuidas=[]
            for i in range(len(Fuj.Tickets)):
                t = 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999

                # ciclo para saber qual o agente disponível
                for agente in Fuj.Agentes:
                    tempo = agente['tempo_final']
                    if float(tempo) < t:
                        t = float(tempo)
                Fuj.L = self.atualizar_prioridades(Fuj.L,t+int(tempo_adicional))
                if len(Fuj.L)>=1:
                    tarefa_atual = Fuj.L[0]
                else:
                    break
                Fuj.L.remove(tarefa_atual)
                tempo_tarefa_atual=tarefa_atual['tempo_tarefa']
                # antes de adicionar um ticket vai ter que atualizar todas as prioridadeas
                self.do_ordena_agente(arg)
                for agente in Fuj.Agentes:
                    tempo_agente=agente['tempo_final']
                    arg=str(agente['nome']) + str(' ') + str(int(tempo_agente)+int(tempo_tarefa_atual))
                    tarefa_atual['tempo_inicio_tarefa']=tempo_agente
                    self.do_atualizar_tempo_agente(arg)
                    Fuj.Tarefas_atribuidas.append((agente['nome'],tarefa_atual['id'],tarefa_atual['tempo_tarefa']))
                    break
            self.do_print_tarefas(arg)
            L=[]
            for agente in Fuj.Agentes:
                K=[]
                nome=agente['nome']
                for i in Fuj.Tarefas_atribuidas:
                    if i[0]==nome:
                        K.append(int(i[1]))
                L.append(K)
            pri=self.prioridade_lista(L)
            print ('Prioridade= ',pri)
        except:
            print('Os parâmetros introduzidos estão incorretos! Introduza o parâmetro tempo')
        print('Tempo de execução: ', time.time() - T)

    def do_atualiza_tarefas(self,arg):
        T=time.time()
        self.do_atualiza_ficheiro(arg)
        self.do_atualiza_realizadas(arg)
        id_tarefa=[]
        for i in Fuj.Tarefas_nrealizadas:
            id_tarefa.append(i['id']) # lista com o id das tarefas não realizadas
        A = []
        for j in Fuj.Tarefas_atribuidas:
            if j[1] in id_tarefa:
                A.append(j)
        for i in A:
            Fuj.Tarefas_atribuidas.remove(i)

        n=len(Fuj.Tarefas_nrealizadas)
        for i in range(n-1):
            for j in range(1+i,n):
                if int(Fuj.Tarefas_nrealizadas[j]['prioridade_alterada'])>int(Fuj.Tarefas_nrealizadas[i]['prioridade_alterada']):
                    temp=Fuj.Tarefas_nrealizadas[i]
                    Fuj.Tarefas_nrealizadas[i]=Fuj.Tarefas_nrealizadas[j]
                    Fuj.Tarefas_nrealizadas[j]=temp
        B=[]
        for a in Fuj.Agentes:
            B.append([a['nome'],Fuj.tempo_inicial])
        for a in Fuj.Tarefas_atribuidas:
            for b in B:
                if a[0]==b[0]:
                    b[1]+=int(a[2])
        for b in B:
            arg = str(b[0]) + str(' ') + str(int(b[1]))
            self.do_atualizar_tempo_agente(arg)
        for i in range(len(Fuj.Tarefas_nrealizadas)):
            t = 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
            # ciclo para saber qual o agente disponível
            for agente in Fuj.Agentes:
                tempo = agente['tempo_final']
                if float(tempo) < t:
                    t = float(tempo)
            Fuj.Tarefas_nrealizadas = self.atualizar_prioridades(Fuj.Tarefas_nrealizadas, t)
            if len(Fuj.Tarefas_nrealizadas) >= 1:
                tarefa_atual = Fuj.Tarefas_nrealizadas[0]
            else:
                break
            Fuj.Tarefas_nrealizadas.remove(tarefa_atual)
            tempo_tarefa_atual=tarefa_atual['tempo_tarefa']
            self.do_ordena_agente(arg)
            for agente in Fuj.Agentes:
                tempo_agente=agente['tempo_final']
                arg=str(agente['nome']) + str(' ') + str(int(tempo_agente)+int(tempo_tarefa_atual))
                tarefa_atual['tempo_inicio_tarefa']=tempo_agente
                self.do_atualizar_tempo_agente(arg)
                Fuj.Tarefas_atribuidas.append((agente['nome'],tarefa_atual['id'],tarefa_atual['tempo_tarefa']))
                break
        self.do_print_tarefas(arg)
        L = []
        for agente in Fuj.Agentes:
            K = []
            nome = agente['nome']
            for i in Fuj.Tarefas_atribuidas:
                if i[0] == nome:
                    K.append(int(i[1]))
            L.append(K)
        pri = self.prioridade_lista(L)
        print('Prioridade= ', pri)
        print('Tempo de execução: ', T - time.time())
    def do_Min_Global_uni(self, arg):
        Q=time.time()
        self.do_atualiza_ficheiro(arg)
        Fuj.Tarefas_atribuidas = []
        L = []
        for i in Fuj.Tickets:
            id = i['id']
            L.append(int(id))
        K = perm_uni(L, len(Fuj.Agentes))
        prioridade = 99999999999999999999999999999999999999999999999999999999999999999999
        for i in K:
            Pri = self.prioridade_lista(i)
            if Pri <= prioridade:
                prioridade = Pri
                lista_final = i
        contador = 0
        for i in lista_final:
            agente = Fuj.Agentes[contador]
            contador += 1
            for j in i:
                for k in Fuj.Tickets:
                    if int(k['id']) == j:
                        ticket = k
                Fuj.Tarefas_atribuidas.append((agente['nome'], ticket['id'], ticket['tempo_tarefa']))

        self.do_print_tarefas(arg)
        print(prioridade)
        print('Tempo de execução: ', time.time()-Q)

    def do_Min_Global_rest(self,arg):
        T=time.time()
        self.do_atualiza_ficheiro(arg)
        Fuj.Tarefas_atribuidas=[]
        L=[]
        for i in Fuj.Tickets:
            id=i['id']
            L.append(int(id))
        K=perm(L,len(Fuj.Agentes))
        prioridade = 99999999999999999999999999999999999999999999999999999999999999999999
        for i in K:
            Pri=self.prioridade_lista(i)
            if Pri <=prioridade:
                prioridade=Pri
                lista_final=i
        contador=0
        for i in lista_final:
            agente=Fuj.Agentes[contador]
            contador+=1
            for j in i:
                for k in Fuj.Tickets:
                    if int(k['id']) == j:
                        ticket = k
                Fuj.Tarefas_atribuidas.append((agente['nome'], ticket['id'], ticket['tempo_tarefa']))

        self.do_print_tarefas(arg)
        print(prioridade)
        print('Tempo de execução: ', time.time() - T)

    def do_Min_Global(self,arg):
        T=time.time()
        self.do_atualiza_ficheiro(arg)
        Fuj.Tarefas_atribuidas=[]
        L=[]
        for i in Fuj.Tickets:
            id=i['id']
            L.append(int(id))
        K=perm_brute(L,len(Fuj.Agentes))
        prioridade = 99999999999999999999999999999999999999999999999999999999999999999999
        for i in K:
            Pri=self.prioridade_lista(i)
            if Pri <=prioridade:
                prioridade=Pri
                lista_final=i
        contador=0

        for i in lista_final:
            agente=Fuj.Agentes[contador]
            contador+=1
            for j in i:
                for k in Fuj.Tickets:
                    if int(k['id']) == j:
                        ticket = k
                Fuj.Tarefas_atribuidas.append((agente['nome'], ticket['id'], ticket['tempo_tarefa']))

        self.do_print_tarefas(arg)
        print(prioridade)
        print('Tempo de execução: ', time.time() - T)

    def prioridade_lista(self,L):
        prioridade = 0
        for i in L:
            tempo=Fuj.tempo_inicial
            for j in i:
                for k in Fuj.Tickets:
                    if int(k['id'])==j:
                        ticket=k
                        break
                tempo_tarefa=ticket['tempo_tarefa']
                prio=self.cal_prioridade(ticket,tempo)
                tempo=tempo+float(tempo_tarefa)
                prioridade+=prio
        return prioridade

    def cal_prioridade(self,ticket,tempo):
        t_call = ticket['t_call']
        p = ticket['prioridade']
        p_c = ticket['constante_p']
        t_limite=ticket['Tempo_limite']
        pen=ticket['penalizacao']
        if float(tempo)-float(t_limite)<0:
            H=0
        if float(tempo)-float(t_limite)>=0:
            H=1
        prio = float(p) + (float(p_c) * (float(tempo) - float(t_call))) + (float(pen)*H)
        return prio

    def probabilidades(self,t,L=None):
        P=[]
        if L==None:
            L=Fuj.Tickets
        for i in L:
            prio=self.cal_prioridade(i,t)
            P.append([i,prio])
        x=0
        for i in P:
            x=x+i[1]
        contador=0
        for i in P:
            q=i[1]
            P[contador][1]=float(q)/float(x)
            contador+=1
        return P

    def prob_agentes(self):
        T=[]
        for i in Fuj.Agentes:
            T.append(float(i['tempo_final']))
        Min=min(T)
        P=[]
        for agente in Fuj.Agentes:
            # Simplesmente, aqui vamos calcular a proridade de sair o agente
            tempo_final = agente['tempo_final']
            P.append([agente,tempo_final])
        contador=0
        for i in P:
            q=i[1]
            P[contador][1]=math.exp(Min-float(q))
            contador+=1
        x=0
        for i in P:
            x=x+i[1]
        contador1=0
        for i in P:
            q=i[1]
            P[contador1][1] = q/x
            contador1 += 1
        return P

    def probabilistico(self):
        #escolha aleatoria do ticket
        A = []
        for i in Fuj.Tickets:
            A.append(i)
        for w in range(len(Fuj.Tickets)):
            #tempo=Fuj.tempo_inicial
            Q = self.prob_agentes()
            Agentes = []
            Prob1 = []
            for i in Q:
                Agentes.append(i[0])
                Prob1.append(i[1])
            b = np.random.choice(Agentes, 1, p=Prob1)
            b = b[0]
            tempo_agente = b['tempo_final']
            ##############
            P=self.probabilidades(tempo_agente,A)
            ID=[]
            Prob=[]
            for i in P:
                ID.append(i[0])
                Prob.append(i[1])
            a = np.random.choice(ID,1,p=Prob)
            a=a[0]
            A.remove(a)
            #escolha do agente

            arg = str(b['nome']) + str(' ') + str(float(tempo_agente) + float(a['tempo_tarefa']))
            self.do_atualizar_tempo_agente(arg)
            Fuj.Tarefas_atribuidas.append((b['nome'], a['id'], a['tempo_tarefa']))
        #self.do_print_tarefas(arg)
        L=[]
        for agente in Fuj.Agentes:
            K=[]
            nome=agente['nome']
            for i in Fuj.Tarefas_atribuidas:
                if i[0]==nome:
                    K.append(int(i[1]))
            L.append(K)
        pri=self.prioridade_lista(L)
        #print ('Prioridade= ',pri)
        return Fuj.Tarefas_atribuidas,pri

    def do_Tarefas_prob(self,arg):
        T=time.time()
        #self.do_atualiza_ficheiro(arg)
        a=Fuj.Agentes[0]
        TIME=a['tempo_final']
        lista = arg.split()
        max=lista[0]
        prioridade=99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
        final=[]
        X = []
        Y = []
        contador=0
        contador_final=0
        while contador<int(max):
            for i in Fuj.Agentes:
                arg = str(i['nome']) + str(' ') + str(TIME)
                self.do_atualizar_tempo_agente(arg)
            Fuj.Tarefas_atribuidas=[]
            L,pri=  self.probabilistico()
            if pri<=prioridade:
                prioridade=pri
                final=L
                contador=0
                X.append(contador_final)
                Y.append(pri)
            contador+=1
            contador_final+=1

        X.append(contador_final)
        Y.append(prioridade)

        K=[]
        for i in Fuj.Agentes:
            L=[]
            nome=i['nome']
            L.append(nome)
            for j in final:
                if j[0]==nome:
                    L.append((j[1],j[2]))
            K.append(L)
        for i in K:
            print(i[0],end='')
            M=[]
            for j in range(len(i)-1):
                print((int(i[j+1][1])-1)*'-',end='')
                print('|',end='')
                M.append(i[j+1][0])
            print(M)
        Tempo_atual=time.time()-Fuj.tempo_inicial
        print('Time::::',(int(Tempo_atual)-3)*'-','|',int(Tempo_atual))
        print(prioridade)
        print('Tempo de execução: ', time.time() - T)
        print('O valor do contador final é:', contador_final)
        plt.plot(X, Y, 'r-')
        plt.show()

    def atualizar_prioridades(self,L,t):
        for ticket in L:
            #t_call = ticket['t_call']
            #p = ticket['prioridade']
            #p_c = ticket['constante_p']
            #ticket['prioridade'] = float(p) + float(p_c)*(float(t)-float(t_call))
            ticket['prioridade_alterada']=self.cal_prioridade(ticket,t)
        # ordenação da lista
        if len(L)<=1:
            pass
        else:
            n=len(L)
            for i in range(n-1):
                for j in range(1+i,n):
                    if int(L[j]['prioridade_alterada'])>int(L[i]['prioridade_alterada']):
                        temp=L[i]
                        L[i]=L[j]
                        L[j]=temp
        return L # Lista dos tickets com a prioridade atualizada

    def do_print_tarefas(self,arg):
        K=[]
        for i in Fuj.Agentes:
            L=[]
            nome=i['nome']
            L.append(nome)
            for j in Fuj.Tarefas_atribuidas:
                if j[0]==nome:
                    L.append((j[1],j[2]))
            K.append(L)
        K.sort()
        for i in K:
            print(i[0],end='')
            M=[]
            for j in range(len(i)-1):
                print((int(i[j+1][1])-1)*'-',end='')
                print('|',end='')
                M.append(i[j+1][0])
            print(M)
        Tempo_atual=time.time()-Fuj.tempo_inicial
        print('Time::::',(int(Tempo_atual)-3)*'-','|',int(Tempo_atual))

    def do_mostrar(self,arg):
        for i in Fuj.Tickets:
            print(i)

if __name__ == '__main__':
    Fuj = Fuj()
    sh = Fujitsu()

    #Criar Agentes
    sh.do_criar_agente('agente1:')
    sh.do_criar_agente('agente2:')
    sh.do_criar_agente('agente3:')
    sh.do_ler_ticket('ola')

    sh.cmdloop()