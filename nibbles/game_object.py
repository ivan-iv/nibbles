from pyglet.event import EventDispatcher


class GameObject():
    def __init__(self, world_map):
        self.world_map = world_map
        self.event_dispatcher = EventDispatcher()

    def draw(self):
        pass

    def update(self, dt):
        pass

    def on_key_press(self, symbol, mods):
        pass

    def register_event(self, event_type):
        self.event_dispatcher.register_event_type(event_type)

    def dispatch_event(self, event_type):
        self.event_dispatcher.dispatch_event(event_type)

    def subscribe(self, event_type, handler):
        self.event_dispatcher.set_handler(event_type, handler)

    def unsubscribe(self, event_type, handler):
        self.event_dispatcher.remove_handler(event_type, handler)

