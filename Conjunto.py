from Bloco import Bloco
import random

class Conjunto:
    def __init__(self, assoc):
        self.assoc = assoc
        self.lista = [Bloco() for b in range(assoc)]

    def busca(self, tag):
        
        for l in self.lista:
            if l.validade == True and l.tag == tag:
                return True
            
        return False

    def insercao(self, tag):
        for b in self.lista:
            if b.validade == False:
                b.validade = True
                b.tag = tag
                return    

        self.substituicao(tag)

    def substituicao(self, tag):
        via = random.randint(0, self.assoc - 1)
        self.lista[via].validade = True
        self.lista[via].tag = tag