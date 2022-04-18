from sys import maxsize
from typing import List, Type, Any, TypeVar, Tuple

from .entity_container import EntityContainer
from .component_container import ComponentContainer
from .system_handler import SystemHandler

from .system_types import Entity, Aspect

System = TypeVar("System")

class World:
    _entity_container: EntityContainer = None
    _component_container: ComponentContainer = None
    _system_handler: SystemHandler = None
    
    _component_bitmasks = {}
    _removed_entities = []
    
    def __init__(self, component_types: List[Type], systems: List[System]):
        component_count: int = 0
        for component_type in component_types:
            self._component_bitmasks[component_type] = 1 << component_count            
            component_count += 1
        
        self._entity_container = EntityContainer()
        self._component_container = ComponentContainer(component_types)
        self._system_handler = SystemHandler(self, systems)
        
       
    @property
    def entity_handler(self) -> EntityContainer:
        return self._entity_container
    
    @property
    def component_container(self) -> ComponentContainer:
        return self._component_container
    
    def clear(self) -> None:
        self._entity_container.clear()
        self._component_container.clear()
        self._system_handler.clear()
        
        
    def run(self, delta_time: float) -> None:
        self._delete_entities()
        self._system_handler.run(delta_time)
    
    def generate_aspect(self, component_types: List[Type]) -> Aspect:
        bitmask = 0
        for component in component_types:
            bitmask |= self._component_bitmasks[component]
            
        return bitmask
    
    def get_components(self, entity: Entity, component_types: List[Type]) -> Tuple:
        return self._component_container.get_components(entity, component_types)
    
    def add_entity(self) -> Entity:
        entity: Entity = self._entity_container.create()
        
        self._entity_changed(entity, 0, 0)
        
        return entity
    
    def add_component(self, entity: Entity, component_type: Type, *argv) -> Any:
        component = self._component_container.add(entity, component_type, *argv)
        
        old_aspect = self._entity_container.get_bitmask(entity)
        new_aspect = old_aspect | self._component_bitmasks[component_type]
        
        self._entity_container.update_bitmask(entity, new_aspect)
        self._entity_changed(entity, old_aspect, new_aspect)
        
        return component
    
    def remove_component(self, entity: Entity, component_type: Type) -> None:
        self._component_container.remove(entity, component_type)
        
        old_aspect = self._entity_container.get_bitmask(entity)
        new_aspect = old_aspect ^ self._component_bitmasks[component_type]
        
        self._entity_container.update_bitmask(entity, new_aspect)
        self._entity_changed(entity, old_aspect, new_aspect)
    
    def remove_entity(self, entity: Entity) -> None:
        self._removed_entities.append(entity)
        
        old_aspect = self._entity_container.get_bitmask(entity)
        new_aspect = 0
        
        self._entity_changed(entity, old_aspect, new_aspect)
    
    def _entity_changed(self, entity: Entity, old_aspect: Aspect, new_aspect: Aspect) -> None:
        self._system_handler.entity_changed(entity, old_aspect, new_aspect)
        
    def _delete_entities(self) -> None:
        for entity in self._removed_entities:
            self._entity_container.delete(entity)
            self._component_container.remove_all(entity)
            
        self._removed_entities.clear()

    
    