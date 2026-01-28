import math
from constants import WIDTH, HEIGHT, GRAY
from clipping import cohen_sutherland_clip


class Graphics:
    """
    Classe Graphics
    ----------------
    Gerencia todas as operações de desenho usando set_pixel como base.
    Recebe a referência da tela (screen) e da câmera.
    """
    
    def __init__(self, screen, camera):
        """
        Inicializa o sistema gráfico.
        
        Parâmetros:
        - screen: Superfície do Pygame para desenhar
        - camera: Instância da classe Camera
        """
        self.screen = screen
        self.camera = camera
    
    def set_pixel(self, x, y, color, use_camera=True):
        """
        Função set_pixel com câmera - FUNÇÃO BASE
        ------------------------------------------
        TODOS os desenhos usam esta função como base.
        Define um pixel na tela considerando a posição da câmera e o zoom.
        """
        if use_camera:
            screen_x, screen_y = self.camera.world_to_screen(x, y)
        else:
            screen_x, screen_y = int(x), int(y)
        
        if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
            self.screen.set_at((screen_x, screen_y), color)
    
    def draw_line(self, x0, y0, x1, y1, color, use_camera=True):
        """
        Função draw_line (Bresenham) com câmera e clipping
        ---------------------------------------------------
        Aplica o algoritmo de Bresenham usando apenas set_pixel.
        """
        if use_camera:
            sx0, sy0 = self.camera.world_to_screen(x0, y0)
            sx1, sy1 = self.camera.world_to_screen(x1, y1)
        else:
            sx0, sy0, sx1, sy1 = int(x0), int(y0), int(x1), int(y1)
        
        # Aplica clipping Cohen-Sutherland
        clipped = cohen_sutherland_clip(sx0, sy0, sx1, sy1, 0, 0, WIDTH - 1, HEIGHT - 1)
        if clipped is None:
            return
        
        sx0, sy0, sx1, sy1 = int(clipped[0]), int(clipped[1]), int(clipped[2]), int(clipped[3])
        
        dx = abs(sx1 - sx0)
        dy = abs(sy1 - sy0)
        stepx = 1 if sx0 < sx1 else -1
        stepy = 1 if sy0 < sy1 else -1
        err = dx - dy

        while True:
            self.screen.set_at((sx0, sy0), color)
            if sx0 == sx1 and sy0 == sy1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                sx0 += stepx
            if e2 < dx:
                err += dx
                sy0 += stepy
    
    def draw_circle(self, cx, cy, radius, color, use_camera=True):
        """
        Desenha um círculo usando o Algoritmo de Bresenham (Midpoint Circle)
        Usa apenas set_pixel para desenhar.
        """
        if use_camera:
            scx, scy = self.camera.world_to_screen(cx, cy)
            sr = int(radius * self.camera.zoom)
        else:
            scx, scy, sr = int(cx), int(cy), int(radius)
        
        x = 0
        y = sr
        d = 3 - 2 * sr
        
        def draw_circle_points(cx, cy, x, y):
            points = [
                (cx + x, cy + y), (cx - x, cy + y),
                (cx + x, cy - y), (cx - x, cy - y),
                (cx + y, cy + x), (cx - y, cy + x),
                (cx + y, cy - x), (cx - y, cy - x)
            ]
            for px, py in points:
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    self.screen.set_at((px, py), color)
        
        while x <= y:
            draw_circle_points(scx, scy, x, y)
            if d < 0:
                d = d + 4 * x + 6
            else:
                d = d + 4 * (x - y) + 10
                y -= 1
            x += 1
    
    def flood_fill(self, x, y, fill_color, boundary_color=None):
        """
        Algoritmo Flood Fill (preenchimento por inundação)
        ---------------------------------------------------
        Preenche uma região a partir de um ponto semente (x, y).
        Usa versão iterativa com pilha para evitar stack overflow.
        
        Parâmetros:
        - x, y: Ponto semente (início do preenchimento)
        - fill_color: Cor para preencher a região
        - boundary_color: Se None, preenche pixels da mesma cor do ponto inicial.
                          Se especificada, para quando encontra essa cor (boundary fill).
        
        Nota: Este algoritmo é usado apenas no MENU.
              No JOGO, usa-se Scanline para preenchimento.
        """
        x, y = int(x), int(y)
        
        # Verifica se o ponto inicial está dentro da tela
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
            return
        
        # Obtém a cor original do ponto semente
        original_color = self.screen.get_at((x, y))[:3]  # Ignora alpha
        
        # Se a cor original já é a cor de preenchimento, não faz nada
        if original_color == fill_color[:3] if len(fill_color) >= 3 else fill_color:
            return
        
        # Pilha para processamento iterativo (evita recursão profunda)
        stack = [(x, y)]
        visited = set()
        
        while stack:
            cx, cy = stack.pop()
            
            # Verifica limites e se já foi visitado
            if not (0 <= cx < WIDTH and 0 <= cy < HEIGHT):
                continue
            if (cx, cy) in visited:
                continue
            
            # Obtém a cor atual do pixel
            current_color = self.screen.get_at((cx, cy))[:3]
            
            # Verifica condição de preenchimento
            if boundary_color is not None:
                # Boundary Fill: para quando encontra a cor de borda
                if current_color == boundary_color[:3] if len(boundary_color) >= 3 else boundary_color:
                    continue
                if current_color == fill_color[:3] if len(fill_color) >= 3 else fill_color:
                    continue
            else:
                # Flood Fill tradicional: só preenche se for a cor original
                if current_color != original_color:
                    continue
            
            # Marca como visitado e preenche
            visited.add((cx, cy))
            self.screen.set_at((cx, cy), fill_color)
            
            # Adiciona vizinhos (4-conectividade)
            stack.append((cx + 1, cy))
            stack.append((cx - 1, cy))
            stack.append((cx, cy + 1))
            stack.append((cx, cy - 1))
    
    def flood_fill_rect(self, x, y, w, h, fill_color, border_color):
        """
        Desenha um retângulo com borda e preenche o interior usando Flood Fill.
        Demonstra o uso do Flood Fill para preenchimento de regiões delimitadas.
        
        Parâmetros:
        - x, y, w, h: Posição e dimensões do retângulo
        - fill_color: Cor de preenchimento interno
        - border_color: Cor da borda
        """
        # Primeiro desenha a borda do retângulo
        self.draw_line(x, y, x + w, y, border_color, use_camera=False)
        self.draw_line(x, y, x, y + h, border_color, use_camera=False)
        self.draw_line(x + w, y, x + w, y + h, border_color, use_camera=False)
        self.draw_line(x, y + h, x + w, y + h, border_color, use_camera=False)
        
        # Depois usa Flood Fill a partir do centro para preencher o interior
        center_x = x + w // 2
        center_y = y + h // 2
        self.flood_fill(center_x, center_y, fill_color, boundary_color=border_color)
    
    def fill_circle(self, cx, cy, radius, color, use_camera=True):
        """
        Preenche um círculo usando scanlines e set_pixel.
        """
        if use_camera:
            scx, scy = self.camera.world_to_screen(cx, cy)
            sr = int(radius * self.camera.zoom)
        else:
            scx, scy, sr = int(cx), int(cy), int(radius)
        
        for y in range(-sr, sr + 1):
            half_width = int(math.sqrt(max(0, sr * sr - y * y)))
            for x in range(-half_width, half_width + 1):
                px, py = scx + x, scy + y
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    self.screen.set_at((px, py), color)
    
    def draw_rect(self, x, y, w, h, color, use_camera=True):
        """Desenha um retângulo usando draw_line (que usa set_pixel)"""
        self.draw_line(x, y, x + w, y, color, use_camera)
        self.draw_line(x, y, x, y + h, color, use_camera)
        self.draw_line(x + w, y, x + w, y + h, color, use_camera)
        self.draw_line(x, y + h, x + w, y + h, color, use_camera)
    
    def fill_rect(self, x, y, w, h, color, use_camera=True):
        """
        Preenche um retângulo usando apenas set_pixel (scanline)
        """
        if use_camera:
            sx, sy = self.camera.world_to_screen(x, y)
            sw = int(w * self.camera.zoom)
            sh = int(h * self.camera.zoom)
        else:
            sx, sy, sw, sh = int(x), int(y), int(w), int(h)
        
        # Clipping
        start_x = max(0, sx)
        end_x = min(WIDTH, sx + sw)
        start_y = max(0, sy)
        end_y = min(HEIGHT, sy + sh)
        
        for py in range(start_y, end_y):
            for px in range(start_x, end_x):
                self.screen.set_at((px, py), color)
    
    def fill_rect_textured(self, x, y, w, h, texture_type="brick", use_camera=True):
        """
        Preenche um retângulo com textura procedural.
        Texturas: "brick", "checker", "stripes", "dots"
        """
        if use_camera:
            sx, sy = self.camera.world_to_screen(x, y)
            sw = int(w * self.camera.zoom)
            sh = int(h * self.camera.zoom)
        else:
            sx, sy, sw, sh = int(x), int(y), int(w), int(h)
        
        start_x = max(0, sx)
        end_x = min(WIDTH, sx + sw)
        start_y = max(0, sy)
        end_y = min(HEIGHT, sy + sh)
        
        for py in range(start_y, end_y):
            for px in range(start_x, end_x):
                lx = px - sx
                ly = py - sy
                
                if texture_type == "brick":
                    brick_w, brick_h = 16, 8
                    mortar = 1
                    row = ly // brick_h
                    offset = (brick_w // 2) if row % 2 else 0
                    bx = (lx + offset) % brick_w
                    by = ly % brick_h
                    if bx < mortar or by < mortar:
                        color = (100, 100, 100)
                    else:
                        color = (160, 80, 60)
                        
                elif texture_type == "checker":
                    tile_size = 8
                    if ((lx // tile_size) + (ly // tile_size)) % 2 == 0:
                        color = (200, 200, 200)
                    else:
                        color = (100, 100, 100)
                        
                elif texture_type == "stripes":
                    stripe_w = 6
                    if (ly // stripe_w) % 2 == 0:
                        color = (180, 180, 100)
                    else:
                        color = (140, 140, 80)
                        
                elif texture_type == "dots":
                    dot_spacing = 8
                    dx = lx % dot_spacing
                    dy = ly % dot_spacing
                    if dx < 2 and dy < 2:
                        color = (255, 255, 200)
                    else:
                        color = (100, 80, 60)
                else:
                    color = GRAY
                
                self.screen.set_at((px, py), color)
    
    def draw_fan(self, cx, cy, radius, angle, color, use_camera=True):
        """
        Desenha um ventilador (hélice) com 4 pás rotacionando.
        Demonstra animação + rotação + primitivas.
        """
        num_blades = 4
        
        for i in range(num_blades):
            blade_angle = angle + (i * math.pi / 2)
            end_x = cx + radius * math.cos(blade_angle)
            end_y = cy + radius * math.sin(blade_angle)
            
            for offset in [-1, 0, 1]:
                ox = offset * math.cos(blade_angle + math.pi/2)
                oy = offset * math.sin(blade_angle + math.pi/2)
                self.draw_line(cx + ox, cy + oy, end_x + ox, end_y + oy, color, use_camera)
        
        self.draw_circle(cx, cy, 3, (255, 255, 255), use_camera)
    
    def draw_progress_bar(self, x, y, w, progress):
        """
        Barra de Progresso usando set_pixel
        """
        self.draw_rect(x, y, w, 10, (255, 255, 255), use_camera=False)
        fill = int(w * progress)
        if fill > 0:
            self.fill_rect(x, y, fill, 10, (50, 200, 50), use_camera=False)

    def apply_shadow(self, color, factor):
        shadow_strength = 0.4
        f = 1.0 - factor * shadow_strength
        return (
            int(color[0] * f),
            int(color[1] * f),
            int(color[2] * f),
        )
