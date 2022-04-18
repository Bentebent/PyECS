from dataclasses import dataclass
from abc import ABC

@dataclass
class AbstractDataclass(ABC):
    def __new__(cls, *args, **kwargs): 
        if cls == AbstractDataclass or cls.__bases__[0] == AbstractDataclass: 
            raise TypeError("Cannot instantiate abstract class.") 
        return super().__new__(cls)