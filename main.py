from time import perf_counter, sleep

from ECS.world import World

from Components.test_components import TestComponentA, TestComponentB
from Systems.test_system import TestSystem

def test(*argv):
    return TestComponentA(*argv)
    
def initialize_world() -> World:
    world: World = World([TestComponentA, TestComponentB], [TestSystem])
        
    world.add_entity()
    world.add_entity()
    world.add_entity()
    
    world.add_component(0, TestComponentA, 1, 1337)
    world.add_component(2, TestComponentA, 2, 1338)
    
    world.remove_entity(0)

    return world
    
def main() -> None:
    world: World = initialize_world()
    
    min_frame_rate: float = 30.0
    max_frame_rate: float = 240.0
    
    max_frame_time: float = 1.0 / min_frame_rate
    min_frame_time: float = 1.0 / max_frame_rate
    
    delta_time: float = min_frame_time
    
    while(True):
        start_time = perf_counter()
        world.run(delta_time)
        end_time = perf_counter()
        
        delta_time = end_time - start_time
        
        if delta_time > max_frame_time:
            delta_time = max_frame_time
        elif delta_time < min_frame_time:
            while delta_time < min_frame_time:
                sleep(0)
                end_time = perf_counter()
                delta_time = end_time - start_time

if __name__ == '__main__':
    main()