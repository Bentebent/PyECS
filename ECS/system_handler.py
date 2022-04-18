from typing import List, Type

from .system_types import Entity, Aspect
from .base_system import BaseSystem
from .entity_container import EntityContainer


class SystemHandler():
    _systems: List[BaseSystem] = []
    
    def __init__(self, world, systems: List[Type]) -> None:
        for system in systems:
            self._systems.append(system(world))
            
    def clear(self):
        for system in self._systems:
            system.clear()
        
    def entity_changed(self, entity: Entity, old_aspect: Aspect, new_aspect: Aspect) -> None:
        for system in self._systems:
            system.entity_changed(entity, old_aspect, new_aspect)
        
    def run(self, delta_time: float) -> None:
        for system in self._systems:
            system.run(delta_time)