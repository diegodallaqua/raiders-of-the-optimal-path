# Procura o Dr. Jones no mapa de objetos e retorna suas coordenadas (linha, coluna).
def find_agent(objects_map):
    for i, row in enumerate(objects_map):
        for j, val in enumerate(row):
            if val == 'J':
                return i, j
    return None, None

# Verifica se a posição (x, y) é válida
def can_move(terrain_map, x, y):
    rows, cols = len(terrain_map), len(terrain_map[0])

    # Verifica limites do grid
    if x < 0 or y < 0 or x >= rows or y >= cols:
        return False
    
    # Verifica se a célula é parede
    if terrain_map[x][y] == 'W':
        return False
    return True

# Move o Dr. Jones na direção especificada ('up', 'down', 'left', 'right') se a célula de destino for válida.
def move_agent(terrain_map, objects_map, x, y, direction):
    # Define deslocamento com base na direção
    dx, dy = 0, 0
    if direction == 'up':
        dx = -1
    elif direction == 'down':
        dx = 1
    elif direction == 'left':
        dy = -1
    elif direction == 'right':
        dy = 1

    new_x, new_y = x + dx, y + dy
    rows, cols = len(terrain_map), len(terrain_map[0])

    # Verifica se o movimento está dentro dos limites e não esbarra em parede
    if 0 <= new_x < rows and 0 <= new_y < cols and terrain_map[new_x][new_y] != 'W':
        # Se a célula de destino tem a arca perdida, finaliza o jogo
        if objects_map[new_x][new_y] == 'X':
            # Atualiza posição do agente
            objects_map[x][y] = None
            objects_map[new_x][new_y] = 'J'
            return new_x, new_y, True

        # Movimento normal: verifica se não está na própria posição do Dr. Jones
        if objects_map[new_x][new_y] != 'J':
            objects_map[x][y] = None
            objects_map[new_x][new_y] = 'J'
            return new_x, new_y, False

    # Movimento inválido ou sem mudança: mantém posição atual
    return x, y, False
