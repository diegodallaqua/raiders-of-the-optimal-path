import random
import pygame

# Tamanho de cada célula do grid em pixels
CELL_SIZE = 100

# Tipos de terreno possíveis (F: Plano, R: Rochoso, S: Arenoso, SW: Pântano)
terrain_type = ['F', 'R', 'S', 'SW']

# Símbolos especiais para parede, tesouro, arca perdida e agente
wall = 'W'
treasure = 'T'
lost_ark = 'X'
dr_jones = 'J'

# Gera duas matrizes 8x8: uma que define o tipo de terreno em cada célula e outra que define os objetos (J, T, X) posicionados no grid
def generate_maps():
    map_data_terrain = []
    map_data_objects = []

    # Cria linhas do mapa de terreno e de objetos
    for i in range(8):
        row_terrain = []
        row_objects = []
        for j in range(8):

            # Garanta que a posição inicial (0,0) e final (7,7) não sejam paredes
            if (i, j) in [(0, 0), (7, 7)]:

                # Sorteia apenas terreno normal
                row_terrain.append(random.choice(terrain_type))
            else:

                # 25% de chance de ser parede
                if random.random() < 0.25:
                    row_terrain.append(wall)
                else:
                    row_terrain.append(random.choice(terrain_type))

            # Inicialmente, nenhuma célula de objetos
            row_objects.append(None)
        map_data_terrain.append(row_terrain)
        map_data_objects.append(row_objects)

    # Posiciona o agente em (0,0)
    map_data_objects[0][0] = dr_jones

    # Posiciona a arca perdida em (7,7)
    map_data_objects[7][7] = lost_ark

    # Posiciona os tesouros em células livres e não-paredes
    placed = 0
    while placed < 6:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if (map_data_terrain[x][y] != wall and
            map_data_objects[x][y] is None):
            map_data_objects[x][y] = treasure
            placed += 1

    return map_data_terrain, map_data_objects

# Desenha o mapa completo na tela
def draw_map(screen, terrain_map, objects_map,
             img_dr_jones, img_treasure, img_ark,
             sand_texture, rock_texture, grass_texture,
             swamp_texture, wall_texture):
    
    for i, row in enumerate(terrain_map):
        for j, terrain in enumerate(row):

            # Converte coordenadas de grid para pixels
            x_px = j * CELL_SIZE
            y_px = i * CELL_SIZE

            # Seleciona textura de fundo com base no tipo de terreno
            if terrain == 'F':
                screen.blit(grass_texture, (x_px, y_px))
            elif terrain == 'R':
                screen.blit(rock_texture, (x_px, y_px))
            elif terrain == 'S':
                screen.blit(sand_texture, (x_px, y_px))
            elif terrain == 'SW':
                screen.blit(swamp_texture, (x_px, y_px))
            elif terrain == 'W':
                screen.blit(wall_texture, (x_px, y_px))
            # Caso não reconheça o símbolo, pinta de branco
            else:
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x_px, y_px, CELL_SIZE, CELL_SIZE))

            # Verifica se há objeto na célula atual
            obj = objects_map[i][j]
            if obj == 'J':
                img = img_dr_jones
            elif obj == 'T':
                img = img_treasure
            elif obj == 'X':
                img = img_ark
            else:
                img = None

            # Se houver imagem de objeto, centraliza e desenha
            if img:
                rect = img.get_rect()
                pos_x = x_px + (CELL_SIZE - rect.width) // 2
                pos_y = y_px + (CELL_SIZE - rect.height) // 2
                screen.blit(img, (pos_x, pos_y))
