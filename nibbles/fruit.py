import random

from game_object import GameObject
from enums import UnitType, Color


class Fruit(GameObject):
    unit_type = UnitType.FRUIT

    def __init__(self, world_map):
        super().__init__(world_map)

        x, y = self.get_default_position()
        self.grow_at(x, y)

        self.register_event('eat')

    def eat_me(self):
        x, y = self.position[0]
        self.world_map.clean_cell(x, y)

        while True:
            rand_x = random.randint(0, self.world_map.width - 1)
            rand_y = random.randint(0, self.world_map.height - 1)

            if not self.world_map.get_cell(rand_x, rand_y):
                self.grow_at(rand_x, rand_y)
                break

        self.dispatch_event('eat')

    def grow_at(self, x, y):
        self.position = [(x, y)]
        self.world_map.set_cell(x, y, self)
        self.color = random.choice([Color.GREEN, Color.YELLOW, Color.BLUE, Color.PURPLE])

    def get_default_position(self):
        return self.world_map.width // 2, self.world_map.height // 2 + self.world_map.height // 5

    def regrow(self):
        self.world_map.clean_cell(self.position[0][0], self.position[0][1])
        x, y = self.get_default_position()
        self.grow_at(x, y)

    def draw(self, canvas):
        canvas.draw(self.position, self.color.value)

