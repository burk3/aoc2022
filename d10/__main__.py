from __future__ import annotations

import abc

from typing import ClassVar, NamedTuple, TypeAlias, Iterator, TypeVar
from itertools import islice
from collections.abc import Generator
from dataclasses import dataclass

from ._input import EXAMPLE, DATA


class RegFile(NamedTuple):
    x: int

NoneGen: TypeAlias = Generator[RegFile, None, RegFile]

class Instr(abc.ABC):
    _instrs: ClassVar[dict[str, type[Instr]]] = {}
    def __init_subclass__(cls,/, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._instrs[cls.__name__] = cls

    @classmethod
    def parse(cls, asm: str) -> Instr:
        assert len(asm) > 0
        instr, *args = asm.split()
        return cls._instrs[instr](*args)

    @abc.abstractmethod
    def exec(self, reg: RegFile) -> NoneGen:
        ...

class addx(Instr):
    n: int
    def __init__(self, n: str) -> None:
        self.n = int(n)

    def exec(self, reg: RegFile) -> NoneGen:
        yield reg
        yield reg
        return reg._replace(x=reg.x + self.n)


class noop(Instr):
    def exec(self, reg: RegFile) -> NoneGen:
        yield reg
        return reg


class Vm:
    reg: RegFile
    program: list[Instr]

    def __init__(self, asm: list[str]) -> None:
        self.reg = RegFile(x=1)
        self.program = [Instr.parse(x) for x in asm]

    def run(self) -> Iterator[RegFile]:
        self.reg = RegFile(x=1)
        for instr in self.program:
            it = instr.exec(self.reg)
            while True:
                try:
                    yield next(it)
                except StopIteration as e:
                    self.reg = e.value
                    break

T = TypeVar("T")
def enum_plus_1(it: Iterator[T]) -> Iterator[tuple[int, T]]:
    yield from ((i+1, x) for i, x in enumerate(it))


def p1(vm: Vm) -> int:
    states = vm.run()
    acc = 0
    for cyc, reg in islice(enum_plus_1(states), 19, None, 40):
        acc += cyc * reg.x
    return acc

def pixel_lit(cyc: int, x: int) -> bool:
    return 0 <= cyc - x <= 2

def p2(vm: Vm) -> None:
    states = vm.run()
    for cyc, reg in enumerate(states):
        hpos = cyc % 40
        if hpos == 0:
            print()
        print('#' if pixel_lit(hpos + 1, reg.x) else '.', end='')
    print()

ex = Vm(EXAMPLE)
da = Vm(DATA)
print(p1(ex))
print(p1(da))
p2(ex)
p2(da)



