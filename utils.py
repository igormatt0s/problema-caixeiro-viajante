import time
import matplotlib.pyplot as plt

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
def precompute_factorial(n):
    factorial = [1] * (n + 1)
    for i in range(2, n + 1):
        factorial[i] = factorial[i - 1] * i
    return factorial

# Função de permutação otimizada
def nth_permutation(arr, n, factorial):
    N = len(arr)
    if n > factorial[N]:
        raise ValueError("n está fora do intervalo para o número de permutações possíveis.")

    permutation = []
    elements = arr[:]
    n -= 1  # Para tornar n zero-indexed
    
    # Cálculo direto da n-ésima permutação sem gerar todas
    for i in range(N, 0, -1):
        fact = factorial[i - 1]
        index = n // fact
        permutation.append(elements.pop(index))
        n %= fact
    
    return permutation

# Função para calcular o custo de um caminho
def custo_caminho(matriz, caminho):
    custo = 0
    for i in range(1, len(caminho)):
        custo += matriz[caminho[i-1]][caminho[i]]
    return custo

# Função para medir o tempo de execução de qualquer algoritmo de TSP
def medir_tempo_execucao(cidades, funcao_tsp, max_cidades=10):
    tempos = []

    # Medir o tempo de execução para diferentes números de cidades
    for i in range(3, max_cidades + 1):  # Variando de 3 até max_cidades (10 por padrão)
        subset_cidades = dict(list(cidades.items())[:i])  # Pega um subset com 'i' cidades
        matriz, todas_cidades = gerar_matriz(subset_cidades)

        # Medir o tempo de execução
        start = time.perf_counter()
        melhor_caminho, melhor_custo = funcao_tsp(matriz, todas_cidades)  # Chama a função de TSP
        end = time.perf_counter()

        print(f"Melhor Caminho para {i} Cidades:", melhor_caminho)
        print(f"Custo do Melhor Caminho para {i} Cidades:", melhor_custo)
        print(f"Tempo de Execução para {i} Cidades:", end - start, "segundos")

        tempos.append(end - start)  # Tempo de execução

    return tempos

# Função para salvar os tempos de execução em um arquivo de texto
def salvar_tempos(tempos, algoritmo):
    with open(f"tempos_execucao_{algoritmo}.txt", 'w') as f:
        for i, tempo in enumerate(tempos, start=3):
            f.write(f"Cidades: {i}, Tempo: {tempo:.5f} segundos\n")

# Função para gerar o gráfico de tempos de execução
def gerar_grafico(tempos, algoritmo):
    cidades = list(range(3, len(tempos) + 3))
    plt.plot(cidades, tempos, marker='o')
    plt.title(f'Tempo de Execução do Algoritmo TSP {algoritmo}')
    plt.xlabel('Número de Cidades')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.grid(True)
    plt.show()