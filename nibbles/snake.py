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

    def __init__(self, speed, world_map):
        super().__init__(world_map)

        self._dir = Dir.UP
        self._speed = speed
        self._is_running = False
        self._is_dying = False
        self._is_input_block = False
        self._position = []
        self._set_default_position()
        self._timestamp = 0
        self._register_event('die')

    def update(self, dt):
        if self._is_dying:
            return

        if self._timestamp >= 1 / self._speed:
            self._timestamp = 0
            self._move()
            self._is_input_block = False
        else:
            self._timestamp += dt

    def draw(self, canvas):
        canvas.draw(self._position, Color.RED.value)

    def on_key_press(self, symbol, mods):
        if self._is_dying:
            return

        if symbol == key.SPACE:
            self._is_running = True
            return

        if self._is_input_block:
            return

        if symbol == key.UP and self._dir != Dir.DOWN:
            self._dir = Dir.UP
            self._is_input_block = True
        elif symbol == key.DOWN and self._dir != Dir.UP:
            self._dir = Dir.DOWN
            self._is_input_block = True
        elif symbol == key.LEFT and self._dir != Dir.RIGHT:
            self._dir = Dir.LEFT
            self._is_input_block = True
        elif symbol == key.RIGHT and self._dir != Dir.LEFT:
            self._dir = Dir.RIGHT
            self._is_input_block = True

    def reborn(self, speed):
        self._speed = speed
        self._dir = Dir.UP
        self._timestamp = 0
        self._set_default_position()

    def _set_default_position(self):
        self._world_map.clean_all(self._position)
        x = self._world_map.width // 2
        y = self._world_map.height // 2
        self._position = [(x, y), (x, y - 1)]
        self._world_map.set_all(self._position, self)

    def _move(self):
        if not self._is_running:
            return

        head = self._calc_new_head_position()

        is_out_width = head[0] < 0 or head[0] >= self._world_map.width
        is_out_height = head[1] < 0 or head[1] >= self._world_map.height

        if is_out_width or is_out_height:
            self._die()
            return

        unit_at = self._world_map.get(head)

        if unit_at and unit_at.unit_type == UnitType.SNAKE:
            self._die()
            return

        self._position.insert(0, head)
        self._world_map.set(head, self)

        if unit_at and unit_at.unit_type == UnitType.FRUIT:
            unit_at.eat_me()
        else:
            tail = self._position.pop()
            self._world_map.clean(tail)

    def _calc_new_head_position(self):
        x, y = self._position[0]

        if self._dir == Dir.UP:
            return x, y + 1
        elif self._dir == Dir.DOWN:
            return x, y - 1
        elif self._dir == Dir.LEFT:
            return x - 1, y
        elif self._dir == Dir.RIGHT:
            return x + 1, y

    def _die(self):
        self._is_running = False
        self._is_dying = True
        self._dispatch_event('die')
