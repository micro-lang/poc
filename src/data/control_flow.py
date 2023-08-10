from enum import Enum


class ControlFlow(Enum):
    BLOCK_OPEN = 0,
    BLOCK_CLOSE = 1,
    BLOCK_STACK_CLOSE = 2,
