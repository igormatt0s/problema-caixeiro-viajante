# Código Sequencial (Força Bruta) para o Problema do Caixeiro Viajante
import math
from utils import carregar_cidades, medir_tempo_execucao, custo_caminho, next_permutation, salvar_tempos, gerar_grafico

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
#    factorial = precompute_factorial(n - 1)
    
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
        
#        permutacao = nth_permutation(cidades_restantes, i + 1, factorial)
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

# Main para execução
if __name__ == "__main__":
    # Carregar os dados de cidades
    cidades = carregar_cidades("cidades.txt")

    # Medir o tempo de execução para diferentes números de cidades
    tempos = medir_tempo_execucao(cidades, tsp)

    # Salvar os tempos em um arquivo de texto
    salvar_tempos(tempos, "sequencial")

    # Gerar o gráfico de tempos de execução
    gerar_grafico(tempos, "Sequencial")