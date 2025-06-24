from collections import deque           # Para estrutura de fila (BFS)
import heapq                            # Para filas de prioridade (A* e Gulosa)

# Definição de custo de movimento por tipo de terreno
terrain_cost = {
    'F': 1,              
    'R': 10,              
    'S': 4,              
    'SW': 20,             
    'W': float('inf')     
}


# Calcula a distância de Manhattan (linha + coluna) entre dois pontos a e b no grid.
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Busca em profundidade
def depth_first_search(terrain_map, objects_map, start, goal):
    rows, cols = len(terrain_map), len(terrain_map[0])
    nodes_expanded = 0

    # Pilha inicial com estado de partida
    stack = [(start, 0, [start], set())]
    visited = set()

    best_path = None
    best_cost = float('inf')
    best_treasures = set()

    while stack:
        (x, y), cost, path, treasures = stack.pop()
        nodes_expanded += 1

        state = (x, y, frozenset(treasures))
        if state in visited:
            continue
        visited.add(state)

        # Se há tesouro e ainda não coletado, adiciona
        if objects_map[x][y] == 'T' and (x, y) not in treasures:
            treasures = treasures.union({(x, y)})

        # Ao atingir a arca, avalia se é melhor solução
        if (x, y) == goal:
            if cost < best_cost or (cost == best_cost and len(treasures) > len(best_treasures)):
                best_path = path
                best_cost = cost
                best_treasures = treasures
            continue

        # Gera vizinhos nas quatro direções
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and terrain_map[nx][ny] != 'W':
                new_cost = cost + terrain_cost[terrain_map[nx][ny]]
                stack.append(((nx, ny), new_cost, path + [(nx, ny)], treasures))

    return best_path, best_cost, best_treasures, nodes_expanded


# Busca em largura
def breadth_first_search(terrain_map, objects_map, start, goal):
    rows, cols = len(terrain_map), len(terrain_map[0])

    # Fila FIFO inicial com estado de partida
    queue = deque([(start, 0, [start], set())])
    visited = set()

    best_path = None
    best_cost = float('inf')
    best_treasures = set()
    nodes_expanded = 0

    # Loop principal
    while queue:
        (x, y), cost, path, treasures = queue.popleft()
        nodes_expanded += 1

        state = (x, y, frozenset(treasures))
        if state in visited:
            continue
        visited.add(state)

        # Coleta tesouro se presente e ainda não coletado
        if objects_map[x][y] == 'T' and (x, y) not in treasures:
            treasures = treasures.union({(x, y)})

        # Atualiza melhor solução
        if (x, y) == goal:
            if cost < best_cost or (cost == best_cost and len(treasures) > len(best_treasures)):
                best_path = path
                best_cost = cost
                best_treasures = treasures
            continue
        
        # Expande vizinhos nas 4 direções
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            # Verifica limites e evita paredes
            if 0 <= nx < rows and 0 <= ny < cols and terrain_map[nx][ny] != 'W':
                new_cost = cost + terrain_cost[terrain_map[nx][ny]]

                # Adiciona novo estado ao final da fila
                queue.append(((nx, ny), new_cost, path + [(nx, ny)], treasures))

    return best_path, best_cost, best_treasures, nodes_expanded

#  Busca A*
def a_star_search(terrain_map, objects_map, start, goal):
    rows, cols = len(terrain_map), len(terrain_map[0])
    open_set = []
    start_h = manhattan_distance(start, goal)

    # (f_score, g_score, posição, caminho, tesouros)
    heapq.heappush(open_set, (start_h, 0, start, [start], set()))
    visited = set()
    best_path = None
    best_cost = float('inf')
    best_treasures = set()
    nodes_expanded = 0

    while open_set:
        f_score, g_score, (x, y), path, treasures = heapq.heappop(open_set)
        nodes_expanded += 1

        state = (x, y, frozenset(treasures))
        if state in visited:
            continue
        visited.add(state)

        # Coleta tesouro se presente e ainda não coletado
        if objects_map[x][y] == 'T' and (x, y) not in treasures:
            treasures = treasures.union({(x, y)})

        # Ao alcançar a arca, atualiza solução ótima
        if (x, y) == goal:
            if g_score < best_cost or (g_score == best_cost and len(treasures) > len(best_treasures)):
                best_path = path
                best_cost = g_score
                best_treasures = treasures
            continue
        
        # Expande vizinhos usando f = g + h para ordenação
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and terrain_map[nx][ny] != 'W':
                terrain_c = terrain_cost[terrain_map[nx][ny]]
                new_g = g_score + terrain_c
                h = manhattan_distance((nx, ny), goal)
                heapq.heappush(open_set, (new_g + h, new_g, (nx, ny), path + [(nx, ny)], treasures))

    return best_path, best_cost, best_treasures, nodes_expanded


# Busca Gulosa
def greedy_search(terrain_map, objects_map, start, goal):
    rows, cols = len(terrain_map), len(terrain_map[0])
    open_set = []
    start_h = manhattan_distance(start, goal)
    heapq.heappush(open_set, (start_h, start, [start], set()))

    visited = set()
    best_path = None
    nodes_expanded = 0

    while open_set:
        h_score, (x, y), path, treasures = heapq.heappop(open_set)
        nodes_expanded += 1

        state = (x, y, frozenset(treasures))
        if state in visited:
            continue
        visited.add(state)

        # Coleta tesouro se presente e ainda não coletado
        if objects_map[x][y] == 'T' and (x, y) not in treasures:
            treasures = treasures.union({(x, y)})

        # Ao alcançar a arca, finaliza imediatamente
        if (x, y) == goal:
            best_path = path
            break
        
        # Expande vizinhos priorizando quem está mais próximo do objetivo
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and terrain_map[nx][ny] != 'W':
                h = manhattan_distance((nx, ny), goal)
                heapq.heappush(open_set, (h, (nx, ny), path + [(nx, ny)], treasures))

    # Retorna custo -1 pois não é calculado especificamente
    return best_path, -1, treasures, nodes_expanded