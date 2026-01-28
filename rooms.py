import pygame
import math

""" Cores usadas na sala e objetos """
GRAY   = (160, 160, 160)
WHITE  = (255, 255, 255)
BLUE   = (50, 50, 200)
GREEN  = (50, 200, 50)
YELLOW = (255, 220, 0)
DARK_YELLOW = (180, 150, 0)
DARK_GREEN = (20, 80, 20) 
CHALK = (240, 240, 230)

""" Cores para móveis """
BROWN = (139, 90, 43)          
DARK_BROWN = (101, 67, 33)      
LIGHT_BROWN = (181, 137, 87)    


class Room:
    """ 
    Rom
    ----------------------
    Representa uma sala no jogo com paredes, porta e lousa (quadro).
    A sala possui uma porta que pode ser aberta/fechada com animação
    usando interpolação linear entre keyframes discretos.
    A lousa dentro da sala exibe uma tarefa que pode ser marcada como concluída.
    """
    def __init__(self, x, y, w, h, door, button, draw_line, fill_rect, screen, board_text="Tarefa", get_camera=None, fill_circle=None, is_meeting_room=False):
        
        """
        Inicializa a sala com posição, dimensões, porta, lousa e funções de desenho.
        ----------------------
        Parâmetros:
        - x, y: Posição da sala no mundo
        - w, h: Dimensões da sala
        - door: Retângulo (x, y, w, h) representando a porta
        - button: Retângulo (x, y, w, h) representando a lousa (quadro)
        - draw_line: Função para desenhar linhas (com transformação de câmera)
        - fill_rect: Função para desenhar retângulos preenchidos (com transformação de câmera)
        - screen: Superfície do Pygame para desenhar texto
        - board_text: Texto a ser exibido na lousa
        - get_camera: Função para obter parâmetros da câmera (opcional)
        - fill_circle: Função para desenhar círculos preenchidos (para sala de reunião)
        - is_meeting_room: Se True, é sala de reunião (mesa redonda); se False, sala de aula
        
        """
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.door = door      
        self.button = button  
        self.completed = False
        self.draw_line = draw_line
        self.fill_rect = fill_rect
        self.fill_circle = fill_circle
        self.screen = screen
        self.board_text = board_text  
        self.get_camera = get_camera
        self.is_meeting_room = is_meeting_room 
        
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 12)

       
        self.door_open = False        
        self.door_opening = False     
        self.door_progress = 0.0      
        self.door_speed = 2.0         
        dx, dy, dw, dh = self.door
        x0, y0, w0, h0 = self.x, self.y, self.w, self.h

        door_cx = dx + dw / 2
        door_cy = dy + dh / 2

        dist_top = abs(door_cy - y0)
        dist_bottom = abs(door_cy - (y0 + h0))
        dist_left = abs(door_cx - x0)
        dist_right = abs(door_cx - (x0 + w0))

        self.door_side = min(
            [
                (dist_top, "top"),
                (dist_bottom, "bottom"),
                (dist_left, "left"),
                (dist_right, "right"),
            ],
            key=lambda t: t[0],
        )[1]

    def interact_door(self):
        """
        Interação com a porta
        ------------------------
        Inicia a animação de abrir/fechar a porta. Como acontece:
        - Se a porta está fechada, inicia a abertura.
        - Se a porta está aberta, inicia o fechamento.
        A animação é controlada pela variável door_opening.
        """
        if not self.door_opening:
            self.door_opening = True

    def update_door(self, dt):
        """
        Atualiza a animação da porta usando Interpolação Linear
        ------------------------
        Atualiza a posição da porta com base no tempo delta (dt)
        usando Interpolação Linear: door_progress = door_progress + speed * dt
        
        Keyframes discretos:
        - Keyframe 0 (t=0): door_progress = 0.0 (porta fechada)
        - Keyframe 1 (t=1): door_progress = 1.0 (porta aberta)
        
        A posição atual da porta é calculada por interpolação linear entre os keyframes.
        """
        if self.door_opening:
            if not self.door_open:
                self.door_progress += self.door_speed * dt
                if self.door_progress >= 1.0:
                    self.door_progress = 1.0
                    self.door_open = True
                    self.door_opening = False
            else:
                self.door_progress -= self.door_speed * dt
                if self.door_progress <= 0.0:
                    self.door_progress = 0.0
                    self.door_open = False
                    self.door_opening = False

    def get_door_collision_rect(self):
        """
        Colisão da Porta
        ------------------------
        Retorna o retângulo de colisão da porta (para verificar se jogador está sobre ela),
        utilizada para detectar se a porta está bloqueando passagem.

        """
        dx, dy, dw, dh = self.door
        return (dx, dy, dw, dh)

    def get_door_interaction_rect(self):
        """
        Área de Interação da Porta
        ------------------------
        Retorna uma área maior ao redor da porta para detectar interação (pressionar E).
        Usada para verificar se o jogador está próximo o suficiente para interagir com a porta.
        
        """
        dx, dy, dw, dh = self.door
        expand = 20
        return (dx - expand, dy - expand, dw + expand * 2, dh + expand * 2)

    def is_door_blocking(self):
        """Verifica se a porta está bloqueando passagem (não totalmente aberta)"""
        return self.door_progress < 0.9  

    def draw_desk(self, x, y, w, h):
        """
        Desenha uma mesa usando fill_rect (Scanline) e set_pixel
        ------------------------
        Mesa retangular com tampo marrom e bordas
        """
        self.fill_rect(x, y, w, h, LIGHT_BROWN)
        self.draw_line(x, y, x + w, y, DARK_BROWN)
        self.draw_line(x, y + h, x + w, y + h, DARK_BROWN)
        self.draw_line(x, y, x, y + h, DARK_BROWN)
        self.draw_line(x + w, y, x + w, y + h, DARK_BROWN)
        leg_w, leg_h = 3, 4
        self.fill_rect(x + 2, y + h, leg_w, leg_h, BROWN)
        self.fill_rect(x + w - leg_w - 2, y + h, leg_w, leg_h, BROWN)

    def draw_chair(self, x, y, facing="up"):
        """
        Desenha uma cadeira usando formas geométricas (fill_rect, draw_line)
        ------------------------
        Cadeira com assento e encosto
        facing: direção do encosto ("up", "down", "left", "right")
        """
        seat_w, seat_h = 12, 10
        back_thickness = 3
        
        self.fill_rect(x, y, seat_w, seat_h, BROWN)
        self.draw_line(x, y, x + seat_w, y, DARK_BROWN)
        self.draw_line(x, y + seat_h, x + seat_w, y + seat_h, DARK_BROWN)
        self.draw_line(x, y, x, y + seat_h, DARK_BROWN)
        self.draw_line(x + seat_w, y, x + seat_w, y + seat_h, DARK_BROWN)
        
        if facing == "up":
            self.fill_rect(x, y - back_thickness, seat_w, back_thickness, DARK_BROWN)
        elif facing == "down":
            self.fill_rect(x, y + seat_h, seat_w, back_thickness, DARK_BROWN)
        elif facing == "left":
            self.fill_rect(x - back_thickness, y, back_thickness, seat_h, DARK_BROWN)
        elif facing == "right":
            self.fill_rect(x + seat_w, y, back_thickness, seat_h, DARK_BROWN)

    def draw_classroom_furniture(self):
        """
        Desenha 4 mesas com 4 cadeiras para sala de aula
        ------------------------
        Usa Scanline (fill_rect) para preenchimento
        Mesas ficam atrás (em relação à lousa na frente)
        """
        base_x = self.x + 30
        base_y = self.y + 80  
        
        desk_w, desk_h = 40, 20
        gap_x, gap_y = 80, 45
        
        for row in range(2):
            for col in range(2):
                mx = base_x + col * gap_x
                my = base_y + row * gap_y
                
                """Mesa"""
                self.draw_desk(mx, my, desk_w, desk_h)
                
                """Cadeira atrás da mesa, encosto virado para lousa/frente"""
                chair_x = mx + (desk_w - 12) // 2
                chair_y = my + desk_h + 5
                self.draw_chair(chair_x, chair_y, facing="up")

    def draw_meeting_room_furniture(self):
        """
        Desenha mesa circular com cadeiras ao redor para sala de reunião
        ------------------------
        Mesa: círculo marrom (usando fill_circle)
        Cadeiras: formas geométricas ao redor
        """
        if self.fill_circle is None:
            return
        
        """ Mesa circular no centro da sala """
        table_cx = self.x + self.w // 2
        table_cy = self.y + self.h // 2 + 10
        table_radius = 30
        
        self.fill_circle(table_cx, table_cy, table_radius, LIGHT_BROWN)
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            px = table_cx + int(table_radius * math.cos(rad))
            py = table_cy + int(table_radius * math.sin(rad))
            self.draw_line(px, py, px + 1, py, DARK_BROWN)
        
        """ Desenha 6 cadeiras ao redor da mesa no GESAD"""
        chair_distance = table_radius + 20
        for i in range(6):
            angle = math.radians(i * 60) 
            cx = table_cx + int(chair_distance * math.cos(angle)) - 6
            cy = table_cy + int(chair_distance * math.sin(angle)) - 5
            
            if i == 0:
                facing = "left"
            elif i == 1:
                facing = "left"
            elif i == 2:
                facing = "up"
            elif i == 3:
                facing = "right"
            elif i == 4:
                facing = "right"
            else:
                facing = "down"
            
            self.draw_chair(cx, cy, facing)

    def draw(self):
        """
        Desenha a sala, porta e lousa (quadro)
        ------------------------
        Desenha a sala com paredes, porta com animação de abertura/fechamento
        e a lousa dentro da sala com o texto da tarefa.
        Usa as funções draw_line e fill_rect com transformação de câmera.
        """
        self.fill_rect(self.x, self.y, self.w, self.h, GRAY)
        
        """ Borda preta do retângulo da sala """
        BLACK = (0, 0, 0)
        self.draw_line(self.x, self.y, self.x + self.w, self.y, BLACK)
        self.draw_line(self.x, self.y + self.h, self.x + self.w, self.y + self.h, BLACK)
        self.draw_line(self.x, self.y, self.x, self.y + self.h, BLACK)
        self.draw_line(self.x + self.w, self.y, self.x + self.w, self.y + self.h, BLACK)
        
        dx, dy, dw, dh = self.door
        x, y, w, h = self.x, self.y, self.w, self.h
        side = self.door_side

        """ Paredes internas (pretas para contraste com fundo branco) """
        if side == "top":
            self.draw_line(x, y, dx, y, BLACK)
            self.draw_line(dx + dw, y, x + w, y, BLACK)
        else:
            self.draw_line(x, y, x + w, y, BLACK)

        if side == "bottom":
            self.draw_line(x, y + h, dx, y + h, BLACK)
            self.draw_line(dx + dw, y + h, x + w, y + h, BLACK)
        else:
            self.draw_line(x, y + h, x + w, y + h, BLACK)

        if side == "left":
            self.draw_line(x, y, x, dy, BLACK)
            self.draw_line(x, dy + dh, x, y + h, BLACK)
        else:
            self.draw_line(x, y, x, y + h, BLACK)

        if side == "right":
            self.draw_line(x + w, y, x + w, dy, BLACK)
            self.draw_line(x + w, dy + dh, x + w, y + h, BLACK)
        else:
            self.draw_line(x + w, y, x + w, y + h, WHITE)

        """ 
        Desenha a Porta (retângulo amarelo) com animação
        ------------------------
        Usa Interpolação Linear para posição da porta:
        pos_atual = pos_inicial + (pos_final - pos_inicial) * progress
        Ou seja: pos_atual = lerp(pos_inicial, pos_final, progress)
        Onde progress varia de 0.0 (fechada) a 1.0 (aberta).
        """
        
        if side in ["top", "bottom"]:
            offset = int(dw * self.door_progress)  
            door_draw_x = dx + offset
            door_draw_w = dw - offset 
            
            if door_draw_w > 0:
                self.fill_rect(door_draw_x, dy, door_draw_w, dh, YELLOW)
                self.draw_line(door_draw_x, dy, door_draw_x + door_draw_w, dy, DARK_YELLOW)
                self.draw_line(door_draw_x, dy + dh, door_draw_x + door_draw_w, dy + dh, DARK_YELLOW)
                self.draw_line(door_draw_x, dy, door_draw_x, dy + dh, DARK_YELLOW)
                self.draw_line(door_draw_x + door_draw_w, dy, door_draw_x + door_draw_w, dy + dh, DARK_YELLOW)
        else:
            door_draw_y = dy + offset
            door_draw_h = dh - offset  
            
            if door_draw_h > 0:
                self.fill_rect(dx, door_draw_y, dw, door_draw_h, YELLOW)
                self.draw_line(dx, door_draw_y, dx + dw, door_draw_y, DARK_YELLOW)
                self.draw_line(dx, door_draw_y + door_draw_h, dx + dw, door_draw_y + door_draw_h, DARK_YELLOW)
                self.draw_line(dx, door_draw_y, dx, door_draw_y + door_draw_h, DARK_YELLOW)
                self.draw_line(dx + dw, door_draw_y, dx + dw, door_draw_y + door_draw_h, DARK_YELLOW)

        """ Desenha móveis (mesas e cadeiras) """
        if self.is_meeting_room:
            self.draw_meeting_room_furniture()
        else:
            self.draw_classroom_furniture()

        bx, by, bw, bh = self.button
        
        """Cor da lousa: verde escuro (não completada) ou verde claro (completada)"""
        board_color = (40, 120, 40) if self.completed else DARK_GREEN
        self.fill_rect(bx, by, bw, bh, board_color)
        frame_color = (139, 90, 43)  
        frame_thickness = 3
        
        """Borda externa (moldura)"""
        for i in range(frame_thickness):
            self.draw_line(bx - i, by - i, bx + bw + i, by - i, frame_color)          
            self.draw_line(bx - i, by + bh + i, bx + bw + i, by + bh + i, frame_color)  
            self.draw_line(bx - i, by - i, bx - i, by + bh + i, frame_color)          
            self.draw_line(bx + bw + i, by - i, bx + bw + i, by + bh + i, frame_color)  
        
        """Borda interna branca (giz)"""
        self.draw_line(bx, by, bx + bw, by, CHALK)          
        self.draw_line(bx, by, bx, by + bh, CHALK)           
        self.draw_line(bx + bw, by, bx + bw, by + bh, CHALK)  
        self.draw_line(bx, by + bh, bx + bw, by + bh, CHALK)  
        
        """Desenha o texto na lousa (como se fosse escrito com giz), quando a tarefa está completa"""
        if self.completed:
            text = "Concluído!"
            text_color = (150, 255, 150)  
        else:
            text = self.board_text
            text_color = CHALK
        
        """Renderiza o texto e desenha na tela (com transformação de câmera)"""
        if self.get_camera:
            cam_x, cam_y, zoom, width, height = self.get_camera()
            screen_x = int((bx + bw // 2 - cam_x) * zoom + width / 2)
            screen_y = int((by + bh // 2 - cam_y) * zoom + height / 2)
            scaled_font = pygame.font.SysFont('Arial', int(12 * zoom))
            text_surface = scaled_font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=(screen_x, screen_y))
        else:
            text_surface = self.font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=(bx + bw // 2, by + bh // 2))
        
        self.screen.blit(text_surface, text_rect)