from functools import cached_property
from typing import NamedTuple

from ._input import EXAMPLE, DATA

class Range:
    start: int
    end: int

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    @classmethod
    def from_str(cls, s: str) -> 'Range':
        start, end = s.split("-", 2)
        return cls(int(start), int(end))

    def __contains__(self, other: "Range") -> bool:
        return other.start <= self.start and other.end >= self.end

class Assig(str):
    @cached_property
    def _ranges(self) -> tuple[Range, Range]:
        l, r = self.split(",", 2)
        return (Range.from_str(l), Range.from_str(r))
    
    def contains(self) -> bool:
        l, r = self._ranges
        return l in r or r in l
    
    def overlaps(self) -> bool:
        l, r = self._ranges
        if self.contains():
            return True
        return r.start <= l.start <= r.end or r.start <= l.end <= r.end

for line in EXAMPLE:
    print(line)
    ass = Assig(line)
    print(ass.contains())
    print(ass.overlaps())

print(sum(1 if Assig(ass).contains() else 0 for ass in EXAMPLE))
print(sum(1 if Assig(ass).contains() else 0 for ass in DATA))
print(sum(1 if Assig(ass).overlaps() else 0 for ass in EXAMPLE))
print(sum(1 if Assig(ass).overlaps() else 0 for ass in DATA))