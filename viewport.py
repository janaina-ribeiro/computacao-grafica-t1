import pygame
import math
from constants import WIDTH, HEIGHT, BLACK, WHITE, GRAY, RED

""" Cores para móveis no mini-mapa """
BROWN = (139, 90, 43)
LIGHT_BROWN = (181, 137, 87)


class Viewport:
    """
    Classe Viewport
    ----------------
    Gerencia o mini-mapa do jogo usando uma matriz de cores.
    """
    
    def __init__(self, screen, graphics):
        """
        Inicializa o sistema de viewport.
        
        Parâmetros:
        - screen: Superfície do Pygame
        - graphics: Instância da classe Graphics
        """
        self.screen = screen
        self.graphics = graphics
        self.title_font = pygame.font.SysFont('Arial', 12)
    
    def create_matrix(self, player, rooms, walls, grid_width=90, grid_height=70):
        """
        Cria a matriz do mini-mapa
        ---------------------------
        Converte o mundo de coordenadas para uma matriz com cores reais.
        Cada célula da matriz representa 10x10 pixels do mundo.
        Inclui mesas e cadeiras.
        """
        cell_size = 10
        matrix = [[WHITE for _ in range(grid_width)] for _ in range(grid_height)]
        
        for room in rooms:
            x_start = room.x // cell_size
            y_start = room.y // cell_size
            x_end = (room.x + room.w) // cell_size
            y_end = (room.y + room.h) // cell_size
            
            for i in range(max(0, y_start), min(grid_height, y_end)):
                for j in range(max(0, x_start), min(grid_width, x_end)):
                    matrix[i][j] = GRAY
            
            """Desenha as paredes da sala (preto para contrastar com fundo branco)"""
            for j in range(max(0, x_start), min(grid_width, x_end)):
                if 0 <= y_start < grid_height:
                    matrix[y_start][j] = BLACK
            for j in range(max(0, x_start), min(grid_width, x_end)):
                if 0 <= y_end - 1 < grid_height:
                    matrix[y_end - 1][j] = BLACK
            for i in range(max(0, y_start), min(grid_height, y_end)):
                if 0 <= x_start < grid_width:
                    matrix[i][x_start] = BLACK
            for i in range(max(0, y_start), min(grid_height, y_end)):
                if 0 <= x_end - 1 < grid_width:
                    matrix[i][x_end - 1] = BLACK

            """Desenha a porta na sala"""
            dx, dy, dw, dh = room.door
            door_x_start = dx // cell_size
            door_y_start = dy // cell_size
            door_x_end = (dx + dw) // cell_size
            door_y_end = (dy + dh) // cell_size
            
            door_color = (255, 220, 0) if room.is_door_blocking() else (100, 100, 100)
            
            for i in range(max(0, door_y_start), min(grid_height, door_y_end + 1)):
                for j in range(max(0, door_x_start), min(grid_width, door_x_end + 1)):
                    if 0 <= i < grid_height and 0 <= j < grid_width:
                        matrix[i][j] = door_color

            bx, by, bw, bh = room.button
            btn_color = (40, 120, 40) if room.completed else (20, 80, 20)
            btn_x_start = bx // cell_size
            btn_y_start = by // cell_size
            btn_x_end = (bx + bw) // cell_size
            btn_y_end = (by + bh) // cell_size
            
            for i in range(max(0, btn_y_start), min(grid_height, btn_y_end + 1)):
                for j in range(max(0, btn_x_start), min(grid_width, btn_x_end + 1)):
                    if 0 <= i < grid_height and 0 <= j < grid_width:
                        matrix[i][j] = btn_color
            
            """ Desenha mesas e cadeiras no mini-mapa """
            if room.is_meeting_room:
                table_cx = (room.x + room.w // 2) // cell_size
                table_cy = (room.y + room.h // 2 + 10) // cell_size
                table_r = 3  
                for dy in range(-table_r, table_r + 1):
                    for dx in range(-table_r, table_r + 1):
                        if dx*dx + dy*dy <= table_r*table_r:
                            ti, tj = table_cy + dy, table_cx + dx
                            if 0 <= ti < grid_height and 0 <= tj < grid_width:
                                matrix[ti][tj] = LIGHT_BROWN
            else:
                base_x = room.x + 30
                base_y = room.y + 80
                desk_w, desk_h = 40, 20
                gap_x, gap_y = 80, 45
                
                for row in range(2):
                    for col in range(2):
                        mx = base_x + col * gap_x
                        my = base_y + row * gap_y
                        
                        """ Mesa no mini-mapa """
                        mx_start = mx // cell_size
                        my_start = my // cell_size
                        mx_end = (mx + desk_w) // cell_size
                        my_end = (my + desk_h) // cell_size
                        
                        for i in range(max(0, my_start), min(grid_height, my_end + 1)):
                            for j in range(max(0, mx_start), min(grid_width, mx_end + 1)):
                                if 0 <= i < grid_height and 0 <= j < grid_width:
                                    matrix[i][j] = LIGHT_BROWN
                        
                        chair_x = mx + (desk_w - 12) // 2
                        chair_y = my + desk_h + 5
                        cx_start = chair_x // cell_size
                        cy_start = chair_y // cell_size
                        
                        if 0 <= cy_start < grid_height and 0 <= cx_start < grid_width:
                            matrix[cy_start][cx_start] = BROWN
        
        """Desenha o jogador (vermelho, maior para visibilidade)"""
        player_x = player.x // cell_size
        player_y = player.y // cell_size
        player_w = max(2, player.w // cell_size)
        player_h = max(3, player.h // cell_size)
        
        for i in range(max(0, player_y), min(grid_height, player_y + player_h)):
            for j in range(max(0, player_x), min(grid_width, player_x + player_w)):
                if 0 <= i < grid_height and 0 <= j < grid_width:
                    matrix[i][j] = RED
        
        return matrix
    
    def draw(self, matrix, vp_x, vp_y, vp_scale=3):
        """
        Desenha o mini-mapa usando APENAS set_pixel
        """
        grid_height = len(matrix)
        grid_width = len(matrix[0]) if grid_height > 0 else 0
        
        for i, row in enumerate(matrix):
            for j, color in enumerate(row):
                for dy in range(vp_scale):
                    for dx in range(vp_scale):
                        px = vp_x + j * vp_scale + dx
                        py = vp_y + i * vp_scale + dy
                        if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                            self.screen.set_at((px, py), color)
        
        """Borda da viewport"""
        vp_width = grid_width * vp_scale
        vp_height = grid_height * vp_scale
        self.graphics.draw_line(vp_x - 1, vp_y - 1, vp_x + vp_width, vp_y - 1, BLACK, False)
        self.graphics.draw_line(vp_x - 1, vp_y + vp_height, vp_x + vp_width, vp_y + vp_height, BLACK, False)
        self.graphics.draw_line(vp_x - 1, vp_y - 1, vp_x - 1, vp_y + vp_height, BLACK, False)
        self.graphics.draw_line(vp_x + vp_width, vp_y - 1, vp_x + vp_width, vp_y + vp_height, BLACK, False)
        
        """Título do mini-mapa"""
        title = self.title_font.render("MAPA NC2A", True, BLACK)
        self.screen.blit(title, (vp_x + vp_width // 2 - title.get_width() // 2, vp_y - 15))
