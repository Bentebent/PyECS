from dataclasses import dataclass
from ECS.base_component import BaseComponent

@dataclass
class TestComponentA(BaseComponent):
    my_int: int = 0
    my_other_int: int = 0
    
@dataclass
class TestComponentB(BaseComponent):
    my_float: float = 0