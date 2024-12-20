# Código Paralelo (Threads) para o Problema do Caixeiro Viajante
from multiprocessing import Pool  # Usando multiprocessing
from utils import carregar_cidades, medir_tempo_execucao, precompute_factorial, nth_permutation, custo_caminho, next_permutation, salvar_tempos, gerar_grafico

# Função de nível superior para processar um bloco de permutações
def processar_bloco(args):
    thread_id, iter_per_process, extra, total_permutacoes, cidades_restantes, todas_cidades, matriz, factorial = args
    melhor_caminho_local = None
    melhor_custo_local = float('inf')

    inicio = thread_id * iter_per_process + min(thread_id, extra)
    fim = inicio + iter_per_process + (1 if thread_id < extra else 0)

    # Verifica se o início está dentro do intervalo válido
    if inicio >= total_permutacoes:
        return None, float('inf')

    # Gerar a permutação inicial para este bloco
    permutacao = nth_permutation(cidades_restantes, inicio + 1, factorial)

    for _ in range(fim - inicio):
        caminho_atual = [todas_cidades[0]] + permutacao + [todas_cidades[0]]
        custo_atual = custo_caminho(matriz, caminho_atual)

        # Atualizar o melhor caminho local
        if custo_atual < melhor_custo_local:
            melhor_custo_local = custo_atual
            melhor_caminho_local = caminho_atual

        # Gera a próxima permutação
        next_permutation(permutacao)

    return melhor_caminho_local, melhor_custo_local

def tsp_paralelo(matriz, todas_cidades):
    melhor_caminho_global = None
    melhor_custo_global = float('inf')
    cidades_restantes = todas_cidades[1:]

    # Pré-computar o fatorial para controle das permutações
    factorial = precompute_factorial(len(cidades_restantes))

    # Calcular o número total de permutações
    total_permutacoes = factorial[len(cidades_restantes)]

    # Configuração para divisão do trabalho
    num_processos = 4
    iter_per_process = total_permutacoes // num_processos
    extra = total_permutacoes % num_processos

    # Argumentos a serem passados para cada processo
    args = [
        (i, iter_per_process, extra, total_permutacoes, cidades_restantes, todas_cidades, matriz, factorial)
        for i in range(num_processos)
    ]

    # Usar multiprocessing.Pool para paralelismo
    with Pool(num_processos) as pool:
        resultados = pool.map(processar_bloco, args)

    # Consolida os resultados globais
    for caminho, custo in resultados:
        if custo < melhor_custo_global:
            melhor_custo_global = custo
            melhor_caminho_global = caminho

    return melhor_caminho_global, melhor_custo_global

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
