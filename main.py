from Cache import Cache
import sys
import os

padrao = (64, 4, 1)

def erro(mensagem):
    print("Erro:", mensagem)
    sys.exit(1)


def potencia_2(n):
    return n > 0 and (n & (n - 1)) == 0


def ler_config(texto):
    partes = texto.split(":")
    if len(partes) != 3:
        erro(f"configuração '{texto}' inválida, use nsets:bsize:assoc")

    try:
        nsets = int(partes[0])
        bsize = int(partes[1])
        assoc = int(partes[2])
    except ValueError:
        erro(f"configuração '{texto}' contém valores que não são números")

    if not potencia_2(nsets):
        erro(f"nsets = {nsets} precisa ser potência de 2")
    if not potencia_2(bsize):
        erro(f"bsize = {bsize} precisa ser potência de 2")
    if assoc <= 0:
        erro(f"assoc = {assoc} precisa ser maior que zero")

    return (nsets, bsize, assoc)

def ler_argumentos():
    args = sys.argv[1:] 

    if len(args) == 1:
        config_il1 = padrao
        config_dl1 = padrao
        config_l2 = padrao
    elif len(args) == 3:
        config_il1 = ler_config(args[0])
        config_dl1 = ler_config(args[1])
        config_l2 = padrao
    elif len(args) == 4:
        config_il1 = ler_config(args[0])
        config_dl1 = ler_config(args[1])
        config_l2 = ler_config(args[2])
    else:
        erro("quantidade de argumentos inválida")

    arquivo = args[-1]
    
    if not os.path.isfile(arquivo):
        erro(f"arquivo '{arquivo}' não encontrado")

    return config_il1, config_dl1, config_l2, arquivo

def ler_enderecos(arquivo, ordem="big"):
    enderecos = []

    with open(arquivo, "rb") as f:
        dados = f.read(4)
        while dados:
            if len(dados) < 4:
                print(f"Aviso: {len(dados)} byte(s) sobrando no fim do arquivo foram ignorados")
                break
            enderecos.append(int.from_bytes(dados, ordem))
            dados = f.read(4)

    return enderecos

def imprimir(nome, cache):
    misses = cache.misses_compulsorios + cache.misses_capacidade_conflito

    if cache.acessos > 0:
        hit_ratio = cache.hits / cache.acessos
        miss_ratio = misses / cache.acessos
    else:
        hit_ratio = 0.0
        miss_ratio = 0.0

    print(f"===== {nome} =====")
    print(f"Configuração: {cache.nsets} conjuntos, blocos de {cache.bsize} bytes, associatividade {cache.assoc}")
    print(f"Acessos:                {cache.acessos}")
    print(f"Hits:                   {cache.hits}")
    print(f"Hit ratio:              {hit_ratio:.4f}")
    print(f"Misses:                 {misses}")
    print(f"Miss ratio:             {miss_ratio:.4f}")
    print(f"  Compulsórios:         {cache.misses_compulsorios}")
    print(f"  Capacidade+conflito:  {cache.misses_capacidade_conflito}")
    print()

def main():
    c_il1, c_dl1, c_l2, arquivo = ler_argumentos()

    il1 = Cache(c_il1[0], c_il1[1], c_il1[2])
    dl1 = Cache(c_dl1[0], c_dl1[1], c_dl1[2])
    l2 = Cache(c_l2[0], c_l2[1], c_l2[2])

    enderecos = ler_enderecos(arquivo)

    limite = 512 * 1024 * 1024

    for e in enderecos:
        if e < limite:
            resultado = dl1.acesso(e)
        else:
            resultado = il1.acesso(e)

        if not resultado:
            l2.acesso(e)

    imprimir("L1 Instruções", il1)
    imprimir("L1 Dados", dl1)
    imprimir("L2 Unificada", l2)

if __name__ == "__main__":
    main()