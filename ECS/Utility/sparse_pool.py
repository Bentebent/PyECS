import math
from typing import List, TypeVar, Type

T = TypeVar("T")

class SparsePool():
    _sparse: List[int] = None
    _dense: List[int] = None
    _values: List[T] = None
    
    _type: T = None
    _sparse_initial_size: int = 0
    _dense_initial_size: int = 0
    _sparse_grow_size: int = 0
    _dense_grow_size: int = 0
    
    _current_element_count: int = 0
    
    def __init__(self, type: Type[T], sparse_size: int, dense_size: int, sparse_grow_size: int, 
                 dense_grow_size: int) -> None:
        self._type = type
        self._sparse_initial_size = sparse_size
        self._dense_initial_size = dense_size
        self._sparse_grow_size = sparse_grow_size
        self._dense_grow_size = dense_grow_size
        
        self.reset()
        
    def reset(self) -> None:
        self._sparse: List[int] = [-1] * self._sparse_initial_size
        self._dense: List[int] = [-1] * self._dense_initial_size
        self._values: List[T] = [None] * self._dense_initial_size
        
    def create(self, index: int, *argv) ->  T:
        if index >= len(self._sparse):
            self._grow_sparse(index)
        if self._current_element_count >= len(self._dense):
            self._grow_dense()
        
        self._sparse[index] = self._current_element_count
        self._dense[self._current_element_count] = index
        self._values[self._current_element_count] = self._type(*argv)
        
        self._current_element_count += 1
        
        return self._values[self._sparse[index]]
    
    def remove(self, index: int) -> None:
        if self._sparse[index] == -1:
            return
        
        self._current_element_count -= 1
        
        dense_index = self._sparse[index]
        dense_back = self._dense[self._current_element_count]
        
        self._dense[dense_index] = dense_back
        self._values[dense_index] = self._values[self._current_element_count]
        self._sparse[dense_back] = dense_index
        
        self._dense.pop()
        self._values.pop()
        
    def get_value(self, index: int) -> T:
        return self._values[self._sparse[index]]
    
    def set_value(self, index: int, val: T) -> None:
        self._values[self._sparse[index]] = val
    
    def _grow_sparse(self, index: int) -> None:
        growth_multiple = 1 + math.ceil((index - len(self._sparse)) / self._sparse_grow_size)
        growth = growth_multiple * self._sparse_grow_size
        self._sparse.extend([-1] * growth)
        
    def _grow_dense(self) -> None:
        self._dense.extend([None] * self._dense_grow_size)
        self._values.extend([None] * self._dense_grow_size)
