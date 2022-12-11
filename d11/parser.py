from enum import IntEnum
from typing import Literal as Lit, Callable, NamedTuple, Iterator
import operator
import re

from parsec import *


class Throw(NamedTuple):
    item: int
    dest: int

class Op(IntEnum):
    ADD = 0
    MUL = 1

OP_LUT: list[Callable[[int, int], int]] = [
    operator.add,
    operator.mul,
]

class Monkey(NamedTuple):
    idx: int
    starting: list[int]
    op_type: Op
    op_val: int
    op_old_fac: Lit[0, 1]
    test: int
    iftrue: int
    iffalse: int
    items: list[int]

    @classmethod
    def new(
            cls,
            idx: int,
            starting: list[int],
            op_type: Op,
            op_val: int | None,
            test: int,
            iftrue: int,
            iffalse: int,
    ):
        op_val_new, op_old_fac = (0, 1) if op_val is None else (op_val, 0)
        return cls(
            idx,
            starting,
            op_type,
            op_val_new,
            op_old_fac,
            test,
            iftrue,
            iffalse,
            [],
        )

    def reset(self) -> None:
        self.items.clear()
        self.items.extend(self.starting)

    def inspect(self, old: int) -> int:
        val: int
        val = self.op_val + (self.op_old_fac * old)
        return OP_LUT[self.op_type](old, val)

    @staticmethod
    def relief(old: int) -> int:
        return old // 3

    def throw(self, item: int) -> int:
        if item % self.test == 0:
            return self.iftrue
        else:
            return self.iffalse

    def catch(self, item: int) -> None:
        self.items.append(item)

    def take_turn(self, relief=True) -> Iterator[Throw]:
        for item in self.items:
            item = self.inspect(item)
            if relief:
                item = self.relief(item)
            yield Throw(item, self.throw(item))
        self.items.clear()


ws = regex(r"\s+", re.MULTILINE)
num = regex(r"\d+")
starting_prefix = string("Starting items: ")
op_prefix = string("Operation: new = old ")
op_type_p = string("+") | string("*")
test_prefix = string("Test: divisible by ")
iftrue_prefix = string("If true: throw to monkey ")
iffalse_prefix = string("If false: throw to monkey ")


@generate
def monkey():
    idx = yield string("Monkey ") >> num << string(":") << ws
    starting = yield starting_prefix >> sepBy(num, string(", ")) << ws
    op_type = yield op_prefix >> op_type_p << space()
    op_val = yield (num | string("old")) << ws
    test = yield test_prefix >> num << ws
    iftrue = yield iftrue_prefix >> num << ws
    iffalse = yield iffalse_prefix >> num

    return Monkey.new(
        int(idx),
        [int(x) for x in starting],
        Op.ADD if op_type == "+" else Op.MUL,
        None if op_val == "old" else int(op_val),
        int(test),
        int(iftrue),
        int(iffalse),
    )


def parse_monkeys(inp: str) -> list[Monkey]:
    return list(sepBy(monkey, ws).parse(inp))
