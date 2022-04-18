from typing import List, Type, TypeVar, Dict, Any

from .Utility.sparse_pool import SparsePool
from .system_types import Entity

class ComponentContainer():
    _components: Dict[Type, SparsePool] = None
    
    def __init__(self, component_types: List[Type]) -> None:
        self._components = {}
        
        for component_type in component_types:
            self._components[component_type] = SparsePool(component_type, 5120, 1024, 1024, 128)
            
    def clear(self):
        for component_type in self._components:
            self._components[component_type].reset()
            
    def get_components(self, entity: Entity, component_types: List[Type]) -> Dict:
        result = []
        
        for component_type in component_types:
            result.append(self._components[component_type].get_value(entity))
        
        return tuple(result)
                    
    def add(self, entity: Entity, component_type: Type, *argv) -> Any:
        return self._components[component_type].create(entity, *argv)
    
    def remove(self, entity: Entity, component_type: Type) -> None:
        self._components[component_type].remove(entity)
        
    def remove_all(self, entity: Entity) -> None:
        for component_type in self._components:
            self._components[component_type].remove(entity)