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

    # Movimento inválido
    if not (0 <= new_x < rows and 0 <= new_y < cols):
        return x, y, False, None

    if terrain_map[new_x][new_y] == 'W':
        return x, y, False, None

    target_object = objects_map[new_x][new_y]

    # Atualiza posição do agente
    objects_map[x][y] = None
    objects_map[new_x][new_y] = 'J'

    # Verifica se encontrou a arca
    finished = (target_object == 'X')

    return new_x, new_y, finished, target_object