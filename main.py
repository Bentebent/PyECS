from time import perf_counter, sleep
import pyglet

from ECS.world import World

from Components.test_components import TestComponentA, TestComponentB
from Systems.test_system import TestSystem

def initialze_window(width: int=1280, height: int=720, fullscreen=False, resizable=True, 
                     caption="3D Programming Test") -> pyglet.window:
    window = pyglet.window.Window(width=width, height=height, fullscreen=fullscreen, resizable=resizable, caption=caption)
    return window
    
    
def initialize_world() -> World:
    world: World = World([TestComponentA, TestComponentB], [TestSystem])
        
    world.add_entity()
    world.add_entity()
    world.add_entity()
    
    world.add_component(0, TestComponentA, 1, 1337)
    world.add_component(2, TestComponentA, 2, 1338)
    
    world.remove_entity(0)

    return world

def on_render(window: pyglet.window):
    window.clear()
    window.flip()
    
def main() -> None:
    window = initialze_window()
    world: World = initialize_world()
    
    min_frame_rate: float = 30.0
    max_frame_rate: float = 240.0
    
    max_frame_time: float = 1.0 / min_frame_rate
    min_frame_time: float = 1.0 / max_frame_rate
    
    delta_time: float = min_frame_time
    
    while(True):
        window.switch_to()
        window.dispatch_events()
        
        start_time = perf_counter()
        world.run(delta_time)
        end_time = perf_counter()
        
        delta_time = end_time - start_time
        
        on_render(window)
        
        if delta_time > max_frame_time:
            delta_time = max_frame_time
        elif delta_time < min_frame_time:
            while delta_time < min_frame_time:
                sleep(0)
                end_time = perf_counter()
                delta_time = end_time - start_time

if __name__ == '__main__':
    main()