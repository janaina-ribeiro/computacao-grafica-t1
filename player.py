import pygame

GRAY  = (160, 160, 160)
WHITE = (255, 255, 255)
BLUE  = (50, 50, 200)
GREEN = (50, 200, 50)
RED  = (200, 50, 50)
BLACK = (0, 0, 0)


class Player:
    def __init__(self, x, y, draw_line, fill_rect):
        self.x, self.y = x, y
        # largura/altura do "corpo" lógico usado para colisão
        self.w, self.h = 20, 32
        self.speed = 5
        self.draw_line = draw_line
        self.fill_rect = fill_rect

    def draw(self):
        # Desenha o personagem usando apenas linhas de Bresenham
        # (draw_line) e, portanto, set_pixel.

        def filled_rect(x, y, w, h, fill_color, border_color=None):
            # Preenchimento por scanline usando draw_line (Bresenham)
            for iy in range(y, y + h):
                self.draw_line(x, iy, x + w - 1, iy, fill_color)

            # Borda opcional
            if border_color is not None:
                self.draw_line(x, y, x + w - 1, y, border_color)               # topo
                self.draw_line(x, y + h - 1, x + w - 1, y + h - 1, border_color)  # base
                self.draw_line(x, y, x, y + h - 1, border_color)               # esquerda
                self.draw_line(x + w - 1, y, x + w - 1, y + h - 1, border_color)  # direita

        px, py = self.x, self.y

        # Cores do personagem
        skin_color = (255, 220, 180)
        shirt_color = BLUE
        pants_color = (30, 30, 120)
        shoes_color = BLACK

        # Cabeça (quadrado)
        head_w = head_h = 10
        head_x = px + (self.w - head_w) // 2
        head_y = py
        filled_rect(head_x, head_y, head_w, head_h, skin_color, WHITE)

        # Tronco (camisa)
        body_w = self.w
        body_h = 12
        body_x = px
        body_y = head_y + head_h
        filled_rect(body_x, body_y, body_w, body_h, shirt_color, WHITE)

        # Calça
        pants_w = self.w
        pants_h = 8
        pants_x = px
        pants_y = body_y + body_h
        filled_rect(pants_x, pants_y, pants_w, pants_h, pants_color, WHITE)

        # Pernas/Sapatos (dois retângulos pequenos)
        leg_w = 6
        leg_h = 4
        gap = (self.w - 2 * leg_w) // 3
        left_leg_x = px + gap
        right_leg_x = px + gap * 2 + leg_w
        legs_y = pants_y + pants_h

        #Braços
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