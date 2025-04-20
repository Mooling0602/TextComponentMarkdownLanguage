from dataclasses import dataclass, field
from enum import Enum


class MissingValueOperation(Enum):
    exception = 0
    asNone = 1
    ignore = 2


@dataclass
class ParserOption:
    outputDebug: bool = field(default=False)
    missingValue: MissingValueOperation = field(default=MissingValueOperation.exception)
