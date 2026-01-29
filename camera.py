from constants import WIDTH, HEIGHT, ZOOM

class Camera:
    """
    Classe Camera
    --------------
    Gerencia a posição da câmera no mundo e fornece métodos
    para transformação de coordenadas mundo -> tela.
    """
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.zoom = ZOOM
    
    def get_camera(self):
        """Retorna a posição atual da câmera e configurações."""
        return self.x, self.y, self.zoom, WIDTH, HEIGHT
    
    def update(self, target_x, target_y):
        """Atualiza a posição da câmera para seguir um alvo."""
        self.x = target_x
        self.y = target_y
    
    def world_to_screen(self, x, y):
        """Converte coordenadas do mundo para coordenadas da tela."""
        screen_x = int((x - self.x) * self.zoom + WIDTH / 2)
        screen_y = int((y - self.y) * self.zoom + HEIGHT / 2)
        return screen_x, screen_y
    
    def screen_to_world(self, screen_x, screen_y):
        """Converte coordenadas da tela para coordenadas do mundo."""
        world_x = (screen_x - WIDTH / 2) / self.zoom + self.x
        world_y = (screen_y - HEIGHT / 2) / self.zoom + self.y
        return world_x, world_y
    def zoom_in(self, factor=1.2):
        """
        Aumenta o zoom (aproxima a câmera). Equivale a DIMINUIR o tamanho da Janela no mundo.
        
        Parâmetros:
        - factor: Fator multiplicativo (1.2 = 20% de aumento)
        """
        self.zoom = min(self.zoom * factor, 5.0)  # Máximo 5x
    
    def zoom_out(self, factor=1.2):
        """
        Diminui o zoom (afasta a câmera).Equivale a AUMENTAR o tamanho da Janela no mundo.
        """
        self.zoom = max(self.zoom / factor, 0.5)  # Mínimo 0.5x
    
    def reset_zoom(self):
        """Reseta o zoom para o valor padrão (ZOOM constante)."""
        self.zoom = ZOOM
    
    def get_window_bounds(self):
        """
        Retorna os limites da Janela (Window) no mundo. """
        half_w = (WIDTH / 2) / self.zoom
        half_h = (HEIGHT / 2) / self.zoom
        
        return (
            self.x - half_w,  # wx_min
            self.y - half_h,  # wy_min
            self.x + half_w,  # wx_max
            self.y + half_h   # wy_max
        )