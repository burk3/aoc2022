from __future__ import annotations

import math
from dataclasses import dataclass
from typing import NamedTuple

from ._input import EXAMPLE, EXAMPLE2, DATA


class St(NamedTuple):
    x: int
    y: int

    def __add__(self, other: St) -> St:  # type: ignore[override]
        return St(self.x + other.x, self.y + other.y)

    def __sub__(self, other: St) -> St:
        return St(self.x - other.x, self.y - other.y)


dirs: dict[str, St] = {
    "U": St(0, 1),
    "D": St(0, -1),
    "L": St(-1, 0),
    "R": St(1, 0),
}


def move_tail(h: St, t: St) -> St:
    match t - h:
        case St(2, 2):
            return St(h.x + 1, h.y + 1)
        case St(-2, 2):
            return St(h.x - 1, h.y + 1)
        case St(2, -2):
            return St(h.x + 1, h.y - 1)
        case St(-2, -2):
            return St(h.x - 1, h.y - 1)
        case St(2, _):
            return St(h.x + 1, h.y)
        case St(-2, _):
            return St(h.x - 1, h.y)
        case St(_, 2):
            return St(h.x, h.y + 1)
        case St(_, -2):
            return St(h.x, h.y - 1)
    return t


def p1(inp: list[str]) -> int:
    h, t = St(0, 0), St(0, 0)
    visited: set[St] = {t}
    for ins in inp:
        ds, ns = ins.split()
        d, n = dirs[ds], int(ns)
        for _ in range(n):
            h = h + d
            t = move_tail(h, t)
            visited.add(t)
    return len(visited)

def p2(inp: list[str]) -> int:
    h, *tails = (St(0,0) for _ in range(10))
    visited: set[St] = set()
    for ins in inp:
        ds, ns = ins.split()
        d, n = dirs[ds], int(ns)
        for _ in range(n):
            h = h + d
            tails[0] = move_tail(h, tails[0])
            for i in range(1, 9):
                tails[i] = move_tail(tails[i-1], tails[i])
            visited.add(tails[-1])
    return len(visited)

# print(p1(EXAMPLE))
# print(p1(DATA))
print(p2(EXAMPLE2))
print(p2(DATA))
