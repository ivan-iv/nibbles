import random

from game_object import GameObject
from enums import UnitType, Color

fruit_colors = ([Color.GREEN, Color.YELLOW, Color.BLUE, Color.PURPLE])


class Fruit(GameObject):
    unit_type = UnitType.FRUIT

    def __init__(self, world_map):
        super().__init__(world_map)
        self._grow_at(self._get_default_position())
        self._register_event('eat')

    def eat_me(self):
        self._world_map.clean(self._position[0])

        while True:
            coord = (random.randint(0, self._world_map.width - 1),
                     random.randint(0, self._world_map.height - 1))

            if not self._world_map.get(coord):
                self._grow_at(coord)
                break

        self._dispatch_event('eat')

    def regrow(self):
        self._world_map.clean(self._position[0])
        self._grow_at(self._get_default_position())

    def draw(self, canvas):
        canvas.draw(self._position, self._color.value)

    def _grow_at(self, coord):
        self._position = [coord]
        self._world_map.set(coord, self)
        self._color = random.choice(fruit_colors)

    def _get_default_position(self):
        return (self._world_map.width // 2,
                self._world_map.height // 2 + self._world_map.height // 5)
