import pygame
import sys

from constants import (
    WIDTH, HEIGHT, FPS, BLACK, WHITE,
    GAME_STATE_MENU, GAME_STATE_PLAYING, GAME_STATE_PAUSED, GAME_STATE_SPLASH, GAME_STATE_CONGRATS
)
from camera import Camera
from graphics import Graphics
from viewport import Viewport
from menu import MenuSystem
from game import Game
from player import Player

def draw_background(screen, width, height):
    """
    Gera um fundo com gradiente vertical para o jogo.
    """
    screen.fill((245, 245, 245))

    for y in range(height):
        factor = y / height
        shade = int(100 * factor)

        color = (
            245 - shade,
            245 - shade,
            245 - shade
        )

        pygame.draw.line(screen, color, (0, y), (width, y))

def main():
    """
        Ponto de Entrada do Jogo NC2A
        =========================================
        Este arquivo é o ponto de entrada principal do jogo.
        Coordena todos os módulos e executa o loop principal.
        
        Estrutura Modular:
        ------------------
        - constants.py       : Constantes e configurações (cores, dimensões, estados)
        - camera.py          : Sistema de câmera (posição, zoom, transformações)
        - clipping.py        : Algoritmo de Cohen-Sutherland para clipping de linhas
        - transformations.py : Transformações geométricas (rotação, escala, translação)
        - graphics.py        : Primitivas de desenho (set_pixel, linha, círculo, texturas)
        - viewport.py        : Sistema de mini-mapa
        - menu.py            : Sistema de menus (principal, pausa, controles)
        - game.py            : Lógica principal do jogo (salas, colisão, tarefas)
        - rooms.py           : Classe das salas (portas, lousas, animação)
        - player.py          : Classe do jogador (movimento, desenho)
    """

    """Inicialização do Pygame"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NC2A - Game")
    clock = pygame.time.Clock()
    
    """Inicializa sistemas"""
    camera = Camera()
    graphics = Graphics(screen, camera)
    viewport = Viewport(screen, graphics)
    menu_system = MenuSystem(screen, graphics)
    
    """Cria o jogador (usa funções de desenho do graphics)"""
    player = Player(395, 240, graphics.draw_line, graphics.fill_rect, 
                    camera.get_camera, screen)
    
    """Cria o jogo (gerencia salas, colisão, tarefas)"""
    game = Game(screen, graphics, camera, player, menu_system, viewport)
    
    """Configuração inicial"""
    game.state = GAME_STATE_SPLASH
    splash_start_time = pygame.time.get_ticks()
    
    """Variáveis de estado local"""
    show_controls = False
    
    """Loop principal do jogo"""
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        game.update(dt)
        draw_background(screen, WIDTH, HEIGHT)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = False
        
        """Processamento de eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
            
            elif event.type == pygame.KEYDOWN:
                if game.state == GAME_STATE_SPLASH:
                    game.state = GAME_STATE_MENU
                elif game.state == GAME_STATE_CONGRATS:
                    game.state = GAME_STATE_MENU
                    game.reset_game()
                elif game.state == GAME_STATE_MENU:
                    if show_controls:
                        show_controls = False
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        menu_system.selected = (menu_system.selected - 1) % 3
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        menu_system.selected = (menu_system.selected + 1) % 3
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if menu_system.selected == 0:
                            game.state = GAME_STATE_PLAYING
                        elif menu_system.selected == 1:
                            show_controls = True
                        elif menu_system.selected == 2:
                            running = False
                
                    """ Jogando"""
                elif game.state == GAME_STATE_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        game.state = GAME_STATE_PAUSED
                        menu_system.selected = 0
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        camera.zoom_in()
                    elif event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE, pygame.K_KP_MINUS):
                        camera.zoom_out()
                    elif event.key in (pygame.K_0, pygame.K_KP0):
                        camera.reset_zoom()
                
                    """ Pausado"""
                elif game.state == GAME_STATE_PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        game.state = GAME_STATE_PLAYING
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        menu_system.selected = (menu_system.selected - 1) % 3
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        menu_system.selected = (menu_system.selected + 1) % 3
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if menu_system.selected == 0:
                            game.state = GAME_STATE_PLAYING
                        elif menu_system.selected == 1:
                            game.state = GAME_STATE_MENU
                            menu_system.selected = 0
                            game.reset_game()
                        elif menu_system.selected == 2:
                            running = False
        
        """Renderização e lógica por estado"""
        
        if game.state == GAME_STATE_SPLASH:
            menu_system.draw_splash_screen()
            if pygame.time.get_ticks() - splash_start_time > 3000:
                game.state = GAME_STATE_MENU

        elif game.state == GAME_STATE_MENU:
            if show_controls:
                menu_system.draw_controls_screen()
            else:
                """Interação com mouse no menu"""
                for i in range(3):
                    option_rect = menu_system.get_main_menu_option_rect(i)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        menu_system.selected = i
                        if mouse_clicked:
                            if i == 0:
                                game.state = GAME_STATE_PLAYING
                            elif i == 1:
                                show_controls = True
                            elif i == 2:
                                running = False
                
                menu_system.draw_main_menu(game.rotation_angle)

        
        elif game.state == GAME_STATE_PLAYING:
            """ Captura teclas"""
            keys = pygame.key.get_pressed()
            
            """ Atualiza o jogo"""
            game.update_playing(dt, keys)
            
            """ Processa clique do mouse"""
            if mouse_clicked:
                game.handle_mouse_click(mouse_x, mouse_y)
            
            """ Desenha o jogo"""
            game.draw_playing()
        
        
        elif game.state == GAME_STATE_PAUSED:
            """ Desenha jogo por baixo (congelado)"""
            game.draw_playing()
            
            """ Interação com mouse no menu de pausa"""
            for i in range(3):
                option_rect = menu_system.get_pause_menu_option_rect(i)
                if option_rect.collidepoint(mouse_x, mouse_y):
                    menu_system.selected = i
                    if mouse_clicked:
                        if i == 0:
                            game.state = GAME_STATE_PLAYING
                        elif i == 1:
                            game.state = GAME_STATE_MENU
                            menu_system.selected = 0
                            game.reset_game()
                        elif i == 2:
                            running = False
            
            menu_system.draw_pause_menu()
        
        elif game.state == GAME_STATE_CONGRATS:
            menu_system.draw_congrats_screen()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
