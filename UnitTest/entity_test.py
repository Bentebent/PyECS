import unittest

from ECS.entity_container import EntityContainer
from ECS.system_types import Entity

class TestEntityContainer(unittest.TestCase):
    def _setup(self) -> EntityContainer:
        return EntityContainer()
    
    def test_add_entity(self):
        entity_container = self._setup()
        
        first: Entity = entity_container.create()
        second: Entity = entity_container.create()
        
        self.assertEqual(first, 0)
        self.assertEqual(second, 1)
        

