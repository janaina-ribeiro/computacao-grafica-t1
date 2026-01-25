import pygame

""" Cores usadas no personagem """
GRAY  = (160, 160, 160)
WHITE = (255, 255, 255)
BLUE  = (50, 50, 200)
GREEN = (50, 200, 50)
RED  = (200, 50, 50)
BLACK = (0, 0, 0)
BROWN = (20, 20, 20)


class Player:
    def __init__(self, x, y, draw_line, fill_rect, get_camera=None, screen=None):

        """ 
        Posição inicial do personagem 
        --------------------------
        Define a posição inicial do personagem no mundo (x, y)
        e faz referência às funções de desenho passadas como parâmetros.
        São recebidos as posições x e y e as funções draw_line e fill_rect
        como parametros para desenhar o personagem.
        
        """
        self.x, self.y = x, y
        """ largura/altura do "corpo" lógico usado para colisão """
        self.w, self.h = 20, 32
        
        """ Velocidade melhorada + sprint """
        self.base_speed = 8       
        self.sprint_speed = 14    
        self.speed = self.base_speed
        
        self.draw_line = draw_line
        self.fill_rect = fill_rect
        self.get_camera = get_camera
        self.screen = screen
        
        """ Fonte pequena para nome na camisa """
        pygame.font.init()
        self.name_font = pygame.font.SysFont('Arial', 5)
    
    def update_speed(self, keys):
        """
        Atualiza a velocidade do jogador
        --------------------------------
        Segure SHIFT para correr mais rápido (sprint)
        """
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.speed = self.sprint_speed
        else:
            self.speed = self.base_speed

    def draw(self):
        """ 
        Desenha o personagem
        --------------------------
        Desenha o personagem usando fill_rect e draw_line
        As funções já aplicam a transformação da câmera. 
        
        O personagem é desenhado como um boneco palito simples com:
        - Cabeça (quadrado)
        - Tronco (retângulo)
        - Braços (retângulos)
        - Pernas/Sapatos (dois retângulos pequenos)
        
        """

        def filled_rect(x, y, w, h, fill_color, border_color=None):
            self.fill_rect(x, y, w, h, fill_color)

            if border_color is not None:
                self.draw_line(x, y, x + w - 1, y, border_color)              
                self.draw_line(x, y + h - 1, x + w - 1, y + h - 1, border_color) 
                self.draw_line(x, y, x, y + h - 1, border_color)              
                self.draw_line(x + w - 1, y, x + w - 1, y + h - 1, border_color)  

        px, py = self.x, self.y

        """ Cores do personagem """
        skin_color = (255, 220, 180)
        shirt_color = BLUE
        pants_color = (30, 30, 120)
        shoes_color = BLACK

        """ Cabeça (quadrado) """
        head_w = head_h = 10
        head_x = px + (self.w - head_w) // 2
        head_y = py
        filled_rect(head_x, head_y, head_w, head_h, skin_color, WHITE)
        
        """
        ========================================
        DETALHES FACIAIS - Usando APENAS set_pixel e Scanline
        ========================================
        Desenha cabelo, olhos, nariz, boca e óculos
        diretamente com screen.set_at() (set_pixel)
        """
        if self.screen is not None and self.get_camera is not None:
            cam_x, cam_y, zoom, width, height = self.get_camera()
            
            hair_color = BROWN  
            eye_color = (50, 50, 50)      
            eye_white = WHITE
            mouth_color = (180, 80, 80)  
            nose_color = (230, 180, 150) 
            glasses_color = (40, 40, 40)  
            lens_color = (180, 220, 255)  
            
            def world_to_screen(wx, wy):
                """Converte coordenadas do mundo para tela"""
                sx = int((wx - cam_x) * zoom + width / 2)
                sy = int((wy - cam_y) * zoom + height / 2)
                return sx, sy
            
            def set_pixel_safe(sx, sy, color):
                """Set pixel com verificação de limites"""
                if 0 <= sx < width and 0 <= sy < height:
                    self.screen.set_at((sx, sy), color)
            

            hair_start_x = head_x
            hair_start_y = head_y
            hair_w = head_w
            hair_h = 3
            
            for hy in range(hair_h):
                world_y = hair_start_y + hy
                for hx in range(hair_w):
                    world_x = hair_start_x + hx
                    sx, sy = world_to_screen(world_x, world_y)
                    for dzy in range(int(zoom)):
                        for dzx in range(int(zoom)):
                            set_pixel_safe(sx + dzx, sy + dzy, hair_color)
            
            fringe_y = head_y + 2
            for fx in range(head_w - 2):
                world_x = head_x + 1 + fx
                sx, sy = world_to_screen(world_x, fringe_y)
                if fx % 2 == 0: 
                    for dzy in range(int(zoom)):
                        for dzx in range(int(zoom)):
                            set_pixel_safe(sx + dzx, sy + dzy, hair_color)
            

            left_eye_x = head_x + 2
            left_eye_y = head_y + 4
            
            right_eye_x = head_x + 7
            right_eye_y = head_y + 4
            
            for eye_x in [left_eye_x, right_eye_x]:
                for ey in range(2):
                    for ex in range(2):
                        wx = eye_x + ex
                        wy = left_eye_y + ey
                        sx, sy = world_to_screen(wx, wy)
                        for dzy in range(int(zoom)):
                            for dzx in range(int(zoom)):
                                set_pixel_safe(sx + dzx, sy + dzy, eye_white)
            
            for eye_x in [left_eye_x + 1, right_eye_x]:
                sx, sy = world_to_screen(eye_x, left_eye_y + 1)
                for dzy in range(int(zoom)):
                    for dzx in range(int(zoom)):
                        set_pixel_safe(sx + dzx, sy + dzy, eye_color)
            

            lens_left_x = head_x + 1
            lens_y = head_y + 3
            
            lens_right_x = head_x + 6
            
            for lens_x in [lens_left_x, lens_right_x]:
                for ly in range(3):
                    for lx in range(3):
                        wx = lens_x + lx
                        wy = lens_y + ly
                        sx, sy = world_to_screen(wx, wy)
                        if ly == 0 or ly == 2 or lx == 0 or lx == 2:
                            for dzy in range(int(zoom)):
                                for dzx in range(int(zoom)):
                                    set_pixel_safe(sx + dzx, sy + dzy, glasses_color)
                        else:
                            for dzy in range(int(zoom)):
                                for dzx in range(int(zoom)):
                                    set_pixel_safe(sx + dzx, sy + dzy, lens_color)
            
            bridge_y = head_y + 4
            for bx in range(2):
                wx = head_x + 4 + bx
                sx, sy = world_to_screen(wx, bridge_y)
                for dzy in range(int(zoom)):
                    for dzx in range(int(zoom)):
                        set_pixel_safe(sx + dzx, sy + dzy, glasses_color)
            
            """ Hastes do óculos (lados) """
            sx, sy = world_to_screen(head_x, head_y + 4)
            for dzy in range(int(zoom)):
                for dzx in range(int(zoom)):
                    set_pixel_safe(sx + dzx, sy + dzy, glasses_color)
            
            sx, sy = world_to_screen(head_x + head_w - 1, head_y + 4)
            for dzy in range(int(zoom)):
                for dzx in range(int(zoom)):
                    set_pixel_safe(sx + dzx, sy + dzy, glasses_color)

            nose_x = head_x + head_w // 2
            nose_y = head_y + 5
            
            for ny in range(2):
                sx, sy = world_to_screen(nose_x, nose_y + ny)
                for dzy in range(int(zoom)):
                    for dzx in range(int(zoom)):
                        set_pixel_safe(sx + dzx, sy + dzy, nose_color)
            
            mouth_x = head_x + 3
            mouth_y = head_y + 8
            mouth_width = 4
            
            for mx in range(mouth_width):
                wx = mouth_x + mx
                sx, sy = world_to_screen(wx, mouth_y)
                for dzy in range(int(zoom)):
                    for dzx in range(int(zoom)):
                        set_pixel_safe(sx + dzx, sy + dzy, mouth_color)

        """ Tronco (camisa) """
        body_w = self.w
        body_h = 12
        body_x = px
        body_y = head_y + head_h
        filled_rect(body_x, body_y, body_w, body_h, shirt_color, WHITE)
        
        if self.screen is not None and self.get_camera is not None:
            cam_x, cam_y, zoom, width, height = self.get_camera()
            text_world_x = body_x + body_w // 2
            text_world_y = body_y + body_h // 2
            screen_x = int((text_world_x - cam_x) * zoom + width / 2)
            screen_y = int((text_world_y - cam_y) * zoom + height / 2)
            scaled_size = max(4, int(5 * zoom))
            scaled_font = pygame.font.SysFont('Arial', scaled_size)
            name_surface = scaled_font.render("GESAD", True, WHITE)
            name_rect = name_surface.get_rect(center=(screen_x, screen_y))
            self.screen.blit(name_surface, name_rect)

        """ Calça """
        pants_w = self.w
        pants_h = 8
        pants_x = px
        pants_y = body_y + body_h
        filled_rect(pants_x, pants_y, pants_w, pants_h, pants_color, WHITE)

        """ Pernas/Sapatos (dois retângulos pequenos) """
        leg_w = 6
        leg_h = 4
        gap = (self.w - 2 * leg_w) // 3
        left_leg_x = px + gap
        right_leg_x = px + gap * 2 + leg_w
        legs_y = pants_y + pants_h

        """ Braços """
        arm_w = 4
        arm_h = 12
        left_arm_x = px - arm_w
        right_arm_x = px + self.w
        arms_y = body_y
        
        filled_rect(left_arm_x, arms_y, arm_w, arm_h, skin_color, WHITE)
        filled_rect(right_arm_x, arms_y, arm_w, arm_h, skin_color, WHITE)
        filled_rect(left_leg_x, legs_y, leg_w, leg_h, shoes_color, WHITE)
        filled_rect(right_leg_x, legs_y, leg_w, leg_h, shoes_color, WHITE)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)