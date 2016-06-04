from enum import Enum

class BagType(Enum):
    IV = 'introduce vertex'
    IE = 'introduce edge'
    J  = 'join'
    F  = 'forget'
    L  = 'leaf'
    R  = 'root'