
import math


def rotate_point(x, y, cx, cy, angle):
    """
    Rotaciona um ponto (x, y) em torno de (cx, cy) por um ângulo em radianos.
    
    Parâmetros:
    - x, y: Coordenadas do ponto a ser rotacionado
    - cx, cy: Centro de rotação
    - angle: Ângulo em radianos
    
    Retorna:
    - Tupla (rx, ry) com as coordenadas rotacionadas
    """
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    tx = x - cx
    ty = y - cy
    rx = tx * cos_a - ty * sin_a
    ry = tx * sin_a + ty * cos_a
    return rx + cx, ry + cy


def scale_point(x, y, cx, cy, sx, sy):
    """
    Escala um ponto (x, y) em relação a (cx, cy) pelos fatores (sx, sy).
    
    Parâmetros:
    - x, y: Coordenadas do ponto a ser escalado
    - cx, cy: Centro de escala
    - sx, sy: Fatores de escala em X e Y
    
    Retorna:
    - Tupla com as coordenadas escaladas
    """
    tx = x - cx
    ty = y - cy
    return tx * sx + cx, ty * sy + cy


def translate_point(x, y, dx, dy):
    """
    Translação de um ponto.
    
    Parâmetros:
    - x, y: Coordenadas do ponto
    - dx, dy: Deslocamento em X e Y
    
    Retorna:
    - Tupla com as coordenadas transladadas
    """
    return x + dx, y + dy
