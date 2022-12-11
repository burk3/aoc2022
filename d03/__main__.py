from collections import Counter
from functools import cached_property
from typing import Iterable
from ._input import EXAMPLE, RUCKSACKS


class Sack(str):
    @cached_property
    def left(self) -> str:
        return self[:len(self)//2]
    
    @cached_property
    def right(self) -> str:
        return self[len(self)//2:]

    def common(self) -> str:
        acc = Counter(self.left).keys() & Counter(self.right).keys()
        assert len(acc) == 1
        return next(iter(acc))


def pri(c: str) -> int:
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    return ord(c) - ord('A') + 27


class Group(tuple[str, str, str]):
    def common(self) -> str:
        acc = set(Counter(self[0]).keys())
        for i in (1, 2):
            acc &= Counter(self[i]).keys()

        assert len(acc) == 1
        return next(iter(acc))

def gen_groups(sacks: list[str]) -> Iterable[Group]:
    it = iter(sacks)
    try:
        while True:
            yield Group((next(it), next(it), next(it)))
    except StopIteration:
        pass
    

print(sum(pri(Sack(sack).common()) for sack in EXAMPLE))
print(sum(pri(Sack(sack).common()) for sack in RUCKSACKS))

print(sum(pri(g.common()) for g in gen_groups(EXAMPLE)))
print(sum(pri(g.common()) for g in gen_groups(RUCKSACKS)))