import unittest
from typing import Type

from ECS.Utility.sparse_pool import SparsePool
from ECS.system_types import Entity

class TestSparsePool(unittest.TestCase):
    def _setup(self, value_type: Type, sparse_size=1024, dense_size=128, sparse_grow_size=1024
               , dense_grow_size=128) -> SparsePool:
        return SparsePool(value_type, sparse_size, dense_size, sparse_grow_size, dense_grow_size)
    
    def test_create(self):
        sparse_pool: SparsePool = self._setup(int)
        
        sparse_pool.create(512, 1337)
        
        self.assertEqual(len(sparse_pool._sparse), 1024)
        self.assertEqual(sparse_pool._sparse[512], 0)
        self.assertEqual(sparse_pool.get_value(512), 1337)
        
    def test_grow(self):
        sparse_pool: SparsePool = self._setup(int)
        
        self.assertEqual(len(sparse_pool._sparse), 1024)
        self.assertEqual(len(sparse_pool._dense), 128)
        self.assertEqual(len(sparse_pool._values), 128)
        
        sparse_pool.create(1024, 9001)
        
        self.assertEqual(len(sparse_pool._sparse), 2048)
        self.assertEqual(len(sparse_pool._dense), 128)
        self.assertEqual(len(sparse_pool._values), 128)
        
        for i in range(512):
            sparse_pool.create(i, i + 1)
            
        self.assertEqual(len(sparse_pool._sparse), 2048)
        self.assertEqual(len(sparse_pool._dense), 640)
        self.assertEqual(len(sparse_pool._values), 640)
        
        self.assertEqual(sparse_pool._sparse[1024], 0)
        self.assertEqual(sparse_pool.get_value(1024), 9001)
        
    def test_delete(self):
        sparse_pool: SparsePool = self._setup(int)
        
        self.assertEqual(len(sparse_pool._sparse), 1024)
        self.assertEqual(len(sparse_pool._dense), 128)
        self.assertEqual(len(sparse_pool._values), 128)
        
        sparse_pool.create(1023, 9001)
        
        self.assertEqual(len(sparse_pool._sparse), 1024)
        self.assertEqual(len(sparse_pool._dense), 128)
        self.assertEqual(len(sparse_pool._values), 128)
        
        sparse_pool.create(0, 1337)
        
        self.assertEqual(sparse_pool._sparse[1023], 0)
        self.assertEqual(sparse_pool._sparse[0], 1)
        
        sparse_pool.remove(1023)
        
        self.assertEqual(sparse_pool._sparse[0], 0)
        self.assertEqual(len(sparse_pool._sparse), 1024)
        self.assertEqual(len(sparse_pool._dense), 127)
        self.assertEqual(len(sparse_pool._values), 127)



        

        
        

