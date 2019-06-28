import time

class Fuj:
    def __init__(self):
        self.Agentes=[]
        self.Tickets=[]
        self.L=[]
        self.Tarefas_atribuidas=[]
        self.Tarefas_realizadas=[]  # Tarefas já realizadas e a serem realizadas
        self.Tarefas_nrealizadas=[]
        self.tempo_inicial=time.time()
        self.inicio=True
        self.lidos=0 # numero de tickets que já foram lidos