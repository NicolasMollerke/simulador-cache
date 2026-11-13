from Conjunto import Conjunto
import math

class Cache:
    def __init__(self, nsets, bsize, assoc):
        self.nsets = nsets
        self.bsize = bsize
        self.assoc = assoc
        
        self.lista = [Conjunto(assoc) for _ in range(nsets)]
        
        self.acessos = 0
        self.hits = 0
        self.misses_compulsorios = 0
        self.misses_capacidade_conflito = 0
        
        self.historico_blocos = set()
        
        self.n_bits_offset = int(math.log2(self.bsize))

        self.n_bits_indice = int(math.log2(self.nsets)) 
        self.n_bits_tag = 32 - self.n_bits_offset - self.n_bits_indice

    def acesso(self, endereco):
        self.acessos += 1
        
        tag = endereco >> (self.n_bits_indice + self.n_bits_offset)
        indice = (endereco >> self.n_bits_offset) & ((2 ** self.n_bits_indice) - 1)

        conjunto_alvo = self.lista[indice]

        bloco_id = endereco >> self.n_bits_offset

        if conjunto_alvo.busca(tag):
            self.hits += 1
            return True
        else:
            if bloco_id in self.historico_blocos:
                self.misses_capacidade_conflito += 1
            else:
                self.misses_compulsorios += 1
                self.historico_blocos.add(bloco_id)
            conjunto_alvo.insercao(tag)
            return False
            
