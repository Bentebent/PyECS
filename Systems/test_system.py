from time import sleep
from typing import Tuple

from ECS.base_system import BaseSystem
from ECS.world import World

from Components.test_components import TestComponentA

class TestSystem(BaseSystem):
    _inclusive_components = [TestComponentA]
    def __init__(self, world):
        super().__init__(world, self._inclusive_components, None)
        
    def run(self, delta_time: float):
        print("Running TestSystem")
        
        for entity in self._entities:
            components: Tuple(TestComponentA) = self._world.get_components(entity, self._inclusive_components)
            print(components[0])
            components[0].my_int += 1
        sleep(1)
        
        