from pyglet.event import EventDispatcher


class GameObject():
    def __init__(self, world_map):
        self._world_map = world_map
        self._event_dispatcher = EventDispatcher()

    def draw(self):
        pass

    def update(self, dt):
        pass

    def on_key_press(self, symbol, mods):
        pass

    def subscribe(self, event_type, handler):
        self._event_dispatcher.set_handler(event_type, handler)

    def unsubscribe(self, event_type, handler):
        self._event_dispatcher.remove_handler(event_type, handler)

    def _register_event(self, event_type):
        self._event_dispatcher.register_event_type(event_type)

    def _dispatch_event(self, event_type):
        self._event_dispatcher.dispatch_event(event_type)
