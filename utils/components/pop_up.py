import pygame 

# Classe para gerenciar janelas pop-up
class Popup: 
    def __init__(self, surface, game_width, game_height,
                 width=580, height=150, border_radius=12):
        # Superfície principal onde o pop-up será desenhado
        self.surface = surface

        # Dimensões da área de jogo
        self.game_width = game_width
        self.game_height = game_height

        # Tamanho da janela de pop-up e raio de cantos arredondados
        self.width = width
        self.height = height
        self.border_radius = border_radius

        # Fonte usada para renderizar o texto das mensagens
        self.font = pygame.font.SysFont('Arial', 28, bold=True)

        # Cores
        self.bg_color = (30, 30, 30, 220)
        self.text_color = (233, 214, 154)

        self.popup_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Flags de controle de visibilidade e mensagem atual
        self.visible = False
        self.message = ""

        # Retângulo do pop-up centralizado na área de jogo (ignora o menu)
        cx = self.game_width // 2
        cy = self.game_height // 2
        self.rect = self.popup_surface.get_rect(center=(cx, cy))

    # Exibe o pop-up com a mensagem fornecida.
    def show(self, message):
        self.message = message
        self.visible = True

    # Oculta o pop-up sem apagar a mensagem.
    def hide(self):
        self.visible = False

    # Desenha o pop-up na tela principal
    def draw(self):
        if not self.visible:
            return 

        # Limpa desenho anterior
        self.popup_surface.fill((0, 0, 0, 0))

        # Desenha o retângulo
        pygame.draw.rect(
            self.popup_surface,
            self.bg_color,
            self.popup_surface.get_rect(),
            border_radius=self.border_radius
        )

        # Quebra a mensagem em linhas para renderização separada
        lines = self.message.split('\n')
        text_surfs = [] 
        total_height = 0

        # Renderiza cada linha e soma a altura total
        for line in lines:
            surf = self.font.render(line, True, self.text_color)
            text_surfs.append(surf)
            total_height += surf.get_height()

        # Espaçamento mínimo entre linhas de texto
        line_spacing = 5
        total_height += line_spacing * (len(lines) - 1)

        # Calcula deslocamento vertical para centralizar texto
        y = (self.height - total_height) // 2

        # Blita cada linha no centro horizontal da superfície auxiliar
        for surf in text_surfs:
            rect = surf.get_rect(centerx=self.width // 2, y=y)
            self.popup_surface.blit(surf, rect)
            y += surf.get_height() + line_spacing

        # Desenha o pop-up pronto na tela principal
        self.surface.blit(self.popup_surface, self.rect.topleft)
