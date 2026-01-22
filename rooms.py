GRAY  = (160, 160, 160)
WHITE = (255, 255, 255)
BLUE  = (50, 50, 200)
GREEN = (50, 200, 50)


class Room:
    def __init__(self, x, y, w, h, door, button, draw_line, fill_rect):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.door = door      
        self.button = button  
        self.completed = False
        self.draw_line = draw_line
        self.fill_rect = fill_rect

        # Calcula em qual lado da sala a porta está
        dx, dy, dw, dh = self.door
        x0, y0, w0, h0 = self.x, self.y, self.w, self.h

        door_cx = dx + dw / 2
        door_cy = dy + dh / 2

        dist_top = abs(door_cy - y0)
        dist_bottom = abs(door_cy - (y0 + h0))
        dist_left = abs(door_cx - x0)
        dist_right = abs(door_cx - (x0 + w0))

        self.door_side = min(
            [
                (dist_top, "top"),
                (dist_bottom, "bottom"),
                (dist_left, "left"),
                (dist_right, "right"),
            ],
            key=lambda t: t[0],
        )[1]

    def draw(self):
        # Preenche o interior da sala
        self.fill_rect(self.x, self.y, self.w, self.h, GRAY)
        # Desenha as paredes com uma "brecha" (porta) na borda mais próxima do retângulo door
        dx, dy, dw, dh = self.door
        x, y, w, h = self.x, self.y, self.w, self.h
        side = self.door_side

        # TOP
        if side == "top":
            self.draw_line(x, y, dx, y, WHITE)
            self.draw_line(dx + dw, y, x + w, y, WHITE)
        else:
            self.draw_line(x, y, x + w, y, WHITE)

        # BOTTOM
        if side == "bottom":
            self.draw_line(x, y + h, dx, y + h, WHITE)
            self.draw_line(dx + dw, y + h, x + w, y + h, WHITE)
        else:
            self.draw_line(x, y + h, x + w, y + h, WHITE)

        # LEFT
        if side == "left":
            self.draw_line(x, y, x, dy, WHITE)
            self.draw_line(x, dy + dh, x, y + h, WHITE)
        else:
            self.draw_line(x, y, x, y + h, WHITE)

        # RIGHT
        if side == "right":
            self.draw_line(x + w, y, x + w, dy, WHITE)
            self.draw_line(x + w, dy + dh, x + w, y + h, WHITE)
        else:
            self.draw_line(x + w, y, x + w, y + h, WHITE)

        # Botão dentro da sala (pode ser um objeto)
        bx, by, bw, bh = self.button
        color = GREEN if self.completed else BLUE
        self.fill_rect(bx, by, bw, bh, color)
        # Borda do botão (retângulo) usando apenas draw_line
        self.draw_line(bx, by, bx + bw, by, WHITE)            # topo
        self.draw_line(bx, by, bx, by + bh, WHITE)            # esquerda
        self.draw_line(bx + bw, by, bx + bw, by + bh, WHITE)  # direita
        self.draw_line(bx, by + bh, bx + bw, by + bh, WHITE)  # base