from ctypes.wintypes import UINT
from typing import NewType
from ctypes import c_uint32

Entity = NewType("Entity", c_uint32)
Aspect = NewType("Aspect", c_uint32)
