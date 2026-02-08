# utils/benchmark.py
import time
from . import search_algorithms

# Função que compara o desempenho dos diferentes algoritmos de busca
def comparar_algoritmos(terrain_map, objects_map, start, goal):
    results = []
    null_path = False

    # Lista com os nomes e funções dos algoritmos a serem comparados
    algs = [
        ('DFS', search_algorithms.depth_first_search),
        ('BFS', search_algorithms.breadth_first_search),
        ('GS',  search_algorithms.greedy_search),
        ('A*',  search_algorithms.a_star_search),
    ]

    # Executa todos os algoritmos
    for name, func in algs:
        # Faz uma cópia do mapa de objetos
        objs_copy = [row.copy() for row in objects_map]

        # Marca o tempo inicial da execução
        begin = time.perf_counter()

        # Executa o algoritmo de busca
        res = func(terrain_map, objs_copy, start, goal)

        # Marca o tempo final
        end = time.perf_counter()

        # Calcula duração da execução
        duration = end - begin

        # Verifica se o resultado foi nulo ou inválido
        if res is None or (isinstance(res, tuple) and (res[0] is None or len(res) == 0)):
            null_path = True
        else:
            path, cost, treasures, nodes_expanded = res

            # 🔹 Ajuste principal aqui
            if cost == 0:
                results.append(
                    f"{name} - Nodes Expanded: {nodes_expanded}"
                )
            else:
                results.append(
                    f"{name} - Cost: {cost:.0f}, {nodes_expanded} Nodes Expanded "
                )

    # Retorna uma mensagem caso nenhum caminho seja encontrado
    if null_path:
        return "Path Inexistent"

    return "\n".join(results)