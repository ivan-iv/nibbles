from pyglet import clock, app, window
from pyglet.window import Window
import pyglet

from snake import Snake
from fruit import Fruit
from canvas import Canvas
from world_map import WorldMap

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
HUD_HEIGHT = 0
WORLD_MAP_WIDTH = 20
WORLD_MAP_HEIGHT = 20
CELL_SIZE = 20
FRAME_RATE = 120

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

def game():
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Nibble Game")
    world_map = WorldMap(WORLD_MAP_WIDTH, WORLD_MAP_HEIGHT)
    canvas = Canvas(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, padding=HUD_HEIGHT)

    current_level = levels[0]
    fruit_counter = 0

    snake = Snake(current_level['speed'], world_map)
    fruit = Fruit(world_map)

    print('Start with level:', current_level)

    def on_die():
        nonlocal current_level, fruit_counter

        current_level = levels[0]
        fruit_counter = 0
        print('You are dead =(')

    def on_eat():
        nonlocal current_level, fruit_counter

        fruit_counter += 1
        n = current_level['number']
        print('Fruits:', '%s/%s' % (fruit_counter, current_level['goal']))

        if fruit_counter >= current_level['goal'] and n < len(levels):
            current_level = levels[n + 1]
            fruit_counter = 0
            snake.reborn(current_level['speed'])
            fruit.regrow()
            print('Next level:', current_level)

    snake.subscribe('die', on_die)
    fruit.subscribe('eat', on_eat)

    game_objects = [snake, fruit]

    def update(dt):
        for x in game_objects:
            x.update(dt)

    def draw():
        window.clear()
        canvas.clear()
        for x in game_objects:
            x.draw(canvas)

    def on_key_press(symbol, mods):
        for x in game_objects:
            x.on_key_press(symbol, mods)

    window.set_handler('on_key_press', on_key_press)
    window.set_handler('on_draw', draw)
    clock.schedule_interval(update, 1 / FRAME_RATE)

if __name__ == '__main__':
    game()
    app.run()

