from enum import Enum
from pyglet import clock, app
from pyglet.window import Window, key

from snake import Snake
from fruit import Fruit
from canvas import Canvas
from world_map import WorldMap

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
WORLD_MAP_WIDTH = 20
WORLD_MAP_HEIGHT = 20
CELL_SIZE = 20
FRAME_RATE = 120


class Game():
    class State(Enum):
        INITIAL = 0
        PLAY = 1
        GAME_OVER = 2
        WIN = 3
        PAUSE = 4

    def __init__(self, levels, cur_level):
        self.window = Window(WINDOW_WIDTH, WINDOW_HEIGHT,
                             caption="Nibble Game")
        self.levels = levels
        self.cur_level = levels[cur_level]
        self.fruit_counter = 0
        self.state = Game.State.INITIAL
        self.world_map = WorldMap(WORLD_MAP_WIDTH, WORLD_MAP_HEIGHT)
        self.canvas = Canvas(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
        self.snake = self._create_snake()
        self.fruit = self._create_fruit()
        self.game_objects = [self.snake, self.fruit]
        self.window.set_handler('on_key_press', self._on_key_press)
        self.window.set_handler('on_draw', self._on_draw)
        clock.schedule_interval(self._on_update, 1 / FRAME_RATE)
        print('Press "Space" for start new game')

    def _start(self):
        print('Start game, level:', self.cur_level)
        self.snake.start(self.cur_level['speed'])
        self.state = Game.State.PLAY

    def _restart(self):
        self.fruit_counter = 0
        self.cur_level = self.levels[0]
        self.fruit.reset()
        self.snake.reset()
        self._start()

    def _on_draw(self):
        self.window.clear()
        self.canvas.clear()
        for x in self.game_objects:
            x.draw(self.canvas)

    def _on_update(self, dt):
        for x in self.game_objects:
            x.update(dt)

    def _on_key_press(self, symbol, mods):
        if self.state == Game.State.PLAY:
            for x in self.game_objects:
                x.on_key_press(symbol, mods)
        elif self.state == Game.State.INITIAL:
            if symbol == key.SPACE:
                self._start()
        elif self.state == Game.State.GAME_OVER:
            if symbol == key.SPACE:
                self._restart()

    def _create_snake(self):
        def on_die():
            self.state = Game.State.GAME_OVER
            print('You are dead (press "Space" for restart)')

        snake = Snake(self.world_map)
        snake.subscribe('die', on_die)
        return snake

    def _create_fruit(self):
        def on_eat():
            lvl = self.cur_level['number']
            goal = self.cur_level['goal']
            self.fruit_counter += 1
            print('Eats fruits:', '%s/%s' % (self.fruit_counter, goal))
            if self.fruit_counter >= goal and lvl < len(self.levels):
                self.fruit_counter = 0
                self.cur_level = self.levels[lvl + 1]
                self.snake.reset()
                self.snake.start(self.cur_level['speed'])
                self.fruit.reset()
                print('Level up:', self.cur_level)
            elif lvl >= len(self.levels):
                self.snake.stop()
                self.state = Game.State.WIN
                print('You win!')

        fruit = Fruit(self.world_map)
        fruit.subscribe('eat', on_eat)
        return fruit


levels = [
    {'number': 0, 'speed': 5, 'goal': 10},
    {'number': 1, 'speed': 7, 'goal': 12},
    {'number': 2, 'speed': 9, 'goal': 14},
    {'number': 3, 'speed': 11, 'goal': 16},
    {'number': 4, 'speed': 13, 'goal': 18},
    {'number': 5, 'speed': 15, 'goal': 20},
    {'number': 6, 'speed': 17, 'goal': 22},
    {'number': 7, 'speed': 19, 'goal': 24},
    {'number': 8, 'speed': 21, 'goal': 26},
    {'number': 9, 'speed': 23, 'goal': 28},
    {'number': 10, 'speed': 25, 'goal': 30}
]

if __name__ == '__main__':
    game = Game(levels, 0)
    app.run()
