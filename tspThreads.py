import time
import matplotlib.pyplot as plt
from multiprocessing.dummy import Pool as ThreadPool  # Substituto para ThreadPoolExecutor

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

# Função para calcular os fatoriais
def precompute_factorial(n):
    factorial = [1] * (n + 1)
    for i in range(2, n + 1):
        factorial[i] = factorial[i - 1] * i
    return factorial

# Função para gerar a n-ésima permutação usando o fatorial
def nth_permutation(arr, n, factorial):
    N = len(arr)
    if n > factorial[N]:
        raise ValueError("n está fora do intervalo para o número de permutações possíveis.")

    permutation = []
    elements = arr[:]
    n -= 1  # Ajusta para índice 0-based

    for i in range(N):
        fact = factorial[N - 1 - i]
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

# Função para gerar a próxima permutação (equivalente ao C++ next_permutation)
def next_permutation(arr):
    i = len(arr) - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    if i == -1:
        return False
    j = len(arr) - 1
    while arr[j] <= arr[i]:
        j -= 1
    arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1:] = reversed(arr[i + 1:])
    return True

# Função para resolver o TSP usando paralelismo com divisão do trabalho
def tsp_paralelo(matriz, todas_cidades):
    melhor_caminho = None
    melhor_custo = float('inf')
    cidades_restantes = todas_cidades[1:]

    # Pré-computar o fatorial para controle das permutações
    factorial = precompute_factorial(len(cidades_restantes))

    # Calcular o número total de permutações
    total_permutacoes = factorial[len(cidades_restantes)]

    # Configuração para divisão do trabalho
    num_threads = 4  # Ajuste o número de threads conforme necessário
    iter_per_thread = total_permutacoes // num_threads
    extra = total_permutacoes % num_threads

    # Função para processar um bloco de permutações
    def processar_bloco(thread_id):
        nonlocal melhor_caminho, melhor_custo
        inicio = thread_id * iter_per_thread + min(thread_id, extra)
        fim = inicio + iter_per_thread + (1 if thread_id < extra else 0)

        # Verifica se o início está dentro do intervalo válido
        if inicio >= total_permutacoes:
            return

        # Gerar a permutação inicial para este bloco
        permutacao = nth_permutation(cidades_restantes, inicio + 1, factorial)

        for _ in range(fim - inicio):
            caminho_atual = [todas_cidades[0]] + permutacao + [todas_cidades[0]]
            custo_atual = custo_caminho(matriz, caminho_atual)

            # Atualizar o melhor caminho de forma segura
            if custo_atual < melhor_custo:
                melhor_custo = custo_atual
                melhor_caminho = caminho_atual

            # Gera a próxima permutação
            next_permutation(permutacao)

    # Usar ThreadPool para paralelismo
    with ThreadPool(num_threads) as pool:
        pool.map(processar_bloco, range(num_threads))

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
        melhor_caminho, melhor_custo = tsp_paralelo(matriz, todas_cidades)
        end = time.perf_counter()

        tempos.append(end - start)  # Tempo de execução

        print(f"Melhor Caminho para {i} Cidades:", melhor_caminho)
        print(f"Custo do Melhor Caminho para {i} Cidades:", melhor_custo)
        print(f"Tempo de Execução para {i} Cidades:", end - start, "segundos")

    return tempos

# Função para salvar os tempos de execução em um arquivo de texto
def salvar_tempos(tempos):
    with open("tempos_execucao_paralelo.txt", 'w') as f:
        for i, tempo in enumerate(tempos, start=3):
            f.write(f"Cidades: {i}, Tempo: {tempo:.5f} segundos\n")

# Função para gerar o gráfico de tempos de execução
def gerar_grafico(tempos):
    cidades = list(range(3, len(tempos) + 3))
    plt.plot(cidades, tempos, marker='o')
    plt.title('Tempo de Execução do Algoritmo TSP Paralelo')
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
