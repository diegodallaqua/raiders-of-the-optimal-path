import pygame                   # Biblioteca para criação de jogos e animações
import os
from utils import map_generator, movement, search_algorithms
from utils.components import patterned_menu, pop_up
from utils.benchmark import comparar_algoritmos

# Inicializa os módulos do pygame
pygame.init()

# ---CONFIGURAÇÕES INICIAIS DA TELA---
GAME_WIDTH, HEIGHT = 800, 800
MENU_WIDTH = 200
screen = pygame.display.set_mode((GAME_WIDTH + MENU_WIDTH, HEIGHT))                    # Cria a janela
score_font = pygame.font.SysFont('Arial', 20)
popup_message = pop_up.Popup(screen, GAME_WIDTH, HEIGHT)                               # Objeto pop-up para exibir mensagem


# ---CARREGAMENTO E ESCALA DE IMAGENS---
base_path = os.path.dirname(__file__)

# Carrega e prepara imagens com fundo transparente
img_dr_jones = pygame.image.load(os.path.join(base_path, "assets", "images", "dr_jones.png")).convert_alpha()
img_treasure = pygame.image.load(os.path.join(base_path, "assets", "images", "treasure.png")).convert_alpha()
img_ark = pygame.image.load(os.path.join(base_path, "assets", "images", "lost_ark.png")).convert_alpha()

# Redimensiona personagens e itens para o tamanho correto
img_dr_jones = pygame.transform.scale(img_dr_jones, (80, 100))
img_treasure = pygame.transform.scale(img_treasure, (70, 70))
img_ark = pygame.transform.scale(img_ark, (100, 100))

# Carrega texturas
sand_texture = pygame.image.load(os.path.join(base_path, "assets", "images", "sand_texture.jpeg")).convert()
rock_texture = pygame.image.load(os.path.join(base_path, "assets", "images", "rock_texture.jpeg")).convert()
grass_texture = pygame.image.load(os.path.join(base_path, "assets", "images", "grass_texture.jpeg")).convert()
swamp_texture = pygame.image.load(os.path.join(base_path, "assets", "images", "swamp_texture.png")).convert()
wall_texture = pygame.image.load(os.path.join(base_path, "assets", "images", "wall_texture.png")).convert()

# Uniformiza tamanho das texturas
sand_texture = pygame.transform.scale(sand_texture, (100, 100))
rock_texture = pygame.transform.scale(rock_texture, (100, 100))
grass_texture = pygame.transform.scale(grass_texture, (100, 100))
swamp_texture = pygame.transform.scale(swamp_texture, (100, 100))
wall_texture = pygame.transform.scale(wall_texture, (100, 100))


# Função que faz a animação do agente seguindo o caminho encontrado.
def animate_path(terrain_map, objects_map, path, screen, draw_func, imgs, delay=0.3):
    # Percorre cada posição do caminho
    for pos in path[1:]:
        x, y = pos

        # Remove agente da posição antiga
        for i, row in enumerate(objects_map):
            for j, val in enumerate(row):
                if val == 'J':
                    objects_map[i][j] = None

        # Remove tesouro se houver
        if objects_map[x][y] == 'T':
            objects_map[x][y] = None

        # Move agente para nova posição
        objects_map[x][y] = 'J'

        # Desenha o mapa atualizado
        draw_func(screen, terrain_map, objects_map, *imgs)
        pygame.display.update()
        pygame.time.wait(int(delay * 1000))

    return True

def main():
    # Gera os mapas de terreno e de objetos
    terrain_map, objects_map = map_generator.generate_maps()

    # Encontra a posição inicial do agente no mapa
    x, y = movement.find_agent(objects_map)

    # Cria o menu lateral
    menu = patterned_menu.Menu(screen, GAME_WIDTH, 0, MENU_WIDTH, HEIGHT)

    # Inicia o controle de tempo do jogo
    clock = pygame.time.Clock()

    # Variáveis de controle do estado do jogo
    game_finished = False
    final_cost = 0
    final_treasures = 0
    running = True

    while running:
        dt = clock.tick(60)/1000.0 

        # Lê os eventos do teclado e mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Só permite ações se o jogo ainda não terminou
            if not game_finished:
                clicked = menu.handle_event(event)

                # Botão: Busca em Profundidade
                if clicked == 'Profundidade':
                    path, cost, treasures, nodes_expanded = search_algorithms.depth_first_search(
                        terrain_map, objects_map, (x,y), (7,7))
                    if path:
                        # Anima o agente seguindo o caminho
                        animate_path(terrain_map, objects_map, path, screen,
                                 map_generator.draw_map, (img_dr_jones, img_treasure, img_ark, sand_texture, rock_texture, grass_texture, swamp_texture, wall_texture))
                        
                        game_finished   = True
                        final_cost      = cost
                        final_treasures = len(treasures)
                    else:
                        popup_message.show("Nenhum caminho disponível")

                # Botão: Busca em Largura
                elif clicked == 'Largura':
                    path, cost, treasures, nodes_expanded = search_algorithms.breadth_first_search(
                        terrain_map, objects_map, (x,y), (7,7))
                    if path:
                        # Anima o agente seguindo o caminho
                        animate_path(terrain_map, objects_map, path, screen,
                                 map_generator.draw_map, (img_dr_jones, img_treasure, img_ark, sand_texture, rock_texture, grass_texture, swamp_texture, wall_texture))
                        
                        game_finished   = True
                        final_cost      = cost
                        final_treasures = len(treasures)
                    else:
                        popup_message.show("Nenhum caminho disponível")

                # Botão: Busca Gulosa
                elif clicked == 'Gulosa':
                    path, cost, treasures, nodes_expanded = search_algorithms.greedy_search(
                        terrain_map, objects_map, (x,y), (7,7))
                    if path:
                        # Anima o agente seguindo o caminho
                        animate_path(terrain_map, objects_map, path, screen,
                                 map_generator.draw_map, (img_dr_jones, img_treasure, img_ark, sand_texture, rock_texture, grass_texture, swamp_texture, wall_texture))
                        
                        game_finished   = True
                        final_cost      = 0
                        final_treasures = len(treasures)
                    else:
                        popup_message.show("Nenhum caminho disponível")

                # Botão: A*
                elif clicked == 'A Estrela':
                    path, cost, treasures, nodes_expanded = search_algorithms.a_star_search(
                        terrain_map, objects_map, (x,y), (7,7))
                    if path:
                        # Anima o agente seguindo o caminho
                        animate_path(terrain_map, objects_map, path, screen,
                                 map_generator.draw_map, (img_dr_jones, img_treasure, img_ark, sand_texture, rock_texture, grass_texture, swamp_texture, wall_texture))
                        
                        game_finished   = True
                        final_cost      = cost
                        final_treasures = len(treasures)
                    else:
                        popup_message.show("Nenhum caminho disponível")

                # Botão: Comparar Algoritmos
                elif clicked == 'Comparar':
                    mensagem = comparar_algoritmos(terrain_map, objects_map, (x, y), (7, 7))
                    popup_message.show(mensagem)

                # Controle manual do agente com as setas do teclado
                elif event.type == pygame.KEYDOWN:
                    dir = None
                    if event.key == pygame.K_UP:    dir = 'up'
                    elif event.key == pygame.K_DOWN:  dir = 'down'
                    elif event.key == pygame.K_LEFT:  dir = 'left'
                    elif event.key == pygame.K_RIGHT: dir = 'right'
                    if dir:
                        x, y, over = movement.move_agent(
                            terrain_map, objects_map, x, y, dir)
                        if over:
                            game_finished   = True
                            final_cost      = 0
                            final_treasures = 0

        # Limpa a tela
        screen.fill((255,255,255))

        # Desenha o mapa e os elementos
        map_generator.draw_map(screen, terrain_map, objects_map,
                               img_dr_jones, img_treasure, img_ark,
                               sand_texture, rock_texture,
                               grass_texture, swamp_texture,
                               wall_texture)

        # Desenha o menu lateral e a caixa de pop-up
        menu.draw()
        popup_message.draw()

        # Pop Up de jogo concluído
        if game_finished:
            popup_message.show("Parabéns, você encontrou a arca!")

            # Posição e tamanho dos retângulos de resultado
            btn_height = 50
            btn_width  = MENU_WIDTH - 20
            btn_margin = 15
            x0 = GAME_WIDTH + 10
            y2 = HEIGHT - btn_margin - btn_height
            y1 = y2 - btn_margin - btn_height

            # Desenha caixas para custo e tesouros
            rect1 = pygame.Rect(x0, y1, btn_width, btn_height)
            rect2 = pygame.Rect(x0, y2, btn_width, btn_height)
            pygame.draw.rect(screen, (84, 64, 52), rect1)
            pygame.draw.rect(screen, (0, 0, 0), rect1, 2)
            pygame.draw.rect(screen, (84, 64, 52), rect2)
            pygame.draw.rect(screen, (0, 0, 0), rect2, 2)

            # Renderiza texto dos resultados
            text1 = score_font.render(f"Custo total: {final_cost}", True, (233, 214, 154))
            text2 = score_font.render(f"Tesouros:    {final_treasures}", True, (233, 214, 154))
            screen.blit(text1, text1.get_rect(center=rect1.center))
            screen.blit(text2, text2.get_rect(center=rect2.center))

        # Atualiza a tela com tudo renderizado
        pygame.display.update()

    # Finaliza o pygame ao sair do loop principal
    pygame.quit()


if __name__ == "__main__":
    main()