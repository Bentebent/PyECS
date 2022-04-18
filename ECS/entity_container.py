from typing import List, Any
from bisect import insort

from .Utility.sparse_pool import SparsePool
from .system_types import Entity, Aspect

class EntityContainer():
    _entities: SparsePool = None
    _available_entities: List[Entity] = None
    _next_entity_id: Entity = 0
    
    def __init__(self) -> None:
        self._entities = SparsePool(Aspect, 10240, 10240, 1024, 1024)
        self._available_entities = []
        
    def clear(self) -> None:
        self._next_entity_id = 0
        self._entities.reset()
        self._available_entities.clear()
    
    def create(self) -> Entity:
        entity_id: Entity = -1
        
        if len(self._available_entities) > 0:
            entity_id = self._available_entities.pop(0)
        else:
            entity_id: Entity = self._next_entity_id
            self._next_entity_id += 1
            
        self._entities.create(entity_id, 0)
        return entity_id
    
    def delete(self, entity: Entity) -> None:
        self._entities.remove(entity)
        insort(self._available_entities, entity)
        
    def get_bitmask(self, entity: Entity) -> Aspect:
        return self._entities.get_value(entity)
    
    def update_bitmask(self, entity: Entity, bitmask: Aspect) -> None:
        self._entities.set_value(entity, bitmask)