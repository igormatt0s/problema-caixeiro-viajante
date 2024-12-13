# Código Sequencial (Força Bruta) para o Problema do Caixeiro Viajante

import time
import matplotlib.pyplot as plt
import math

# Função para carregar os dados de cidades
def carregar_cidades(arquivo):
    adjacencia = {}
    
    with open(arquivo, 'r') as f:
        for linha in f.readlines():
            cidade, dados = linha.strip().split(":")
            cidade = cidade.strip()
            dados = eval(dados.strip())
            adjacencia[cidade] = {dados[i]: dados[i+1] for i in range(0, len(dados), 2)}

    return adjacencia

# Função para gerar a matriz de distâncias
def gerar_matriz(cidades):
    todas_cidades = list(cidades.keys())
    n = len(todas_cidades)
    
    # Inicializa a matriz de distâncias com infinito
    matriz = {cidade: {other: float('inf') for other in todas_cidades} for cidade in todas_cidades}
    
    # Preenche as distâncias
    for cidade, vizinhos in cidades.items():
        for vizinho, distancia in vizinhos.items():
            matriz[cidade][vizinho] = distancia

    return matriz, todas_cidades

# Função para calcular a próxima permutação lexicográfica
def next_permutation(arr):
    # Encontre o maior índice k tal que arr[k] < arr[k + 1]
    k = len(arr) - 2
    while k >= 0 and arr[k] >= arr[k + 1]:
        k -= 1
    
    # Se não existe tal k, a permutação está no último valor
    if k == -1:
        return False
    
    # Encontre o maior índice l tal que arr[k] < arr[l]
    l = len(arr) - 1
    while arr[k] >= arr[l]:
        l -= 1
    
    # Troque os elementos em k e l
    arr[k], arr[l] = arr[l], arr[k]
    
    # Inverta a sequência após k
    arr[k + 1:] = reversed(arr[k + 1:])
    
    return True

# Função para pré-calcular os fatoriais
def precalcular_fatoriais(n):
    fatoriais = [1] * (n + 1)
    for i in range(2, n + 1):
        fatoriais[i] = fatoriais[i - 1] * i
    return fatoriais

# Função de permutação otimizada
def nth_permutation(arr, n, fatoriais):
    N = len(arr)
    result = []
    available = arr[:]
    n -= 1  # Para tornar n zero-indexed
    
    # Cálculo direto da n-ésima permutação sem gerar todas
    for i in range(N, 0, -1):
        factorial = fatoriais[i - 1]
        index = n // factorial
        result.append(available.pop(index))
        n %= factorial
    
    return result

# Função para calcular o custo de um caminho
def custo_caminho(matriz, caminho):
    custo = 0
    for i in range(1, len(caminho)):
        custo += matriz[caminho[i-1]][caminho[i]]
    return custo

# Função de força bruta para resolver o TSP usando next_permutation
def tsp(matriz, todas_cidades):
    melhor_caminho = None
    melhor_custo = float('inf')
    n = len(todas_cidades)

    # Gera permutações de 1 até (n-1) cidades (sem a cidade 0)
    cidades_restantes = todas_cidades[1:]
    
    # Número total de permutações
    total_permutacoes = math.factorial(n - 1)

    # Pré-calcular os fatoriais até n-1
#    fatoriais = precalcular_fatoriais(n - 1)
    
    # Gerar a primeira permutação
    cidades_restantes.sort()

    # Inicializa o custo do primeiro caminho
    caminho_atual = [todas_cidades[0]] + cidades_restantes + [todas_cidades[0]]
    melhor_custo = custo_caminho(matriz, caminho_atual)
    melhor_caminho = caminho_atual.copy()
    
    # Verificar cada permutação diretamente usando next_permutation
    for i in range(total_permutacoes):
        if i % 1000 == 0:  # Apenas imprima a cada 1000 iterações
            print(f"Processando a permutação {i + 1} de {total_permutacoes}")
        
#        permutacao = nth_permutation(cidades_restantes, i + 1, fatoriais)
        if not next_permutation(cidades_restantes):  # Se não houver mais permutações
            break
#        caminho_atual = [todas_cidades[0]] + permutacao + [todas_cidades[0]]
        caminho_atual = [todas_cidades[0]] + cidades_restantes + [todas_cidades[0]]  # Garante o retorno à cidade inicial
        custo_atual = custo_caminho(matriz, caminho_atual)
        
        if custo_atual < melhor_custo:
            melhor_custo = custo_atual
            melhor_caminho = caminho_atual
        
        # Gere a próxima permutação
        if not next_permutation(cidades_restantes):
            break
    
    return melhor_caminho, melhor_custo

# Função para medir o tempo de execução
def medir_tempo_execucao(arquivo, cidades, max_cidades=10):
    tempos = []
    
    # Medir o tempo de execução para diferentes números de cidades
    for i in range(3, max_cidades + 1):  # Variando de 3 até max_cidades (10 por padrão)
        subset_cidades = dict(list(cidades.items())[:i])  # Pega um subset com 'i' cidades
        matriz, todas_cidades = gerar_matriz(subset_cidades)
        
        # Medir o tempo de execução
        start = time.perf_counter()
        melhor_caminho, melhor_custo = tsp(matriz, todas_cidades)
        end = time.perf_counter()

        print(f"Melhor Caminho para {i} Cidades:", melhor_caminho)
        print(f"Custo do Melhor Caminho para {i} Cidades:", melhor_custo)
        print(f"Tempo de Execução para {i} Cidades:", end - start, "segundos")
        
        tempos.append(end - start)  # Tempo de execução
    
    return tempos

# Função para salvar os tempos de execução em um arquivo de texto
def salvar_tempos(tempos):
    with open("tempos_execucao_sequencial.txt", 'w') as f:
        for i, tempo in enumerate(tempos, start=3):
            f.write(f"Cidades: {i}, Tempo: {tempo:.5f} segundos\n")

# Função para gerar o gráfico de tempos de execução
def gerar_grafico(tempos):
    cidades = list(range(3, len(tempos) + 3))
    plt.plot(cidades, tempos, marker='o')
    plt.title('Tempo de Execução do Algoritmo TSP Sequencial')
    plt.xlabel('Número de Cidades')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.grid(True)
    plt.show()

# Main para execução
if __name__ == "__main__":
    # Carregar os dados de cidades
    cidades = carregar_cidades("cidades.txt")
    
    # Medir o tempo de execução para diferentes números de cidades
    tempos = medir_tempo_execucao("cidades.txt", cidades)
    
    # Salvar os tempos em um arquivo de texto
    salvar_tempos(tempos)
    
    # Gerar o gráfico de tempos de execução
    gerar_grafico(tempos)