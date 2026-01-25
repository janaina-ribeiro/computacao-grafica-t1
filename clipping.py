
"""Códigos de região para Cohen-Sutherland"""
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8


def compute_outcode(x, y, xmin, ymin, xmax, ymax):
    """
    Calcula o código de região para um ponto.
    
    Parâmetros:
    - x, y: Coordenadas do ponto
    - xmin, ymin, xmax, ymax: Limites da região de clipping
    
    Retorna:
    - Código de região (combinação de INSIDE, LEFT, RIGHT, TOP, BOTTOM)
    """
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= TOP
    elif y > ymax:
        code |= BOTTOM
    return code


def cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    """
    Algoritmo de Cohen-Sutherland para clipping de linhas.
    
    Parâmetros:
    - x0, y0, x1, y1: Coordenadas dos endpoints da linha
    - xmin, ymin, xmax, ymax: Limites da região de clipping
    
    Retorna:
    - None se a linha está completamente fora
    - Tupla (x0, y0, x1, y1) com as coordenadas clippadas
    """
    outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
    outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    
    while True:
        """
            Enquanto True, o loop continua até que a linha seja 
            aceita ou rejeitada. Se ambos os pontos estiverem dentro da região
            (outcode0 | outcode1 == 0), a linha é aceita. Se ambos os pontos
            estiverem fora da região (outcode0 & outcode1 != 0), a linha é rejeitada.
            Caso contrário, calcula o ponto de interseção com a borda da região
            e atualiza o endpoint correspondente.
        """
        if not (outcode0 | outcode1):
            return (x0, y0, x1, y1)
        elif outcode0 & outcode1:
            return None
        else:
            outcode_out = outcode0 if outcode0 else outcode1
            
            if outcode_out & TOP:
                x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0) if y1 != y0 else x0
                y = ymin
            elif outcode_out & BOTTOM:
                x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0) if y1 != y0 else x0
                y = ymax
            elif outcode_out & RIGHT:
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0) if x1 != x0 else y0
                x = xmax
            elif outcode_out & LEFT:
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0) if x1 != x0 else y0
                x = xmin
            
            if outcode_out == outcode0:
                x0, y0 = x, y
                outcode0 = compute_outcode(x0, y0, xmin, ymin, xmax, ymax)
            else:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    
    return None
