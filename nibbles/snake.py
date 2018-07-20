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
        self.speed = 1
        self.is_running = False
        self.is_dead = False
        self.is_input_block = False
        self.position = []
        self._set_default_position()
        self.timestamp = 0
        self._register_event('die')

    def update(self, dt):
        if self.is_dead:
            return

        if self.timestamp >= 1 / self.speed:
            self.timestamp = 0
            self._move()
            self.is_input_block = False
        else:
            self.timestamp += dt

    def draw(self, canvas):
        canvas.draw(self.position, Color.RED.value)

    def on_key_press(self, symbol, mods):
        if self.is_dead or self.is_input_block:
            return

        if symbol == key.UP and self.dir != Dir.DOWN:
            self.dir = Dir.UP
            self.is_input_block = True
        elif symbol == key.DOWN and self.dir != Dir.UP:
            self.dir = Dir.DOWN
            self.is_input_block = True
        elif symbol == key.LEFT and self.dir != Dir.RIGHT:
            self.dir = Dir.LEFT
            self.is_input_block = True
        elif symbol == key.RIGHT and self.dir != Dir.LEFT:
            self.dir = Dir.RIGHT
            self.is_input_block = True

    def reset(self):
        self.dir = Dir.UP
        self.timestamp = 0
        self.is_dead = False
        self._set_default_position()

    def start(self, speed):
        self.speed = speed
        self.is_running = True

    def _set_default_position(self):
        self.world_map.clean_all(self.position)
        x = self.world_map.width // 2
        y = self.world_map.height // 2
        self.position = [(x, y), (x, y - 1)]
        self.world_map.set_all(self.position, self)

    def _move(self):
        if not self.is_running:
            return

        head = self._calc_new_head_position()
        is_out_width = head[0] < 0 or head[0] >= self.world_map.width
        is_out_height = head[1] < 0 or head[1] >= self.world_map.height

        if is_out_width or is_out_height:
            self._die()
            return

        unit_at = self.world_map.get(head)

        if unit_at and unit_at.unit_type == UnitType.SNAKE:
            self._die()
            return
        self.position.insert(0, head)
        self.world_map.set(head, self)

        if unit_at and unit_at.unit_type == UnitType.FRUIT:
            unit_at.eat_me()
        else:
            tail = self.position.pop()
            self.world_map.clean(tail)

    def _calc_new_head_position(self):
        x, y = self.position[0]
        if self.dir == Dir.UP:
            return x, y + 1
        elif self.dir == Dir.DOWN:
            return x, y - 1
        elif self.dir == Dir.LEFT:
            return x - 1, y
        elif self.dir == Dir.RIGHT:
            return x + 1, y

    def _die(self):
        self.is_running = False
        self.is_dead = True
        self._dispatch_event('die')
