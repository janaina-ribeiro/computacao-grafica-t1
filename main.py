import pygame
import sys
import math
from player import Player
from rooms import Room

""" Configuração da Tela e Cores"""
WIDTH, HEIGHT = 700, 500
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (160, 160, 160)
RED   = (200, 50, 50)
BLUE  = (50, 50, 200)
GREEN = (50, 200, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NC2A - Game")
clock = pygame.time.Clock()

""" Função set_pixel """
def set_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        screen.set_at((x, y), color)

""" Função draw_line (Bresenham) """
def draw_line(x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        set_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

""" Funções de desenho de retângulos """
def draw_rect(x, y, w, h, color):
    draw_line(x, y, x + w, y, color)
    draw_line(x, y, x, y + h, color)
    draw_line(x + w, y, x + w, y + h, color)
    draw_line(x, y + h, x + w, y + h, color)

""" Preenche um retângulo """
def fill_rect(x, y, w, h, color):
    for iy in range(y + 1, y + h):
        draw_line(x + 1, iy, x + w - 1, iy, color)



""" Verifica interseção entre retângulos (colisao)"""
def intersects(r1, r2):
    return r1.colliderect(pygame.Rect(*r2))

""" Barra de Progresso """
def draw_progress_bar(x, y, w, progress):
    draw_rect(x, y, w, 10, WHITE)
    fill = int(w * progress)
    if fill > 0:
        fill_rect(x, y, fill, 10, GREEN)

""" Configuração das 4 salas do jogo """
rooms = [
    Room(20, 20, 300, 200, (160, 220, 40, 10), (60, 60, 20, 20), draw_line, fill_rect),
    Room(380, 20, 300, 200, (520, 220, 40, 10), (420, 60, 20, 20), draw_line, fill_rect),
    Room(20, 260, 300, 200, (160, 260, 40, 10), (60, 300, 20, 20), draw_line, fill_rect),
    Room(380, 260, 300, 200, (520, 260, 40, 10), (420, 300, 20, 20), draw_line, fill_rect),
]

""" Cria retângulos de parede para colisão (exceto na porta) """
WALL_THICKNESS = 4
walls = []

for room in rooms:
    x, y, w, h = room.x, room.y, room.w, room.h
    dx, dy, dw, dh = room.door
    side = room.door_side

    left_x = x
    right_x = x + w
    top_y = y
    bottom_y = y + h

    if side == "top":
        # parede superior com abertura para a porta
        door_start = dx
        door_end = dx + dw
        if door_start > left_x:
            walls.append(pygame.Rect(left_x, top_y - WALL_THICKNESS, door_start - left_x, WALL_THICKNESS))
        if door_end < right_x:
            walls.append(pygame.Rect(door_end, top_y - WALL_THICKNESS, right_x - door_end, WALL_THICKNESS))

        # demais paredes completas
        walls.append(pygame.Rect(left_x, bottom_y, w, WALL_THICKNESS))
        walls.append(pygame.Rect(left_x - WALL_THICKNESS, top_y, WALL_THICKNESS, h))
        walls.append(pygame.Rect(right_x, top_y, WALL_THICKNESS, h))

    elif side == "bottom":
        # parede inferior com abertura para a porta
        door_start = dx
        door_end = dx + dw
        if door_start > left_x:
            walls.append(pygame.Rect(left_x, bottom_y, door_start - left_x, WALL_THICKNESS))
        if door_end < right_x:
            walls.append(pygame.Rect(door_end, bottom_y, right_x - door_end, WALL_THICKNESS))

        # demais paredes completas
        walls.append(pygame.Rect(left_x, top_y - WALL_THICKNESS, w, WALL_THICKNESS))
        walls.append(pygame.Rect(left_x - WALL_THICKNESS, top_y, WALL_THICKNESS, h))
        walls.append(pygame.Rect(right_x, top_y, WALL_THICKNESS, h))

    elif side == "left":
        # parede esquerda com abertura para a porta
        door_start = dy
        door_end = dy + dh
        if door_start > top_y:
            walls.append(pygame.Rect(left_x - WALL_THICKNESS, top_y, WALL_THICKNESS, door_start - top_y))
        if door_end < bottom_y:
            walls.append(pygame.Rect(left_x - WALL_THICKNESS, door_end, WALL_THICKNESS, bottom_y - door_end))

        # demais paredes completas
        walls.append(pygame.Rect(left_x, top_y - WALL_THICKNESS, w, WALL_THICKNESS))
        walls.append(pygame.Rect(left_x, bottom_y, w, WALL_THICKNESS))
        walls.append(pygame.Rect(right_x, top_y, WALL_THICKNESS, h))

    elif side == "right":
        # parede direita com abertura para a porta
        door_start = dy
        door_end = dy + dh
        if door_start > top_y:
            walls.append(pygame.Rect(right_x, top_y, WALL_THICKNESS, door_start - top_y))
        if door_end < bottom_y:
            walls.append(pygame.Rect(right_x, door_end, WALL_THICKNESS, bottom_y - door_end))

        # demais paredes completas
        walls.append(pygame.Rect(left_x, top_y - WALL_THICKNESS, w, WALL_THICKNESS))
        walls.append(pygame.Rect(left_x, bottom_y, w, WALL_THICKNESS))
        walls.append(pygame.Rect(left_x - WALL_THICKNESS, top_y, WALL_THICKNESS, h))

""" Inicialização do Jogador e Variáveis do Jogo """
current_room = 0 
player = Player(100, 100, draw_line, fill_rect)

task_active = False
task_progress = 0.0
active_room = None

""" Loop Principal do Jogo """
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    """ Captura de Eventos """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    """ Captura de Teclas Pressionadas e movimento com colisão nas paredes """
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0
    if keys[pygame.K_w]:
        dy -= player.speed
    if keys[pygame.K_s]:
        dy += player.speed
    if keys[pygame.K_a]:
        dx -= player.speed
    if keys[pygame.K_d]:
        dx += player.speed

    # movimento no eixo X com colisão
    if dx != 0:
        player.x += dx
        for wall in walls:
            if player.rect().colliderect(wall):
                if dx > 0:
                    player.x = wall.left - player.w
                else:
                    player.x = wall.right
                break

    # movimento no eixo Y com colisão
    if dy != 0:
        player.y += dy
        for wall in walls:
            if player.rect().colliderect(wall):
                if dy > 0:
                    player.y = wall.top - player.h
                else:
                    player.y = wall.bottom
                break

    """ Desenha as Salas do NC2A """
    for room in rooms:
        room.draw()

    """ Lógica de Interação com Botões nas Salas (que podem ser outros elementos)"""
    if not task_active:
        active_room = None
        for room in rooms:
            if intersects(player.rect(), room.button):
                if keys[pygame.K_e] and not room.completed:
                    task_active = True
                    active_room = room

    """ Atualiza a Barra de Progresso se uma Tarefa estiver Ativa """
    if task_active and active_room is not None:
        task_progress += 1.0 / FPS
        task_progress = min(task_progress, 1.0)
        draw_progress_bar(250, 470, 200, task_progress)

        if task_progress >= 1.0:
            task_progress = 0.0
            task_active = False
            active_room.completed = True

    """ Desenha o Jogador """
    player.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
