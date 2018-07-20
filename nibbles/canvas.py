from pyglet import graphics, gl


class Canvas():
    bg_color = 255, 155, 35

    def __init__(self, width, height, cell_size, padding=0):
        self.width = width
        self.height = height
        self.padding = padding
        self.cell_size = cell_size

    def clear(self):
        x1 = x4 = 0
        x2 = x3 = self.width
        y1 = y2 = self.height
        y3 = y4 = self.padding
        coords = (x1, y1, x2, y2, x3, y3, x4, y4)
        vertices = graphics.vertex_list(4, ('v2i', coords),
                                        ('c3B', Canvas.bg_color * 4))
        vertices.draw(gl.GL_QUADS)

    def draw(self, coords, color):
        all_points = []
        all_colors = []
        for x, y in coords:
            # x1,y1  x2,y2
            # x4,y4  x3,y3
            x1 = x4 = x * self.cell_size
            x2 = x3 = x * self.cell_size + self.cell_size
            y1 = y2 = y * self.cell_size + self.padding
            y3 = y4 = y * self.cell_size + self.cell_size + self.padding
            all_points.extend((x1, y1, x2, y2, x3, y3, x4, y4))
            all_colors.extend(color * 4)
        vertices = graphics.vertex_list(4 * len(coords),
                                        ('v2i', all_points),
                                        ('c3B', all_colors))
        vertices.draw(gl.GL_QUADS)
