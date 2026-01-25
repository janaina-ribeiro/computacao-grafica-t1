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
