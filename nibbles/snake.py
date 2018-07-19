from enum import Enum
from pyglet.window import key

from game_object import GameObject
from enums import Color, UnitType


class Dir(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

DEFAULT_SPEED = 5

class Snake(GameObject):
    unit_type = UnitType.SNAKE

    def __init__(self, world_map):
        super().__init__(world_map)

        self.dir = Dir.UP
        self.speed = DEFAULT_SPEED
        self.is_running = False
        self.is_dying = False

        self.position = self.get_default_position()
        self.resync_with_world_map(self.position)

        self.timestamp = 0
        self.register_event('die')

    def update(self, dt):
        if self.is_dying:
            return

        if self.timestamp >= 1 / self.speed:
            self.timestamp = 0
            self.crawl()
        else:
            self.timestamp += dt

    def draw(self, canvas):
        canvas.draw(self.position, Color.RED.value)

    def on_key_press(self, symbol, mods):
        if self.is_dying:
            return

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

    def reborn(self, speed=DEFAULT_SPEED):
        self.speed = speed
        self.dir = Dir.UP

        old_position = self.position
        self.position = self.get_default_position()
        self.resync_with_world_map(old_position)

    def get_default_position(self):
        start_x = self.world_map.width // 2
        start_y = self.world_map.height // 2

        return [
            (start_x, start_y),
            (start_x, start_y - 1),
            (start_x, start_y - 2)
        ]

    def resync_with_world_map(self, position, old_position=[]):
        if old_position:
            for x, y in old_position:
                self.world_map.clean_cell(x, y)

        for x, y in position:
            self.world_map.set_cell(x, y, self)

    def crawl(self):
        if not self.is_running:
            return

        x, y = self.calc_new_head_position()

        if x < 0 or x >= self.world_map.width or y < 0 or y >= self.world_map.height:
            self.die()
            return

        unit_at = self.world_map.get_cell(x, y)

        if unit_at and unit_at.unit_type == UnitType.SNAKE:
            self.die()
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

    def die(self):
        self.is_running = False
        self.is_dying = True
        self.dispatch_event('die')

