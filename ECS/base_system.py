from abc import ABC, abstractmethod
from typing import List, Type
from sys import maxsize

from .system_types import Entity, Aspect

class BaseSystem(ABC):
    _inclusive_aspect: Aspect = 0
    _exclusive_aspect: Aspect = 0
    _entities: List[Entity] = []
    _world = None
    
    def __init__(self, world, included_components: List[Type], excluded_components: List[Type]):
        self._world = world
        
        if included_components:
            self._inclusive_aspect = self._world.generate_aspect(included_components)
            
        if excluded_components:
            self._exclusive_aspect = self._world.generate_aspect(excluded_components)
            
    def clear(self):
        self._entities.clear()
    
    def entity_changed(self, entity: Entity, old_aspect: Aspect, new_aspect: Aspect) -> None:
        if self._aspect_matches(old_aspect):
            self._entities.remove(entity)
        
        if self._aspect_matches(new_aspect):
            self._entities.append(entity)
    
    def _aspect_matches(self, aspect: Aspect) -> bool:
        return ((self._inclusive_aspect & aspect) == self._inclusive_aspect) and ((self._exclusive_aspect & aspect) == 0)

    @abstractmethod
    def run(self, delta_time: float):
        pass
    
   