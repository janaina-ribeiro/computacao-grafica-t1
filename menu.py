import pygame
from constants import WIDTH, HEIGHT, WHITE, YELLOW, BLUE, DARK_GRAY, BLACK, GREEN


class MenuSystem:
    """
    Classe MenuSystem
    ------------------
    Gerencia a renderização e interação dos menus do jogo.
    """
    
    def __init__(self, screen, graphics):
        """
        Inicializa o sistema de menus.
        
        Parâmetros:
        - screen: Superfície do Pygame
        - graphics: Instância da classe Graphics
        """
        self.screen = screen
        self.graphics = graphics
        
        pygame.font.init()
        self.menu_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.game_font = pygame.font.SysFont('Arial', 18, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 14)
        
        self.selected = 0
    
    def draw_splash_screen(self):
        """
        Desenha a Splash Screen (Intro)
        """
        self.screen.fill(BLACK)
        
        # Title
        title = self.menu_font.render("Trabalho de Computação Gráfica", True, YELLOW)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        
        # Team Header
        team_header = self.game_font.render("Equipe:", True, BLUE)
        self.screen.blit(team_header, (WIDTH // 2 - team_header.get_width() // 2, HEIGHT // 2))
        
        # Team Members
        members = [
            "Janaína Ribeiro",
            "Joaquim Ribeiro",
            "Marcio Gabriel",
            "Suyane Carvalho"
        ]
        
        y_offset = HEIGHT // 2 + 30
        for member in members:
            text = self.game_font.render(member, True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 25

    def draw_main_menu(self, rotation_angle):
        """
        Desenha o menu principal usando FLOOD FILL para preenchimento.
        
        ALGORITMO DE PREENCHIMENTO:
        - Menu (tela inicial): usa FLOOD FILL
        - Jogo: usa SCANLINE
        
        Parâmetros:
        - rotation_angle: Ângulo atual para animação dos ventiladores
        """
        """Fundo com textura (scanline - preparação do fundo)"""
        self.graphics.fill_rect_textured(0, 0, WIDTH, HEIGHT, "checker", use_camera=False)
        
        """Caixa central - usa FLOOD FILL para preenchimento!"""
        box_w, box_h = 400, 350
        box_x = (WIDTH - box_w) // 2
        box_y = (HEIGHT - box_h) // 2
        
        """Usa flood_fill_rect: desenha borda e preenche com Flood Fill"""
        self.graphics.flood_fill_rect(box_x, box_y, box_w, box_h, DARK_GRAY, WHITE)
        
        """Título"""
        title = self.menu_font.render("NC2A - GAME", True, YELLOW)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, box_y + 30))
        
        """Opções"""
        options = ["Iniciar Jogo", "Controles de Teclas", "Sair"]
        option_y = box_y + 120
        
        for i, option in enumerate(options):
            color = YELLOW if i == self.selected else WHITE
            if i == self.selected:
                self.graphics.fill_circle(box_x + 50, option_y + 15, 8, YELLOW, use_camera=False)
            else:
                self.graphics.draw_circle(box_x + 50, option_y + 15, 8, WHITE, use_camera=False)
            
            text = self.game_font.render(option, True, color)
            self.screen.blit(text, (box_x + 80, option_y))
            option_y += 50
        
        instructions = self.small_font.render("W/S ou Mouse: navegar | ENTER/Click: selecionar", True, WHITE)
        self.screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, box_y + box_h - 40))
        
        """Ventiladores animados"""
        self.graphics.draw_fan(box_x + 350, box_y + 50, 25, rotation_angle, WHITE, use_camera=False)
        self.graphics.draw_fan(box_x + 50, box_y + 300, 20, -rotation_angle * 1.5, BLUE, use_camera=False)
    
    def draw_pause_menu(self):
        """Desenha o menu de pausa"""
        for y in range(0, HEIGHT, 2):
            for x in range(0, WIDTH, 2):
                self.screen.set_at((x, y), (0, 0, 0))
        
        box_w, box_h = 300, 200
        box_x = (WIDTH - box_w) // 2
        box_y = (HEIGHT - box_h) // 2
        
        self.graphics.fill_rect(box_x, box_y, box_w, box_h, DARK_GRAY, use_camera=False)
        self.graphics.draw_rect(box_x, box_y, box_w, box_h, WHITE, use_camera=False)
        
        title = self.game_font.render("PAUSADO", True, YELLOW)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, box_y + 20))
        
        options = ["Continuar", "Menu Principal", "Sair"]
        option_y = box_y + 70
        
        for i, option in enumerate(options):
            color = YELLOW if i == self.selected else WHITE
            if i == self.selected:
                self.graphics.fill_circle(box_x + 30, option_y + 10, 6, YELLOW, use_camera=False)
            else:
                self.graphics.draw_circle(box_x + 30, option_y + 10, 6, WHITE, use_camera=False)
            
            text = self.small_font.render(option, True, color)
            self.screen.blit(text, (box_x + 50, option_y))
            option_y += 40

    def draw_congrats_screen(self):
        """Desenha a tela de Parabéns"""
        self.screen.fill(BLACK)
        
        # Confetti effect (simple random dots)
        import random
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = random.choice([YELLOW, BLUE, GREEN, WHITE])
            self.graphics.set_pixel(x, y, color, use_camera=False)
            
        title = self.menu_font.render("PARABÉNS!", True, GREEN)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        
        subtitle = self.game_font.render("Todas as tarefas foram completadas.", True, WHITE)
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 + 10))
        
        info = self.small_font.render("Pressione qualquer tecla para voltar ao menu...", True, DARK_GRAY)
        self.screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT - 50))
    
    def draw_controls_screen(self):
        """Desenha tela de controles"""
        self.graphics.fill_rect(0, 0, WIDTH, HEIGHT, DARK_GRAY, use_camera=False)
        
        title = self.menu_font.render("CONTROLES", True, YELLOW)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        controls = [
            "W/Seta Cima - Mover para cima",
            "S/Seta Baixo - Mover para baixo",
            "A/Seta Esquerda - Mover para esquerda",
            "D/Seta Direita - Mover para direita",
            "E - Interagir (portas e lousas)",
            "ESC - Pausar jogo",
            "Mouse - Navegar menus e clicar em portas/lousas",
            "+  Zoom in",
            "-  Zoom out",
        ]
        
        y = 150
        for control in controls:
            text = self.game_font.render(control, True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 40
        
        back = self.small_font.render("Pressione qualquer tecla para voltar", True, YELLOW)
        self.screen.blit(back, (WIDTH // 2 - back.get_width() // 2, HEIGHT - 50))
    
    def get_main_menu_option_rect(self, index):
        """Retorna o retângulo de uma opção do menu principal para detecção de mouse"""
        box_x = (WIDTH - 400) // 2
        box_y = (HEIGHT - 350) // 2
        return pygame.Rect(box_x + 40, box_y + 120 + index * 50 - 5, 320, 40)
    
    def get_pause_menu_option_rect(self, index):
        """Retorna o retângulo de uma opção do menu de pausa para detecção de mouse"""
        box_x = (WIDTH - 300) // 2
        box_y = (HEIGHT - 200) // 2
        return pygame.Rect(box_x + 20, box_y + 70 + index * 40 - 5, 260, 30)
