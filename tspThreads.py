# Código Paralelo (Threads) para o Problema do Caixeiro Viajante
from multiprocessing.dummy import Pool as ThreadPool  # Substituto para ThreadPoolExecutor
from utils import carregar_cidades, medir_tempo_execucao, precompute_factorial, nth_permutation, custo_caminho, next_permutation, salvar_tempos, gerar_grafico

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

# Main para execução
if __name__ == "__main__":
    # Carregar os dados de cidades
    cidades = carregar_cidades("cidades.txt")

    # Medir o tempo de execução para diferentes números de cidades
    tempos = medir_tempo_execucao(cidades, tsp_paralelo)

    # Salvar os tempos em um arquivo de texto
    salvar_tempos(tempos, "paralelo")

    # Gerar o gráfico de tempos de execução
    gerar_grafico(tempos, "Paralelo")
