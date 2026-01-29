import pygame
from constants import (
    WIDTH, HEIGHT, FPS, BLACK, WHITE, GREEN,
    GAME_STATE_MENU, GAME_STATE_PLAYING, GAME_STATE_PAUSED, GAME_STATE_CONGRATS,
    WALL_THICKNESS, MAX_TASKS
)
from rooms import Room


class Game:
    """
    Classe Game
    ------------
    Gerencia todo o estado e lógica do jogo.
    """
    
    def __init__(self, screen, graphics, camera, player, menu_system, viewport):
        """
        Inicializa o jogo.
        
        Parâmetros:
        - screen: Superfície do Pygame
        - graphics: Instância da classe Graphics
        - camera: Instância da classe Camera
        - player: Instância da classe Player
        - menu_system: Instância da classe MenuSystem
        - viewport: Instância da classe Viewport
        """
        self.screen = screen
        self.graphics = graphics
        self.camera = camera
        self.player = player
        self.menu_system = menu_system
        self.viewport = viewport
        
        """Fontes"""
        pygame.font.init()
        self.game_font = pygame.font.SysFont('Arial', 18, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 14)
        
        """Estado do jogo"""
        self.state = GAME_STATE_MENU
        self.show_controls = False
        self.rotation_angle = 0.0
        
        """Variáveis de tarefa"""
        self.task_active = False
        self.task_progress = 0.0
        self.active_room = None
        
        """Controle de teclas"""
        self.e_key_pressed = False
        
        """Cria as salas"""
        self.rooms = self._create_rooms()
        
        """Cria as paredes"""
        self.walls = self._create_walls()
        
        """Posições dos ventiladores"""
        self.fan_positions = [
            (room.x + room.w - 40, room.y + 30) for room in self.rooms
        ]
    
    def _create_rooms(self):
        """
        Cria as 5 salas do jogo
        ------------------------
        Salas 1-4: Salas de aula com mesas e cadeiras
        Sala 5: Sala de reunião com mesa circular
        
        Lousas posicionadas na FRENTE (parte superior) das salas
        para ficarem de frente para as mesas e cadeiras.
        """
        return [
            # Sala 1: Prog. Matemática 
            Room(20, 20, 400, 180, (180, 190, 50, 10), (70, 35, 100, 30),
                 self.graphics.draw_line, self.graphics.fill_rect, self.screen,
                 "Prog. Matemática", self.camera.get_camera,
                 self.graphics.fill_circle, is_meeting_room=False,
                 fill_rect_textured=self.graphics.fill_rect_textured),
            
            # Sala 2: Complexidade 
            Room(480, 20, 400, 180, (640, 190, 50, 10), (550, 35, 100, 30),
                 self.graphics.draw_line, self.graphics.fill_rect, self.screen,
                 "Complexidade", self.camera.get_camera,
                 self.graphics.fill_circle, is_meeting_room=False,
                 fill_rect_textured=self.graphics.fill_rect_textured),
            
            # Sala 3: Machine Learning
            Room(20, 300, 400, 180, (180, 300, 50, 10), (70, 315, 100, 30),
                 self.graphics.draw_line, self.graphics.fill_rect, self.screen,
                 "Machine Learning", self.camera.get_camera,
                 self.graphics.fill_circle, is_meeting_room=False,
                 fill_rect_textured=self.graphics.fill_rect_textured),
            
            # Sala 4: Algebra Linear  
            Room(480, 300, 400, 180, (580, 300, 50, 10), (490, 315, 100, 30),
                 self.graphics.draw_line, self.graphics.fill_rect, self.screen,
                    "Algebra Linear", self.camera.get_camera,
                    self.graphics.fill_circle, is_meeting_room=False,
                    fill_rect_textured=self.graphics.fill_rect_textured),
            
            # Sala 5: Reunião de Equipe no GESAD 
            Room(250, 520, 400, 150, (410, 520, 50, 10), (300, 530, 80, 25),
                 self.graphics.draw_line, self.graphics.fill_rect, self.screen,
                 "Reunião", self.camera.get_camera,
                 self.graphics.fill_circle, is_meeting_room=True,
                 fill_rect_textured=self.graphics.fill_rect_textured),
        ]
    
    def _create_walls(self):
        """Cria as paredes das salas"""
        walls = []
        
        for room in self.rooms:
            x, y, w, h = room.x, room.y, room.w, room.h
            dx, dy, dw, dh = room.door
            side = room.door_side
            
            """ Parede superior """
            if side == "top":
                door_start = dx
                door_end = dx + dw
                if door_start > x:
                    walls.append(pygame.Rect(x, y, door_start - x, WALL_THICKNESS))
                if door_end < x + w:
                    walls.append(pygame.Rect(door_end, y, (x + w) - door_end, WALL_THICKNESS))
            else:
                walls.append(pygame.Rect(x, y, w, WALL_THICKNESS))
            
            """ Parede inferior """
            if side == "bottom":
                door_start = dx
                door_end = dx + dw
                if door_start > x:
                    walls.append(pygame.Rect(x, y + h - WALL_THICKNESS, door_start - x, WALL_THICKNESS))
                if door_end < x + w:
                    walls.append(pygame.Rect(door_end, y + h - WALL_THICKNESS, (x + w) - door_end, WALL_THICKNESS))
            else:
                walls.append(pygame.Rect(x, y + h - WALL_THICKNESS, w, WALL_THICKNESS))
            
            """ Parede esquerda """
            if side == "left":
                door_start = dy
                door_end = dy + dh
                if door_start > y:
                    walls.append(pygame.Rect(x, y, WALL_THICKNESS, door_start - y))
                if door_end < y + h:
                    walls.append(pygame.Rect(x, door_end, WALL_THICKNESS, (y + h) - door_end))
            else:
                walls.append(pygame.Rect(x, y, WALL_THICKNESS, h))
            
            """ Parede direita """
            if side == "right":
                door_start = dy
                door_end = dy + dh
                if door_start > y:
                    walls.append(pygame.Rect(x + w - WALL_THICKNESS, y, WALL_THICKNESS, door_start - y))
                if door_end < y + h:
                    walls.append(pygame.Rect(x + w - WALL_THICKNESS, door_end, WALL_THICKNESS, (y + h) - door_end))
            else:
                walls.append(pygame.Rect(x + w - WALL_THICKNESS, y, WALL_THICKNESS, h))
        
        return walls
    
    def reset_game(self):
        """Reseta o jogo para o estado inicial"""
        self.player.x, self.player.y = 395, 240
        for room in self.rooms:
            room.completed = False
            room.door_open = False
            room.door_progress = 0.0
        self.task_active = False
        self.task_progress = 0.0
        self.active_room = None
    
    def update(self, dt):
        """
        Atualiza o estado do jogo e Atualiza ângulo de rotação para animações.

        Parâmetros:
        - dt: Delta time desde o último frame
        """
        import math
        self.rotation_angle += 3.0 * dt
        if self.rotation_angle > 2 * math.pi:
            self.rotation_angle -= 2 * math.pi
    
    def update_playing(self, dt, keys):
        """
        Atualiza o estado durante o gameplay
        -----------------------------------
        Atualiza a posição do jogador, câmera, interações e tarefas.
        Parâmetros:
        - dt: Delta time desde o último frame
        
        """
        """Atualiza animação das portas"""
        for room in self.rooms:
            room.update_door(dt)
        
        """Atualiza câmera"""
        target_x = self.player.x + self.player.w / 2
        target_y = self.player.y + self.player.h / 2
        self.camera.update(target_x, target_y)
        
        """Atualiza velocidade do jogador (sprint com Shift)"""
        self.player.update_speed(keys)
        
        """Movimento do jogador"""
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.player.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.player.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.player.speed
        
        """Colisão"""
        collision_rects = self.walls.copy()
        for room in self.rooms:
            if room.is_door_blocking():
                door_rect = room.get_door_collision_rect()
                collision_rects.append(pygame.Rect(*door_rect))
        
        if dx != 0:
            self.player.x += dx
            for wall in collision_rects:
                if self.player.rect().colliderect(wall):
                    if dx > 0:
                        self.player.x = wall.left - self.player.w
                    else:
                        self.player.x = wall.right
                    break
        
        if dy != 0:
            self.player.y += dy
            for wall in collision_rects:
                if self.player.rect().colliderect(wall):
                    if dy > 0:
                        self.player.y = wall.top - self.player.h
                    else:
                        self.player.y = wall.bottom
                    break
        
        """ Interação com portas (teclado)"""
        if keys[pygame.K_e]:
            if not self.e_key_pressed:
                self.e_key_pressed = True
                for room in self.rooms:
                    interaction_rect = room.get_door_interaction_rect()
                    if self._intersects(self.player.rect(), interaction_rect):
                        room.interact_door()
                        break
        else:
            self.e_key_pressed = False
        
        """ Interação com lousas (teclado)"""
        if not self.task_active:
            self.active_room = None
            for room in self.rooms:
                if self._intersects(self.player.rect(), room.button):
                    if keys[pygame.K_e] and not room.completed:
                        self.task_active = True
                        self.active_room = room
        
        """ Atualiza barra de progresso"""
        if self.task_active and self.active_room is not None:
            self.task_progress += 1.0 / FPS
            self.task_progress = min(self.task_progress, 1.0)
            
            if self.task_progress >= 1.0:
                self.task_progress = 0.0
                self.task_active = False
                self.active_room.completed = True
                
                # Check for victory
                completed_count = sum(1 for r in self.rooms if r.completed)
                if completed_count >= MAX_TASKS:
                    self.state = GAME_STATE_CONGRATS
    
    def handle_mouse_click(self, mouse_x, mouse_y):
        """
        Processa clique do mouse durante gameplay
        -----------------------------------
        Parâmetros:
        - mouse_x: Posição X do mouse na tela
        - mouse_y: Posição Y do mouse na tela
        
        """
        world_x, world_y = self.camera.screen_to_world(mouse_x, mouse_y)
        
        for room in self.rooms:
            """Click na porta"""
            pdx, pdy, pdw, pdh = room.get_door_interaction_rect()
            if pdx <= world_x <= pdx + pdw and pdy <= world_y <= pdy + pdh:
                room.interact_door()
                return
            
            """ Click na lousa """
            bx, by, bw, bh = room.button
            if bx <= world_x <= bx + bw and by <= world_y <= by + bh:
                if not room.completed and not self.task_active:
                    self.task_active = True
                    self.active_room = room
                return
    
    def draw_playing(self):
        """Desenha o estado de gameplay"""
        for room in self.rooms:
            room.draw()
        
        """ Desenha ventiladores animados"""
        for i, (fx, fy) in enumerate(self.fan_positions):
            speed_mult = 1.0 + i * 0.3
            self.graphics.draw_fan(fx, fy, 12, self.rotation_angle * speed_mult, WHITE, use_camera=True)
        
        """ Barra de progresso"""
        if self.task_active and self.active_room is not None:
            task_text = self.game_font.render("Task em progresso...", True, BLACK)
            text_rect = task_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
            self.screen.blit(task_text, text_rect)
            
            self.graphics.draw_progress_bar(WIDTH // 2 - 100, HEIGHT - 60, 200, self.task_progress)
        
        """Desenha jogador"""
        self.player.draw()
        
        """ Desenha viewport"""
        viewport_matrix = self.viewport.create_matrix(self.player, self.rooms, self.walls, self.fan_positions)
        self.viewport.draw(viewport_matrix, WIDTH - 280, 20, vp_scale=3)
        
        """ HUD: Barra de Tarefas (Among Us Style) """
        bar_x, bar_y = 10, 10
        bar_w, bar_h = 200, 20
        
        # Fundo da barra
        self.graphics.fill_rect(bar_x, bar_y, bar_w, bar_h, (50, 50, 50), use_camera=False)
        self.graphics.draw_rect(bar_x, bar_y, bar_w, bar_h, WHITE, use_camera=False)
        
        # Progresso
        completed_count = sum(1 for r in self.rooms if r.completed)
        progress_ratio = completed_count / MAX_TASKS
        fill_w = int(bar_w * progress_ratio)
        
        if fill_w > 0:
            self.graphics.fill_rect(bar_x, bar_y, fill_w, bar_h, GREEN, use_camera=False)
            
        # Segments
        segment_w = bar_w / MAX_TASKS
        for i in range(1, MAX_TASKS):
            sx = int(bar_x + i * segment_w)
            self.graphics.draw_line(sx, bar_y, sx, bar_y + bar_h, BLACK, use_camera=False)
            
        # Texto
        task_text = self.small_font.render(f"Tarefas: {completed_count}/{MAX_TASKS}", True, WHITE)
        self.screen.blit(task_text, (bar_x, bar_y + bar_h + 5))
        
        """ Instruções"""
        help_text = self.small_font.render("WASD: Mover | SHIFT: Correr | E: Interagir | ESC: Pausar | + Zoom in | - Zoom out" , True, BLACK)
        self.screen.blit(help_text, (10, HEIGHT - 25))
    
    def _intersects(self, r1, r2):
        """
        Verifica interseção entre retângulos
        ---------------------------
        Parâmetros:
        - r1: pygame.Rect do jogador
        - r2: tupla (x, y, w, h) do outro retângulo
        Retorna True se os retângulos se intersectam, False caso contrário. 
        """
        return r1.colliderect(pygame.Rect(*r2))
