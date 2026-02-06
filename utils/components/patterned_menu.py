import pygame

# Menu lateral com botões
class Menu:
    def __init__(self, surface, x, y, width, height):
        # Superfície principal para renderização
        self.surface = surface       

        # Posição horizontal do menu
        self.x = x                  

        # Posição vertical do menu
        self.y = y                   

        # Largura total do menu
        self.width = width          

        # Altura total do menu
        self.height = height         
        
        # Lista para armazenar botões
        self.buttons = []            

        # Fonte para texto dos botões
        self.font = pygame.font.SysFont('Arial', 24)  
        
        # Definições de altura, largura e espaçamento dos botões
        btn_height = 50
        btn_width = self.width - 20
        btn_margin = 15
        
        # Nomes correspondentes às ações de busca e comparação
        button_names = ['Depth First', 'Breadth First', 'Greedy', 'A Star', 'Compare']
        
        # Cria retângulos e associa cada nome a um botão
        for i, name in enumerate(button_names):
            rect = pygame.Rect(
                self.x + 10,
                self.y + 10 + i * (btn_height + btn_margin),
                btn_width,
                btn_height
            )
            self.buttons.append({'name': name, 'rect': rect})

    # Desenha o painel do menu e seus botões
    def draw(self):
        
        # Desenha fundo retangular do menu
        pygame.draw.rect(
            self.surface,
            (30, 30, 30),
            (self.x, self.y, self.width, self.height)
        )
        
        # Itera sobre cada botão para desenhar
        for btn in self.buttons:
            # Fundo do botão
            pygame.draw.rect(
                self.surface,
                (233, 214, 154),
                btn['rect']
            )

            # Borda preta para contorno
            pygame.draw.rect(
                self.surface,
                (0, 0, 0),   
                btn['rect'],
                2               
            )
            
            # Renderiza o texto do botão e centraliza
            text_surf = self.font.render(btn['name'], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=btn['rect'].center)
            self.surface.blit(text_surf, text_rect)

    # Processa eventos de mouse para detectar cliques em botões
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos  # posição do clique

            # Verifica colisão com cada botão
            for btn in self.buttons:
                if btn['rect'].collidepoint(pos):
                    return btn['name']
                
        return None
