from enum import Enum
from pyglet.window import key

from game_object import GameObject
from enums import Color, UnitType


class Dir(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


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

    def draw(self, canvas):
        canvas.draw(self.position, Color.RED.value)

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

