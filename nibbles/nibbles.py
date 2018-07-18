from enum import Enum
import random
import pyglet
from pyglet.graphics import Batch
from pyglet.window import key


class UnitType(Enum):
    SNAKE = 1
    FRUIT = 2


class Dir(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Color(Enum):
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 255, 255)
    PURPLE = (255, 0, 255)


class WorldMap():
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = [[None for i in range(self.height)] for i in range(self.width)]

    def set_cell(self, x, y, unit):
        self.cells[x][y] = unit

    def get_cell(self, x, y):
        return self.cells[x][y]

    def clean_cell(self, x, y):
        self.cells[x][y] = None

    def __str__(self):
        result = ''

        for y in range(self.height):
            for x in range(self.width):
                unit = self.cells[x][y]
                if unit:
                    symbol = unit.unit_type.value
                else:
                    symbol = 0
                result += '%s ' % symbol
            result += '\n'

        return result


def render(coords, color, cell_size):
    all_points = []
    all_colors = []

    for x, y in coords:
        # x1,y1  x2,y2
        # x4,y4  x3,y3
        x1 = x4 = x * cell_size
        x2 = x3 = x * cell_size + cell_size
        y1 = y2 = y * cell_size
        y3 = y4 = y * cell_size + cell_size
        all_points.extend((x1, y1, x2, y2, x3, y3, x4, y4))
        all_colors.extend(color * 4)

    vertex_list = pyglet.graphics.vertex_list(4 * len(coords),
                                              ('v2i', all_points),
                                              ('c3B', all_colors))
    vertex_list.draw(pyglet.gl.GL_QUADS)


class GameObject():
    def __init__(self, world_map):
        self.world_map = world_map

    def draw(self):
        pass

    def update(self, dt):
        pass

    def on_key_press(self, symbol, mods):
        pass


class Snake(GameObject):
    unit_type = UnitType.SNAKE

    def __init__(self, world_map):
        super().__init__(world_map)

        self.dir = Dir.UP
        self.is_running = False
        self.speed = 5

        start_x = self.world_map.width // 2
        start_y = self.world_map.height // 2
        self.position = [
            (start_x, start_y),
            (start_x, start_y - 1),
            (start_x, start_y - 2)
        ]

        for x, y in self.position:
            self.world_map.set_cell(x, y, self)

        self.timestamp = 0

    def update(self, dt):
        if self.timestamp >= 1 / self.speed:
            self.timestamp = 0
            self.crawl()
        else:
            self.timestamp += dt

    def draw(self):
        render(self.position, Color.RED.value, self.world_map.cell_size)

    def on_key_press(self, symbol, mods):
        if symbol == key.SPACE:
            self.is_running = True

        if symbol == key.UP and self.dir != Dir.DOWN:
            self.dir = Dir.UP
        elif symbol == key.DOWN and self.dir != Dir.UP:
            self.dir = Dir.DOWN
        elif symbol == key.LEFT and self.dir != Dir.RIGHT:
            self.dir = Dir.LEFT
        elif symbol == key.RIGHT and self.dir != Dir.LEFT:
            self.dir = Dir.RIGHT

    def crawl(self):
        if not self.is_running:
            return

        x, y = self.calc_new_head_position()

        if x < 0 or x >= self.world_map.width or y < 0 or y >= self.world_map.height:
            self.is_running = False
            return

        unit_at = self.world_map.get_cell(x, y)

        if unit_at and unit_at.unit_type == UnitType.SNAKE:
            self.is_running = False
            return

        if unit_at and unit_at.unit_type == UnitType.FRUIT:
            unit_at.eat_me()
        else:
            tail = self.position.pop()
            self.world_map.clean_cell(tail[0], tail[1])

        self.position.insert(0, (x, y))
        self.world_map.set_cell(x, y, self)

    def calc_new_head_position(self):
        x, y = self.position[0]

        if self.dir == Dir.UP:
            return x, y + 1
        elif self.dir == Dir.DOWN:
            return x, y - 1
        elif self.dir == Dir.LEFT:
            return x - 1, y
        elif self.dir == Dir.RIGHT:
            return x + 1, y



class Fruit(GameObject):
    unit_type = UnitType.FRUIT

    def __init__(self, world_map):
        super().__init__(world_map)

        self.color = Color.GREEN

        start_x = self.world_map.width // 2
        start_y = self.world_map.height // 2 + self.world_map.height // 5
        self.grow_at(start_x, start_y)

    def eat_me(self):
        x, y = self.position[0]
        self.world_map.clean_cell(x, y)

        while True:
            rand_x = random.randint(0, self.world_map.width - 1)
            rand_y = random.randint(0, self.world_map.height - 1)
            if not self.world_map.get_cell(rand_x, rand_y):
                self.grow_at(rand_x, rand_y)
                break

    def grow_at(self, x, y):
        self.position = [(x, y)]
        self.world_map.set_cell(x, y, self)
        self.color = random.choice([Color.GREEN, Color.YELLOW, Color.BLUE, Color.PURPLE])

    def draw(self):
        render(self.position, self.color.value, self.world_map.cell_size)

window = pyglet.window.Window(400, 600, caption="Nibble Game")

world_map = WorldMap(20, 30, 20)

snake = Snake(world_map)
fruit = Fruit(world_map)

game_objects = [snake, fruit]

def update(dt):
    for x in game_objects:
        x.update(dt)

def draw():
    window.clear()
    for x in game_objects:
        x.draw()

def on_key_press(symbol, mods):
    for x in game_objects:
        x.on_key_press(symbol, mods)

window.set_handler('on_key_press', snake.on_key_press)
window.set_handler('on_draw', draw)
pyglet.clock.schedule_interval(update, 1/120)

if __name__ == '__main__':
    pyglet.app.run()

