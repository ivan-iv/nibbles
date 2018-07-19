from pyglet import clock, app, window
from pyglet.window import Window
import pyglet

from snake import Snake
from fruit import Fruit
from canvas import Canvas
from world_map import WorldMap

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 670
HUD_HEIGHT = 50
WORLD_MAP_WIDTH = 20
WORLD_MAP_HEIGHT = 30
CELL_SIZE = 20
FRAME_RATE = 120

def game():
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Nibble Game")
    world_map = WorldMap(WORLD_MAP_WIDTH, WORLD_MAP_HEIGHT)
    canvas = Canvas(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, padding=HUD_HEIGHT)

    snake = Snake(world_map)
    fruit = Fruit(world_map)

    def on_die():
        print('DIE')

    def on_eat():
        print('EAT')

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

