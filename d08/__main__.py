from ._input import EXAMPLE, DATA
from dataclasses import dataclass
from itertools import product
from types import EllipsisType as ElT
from typing import Sequence, overload, Iterable


@dataclass
class Forest:
    grid: tuple[tuple[int, ...], ...]

    @overload
    def __getitem__(self, idx: tuple[int, ElT] | tuple[ElT, int]) -> tuple[int, ...]:
        ...

    @overload
    def __getitem__(self, idx: tuple[int, int]) -> int:
        ...

    def __getitem__(self, idx: tuple[int | ElT, int | ElT]) -> int | tuple[int, ...]:
        match idx:
            case (ElT(), int(y)):
                return self.grid[y]
            case (int(x), ElT()):
                return tuple(row[x] for row in self.grid)
            case (int(x), int(y)):
                return self.grid[y][x]
        raise RuntimeError("sup")

    def visible(self, x: int, y: int) -> bool:
        w, h = (len(self.grid[0]), len(self.grid))
        if x in (0, w-1) or y in (0, h-1):
            return True
        target = self[x, y]
        col = self[x, ...]
        row = self[..., y]
        vectors = [
            col[:y],
            col[y + 1 :],
            row[:x],
            row[x + 1:],
        ]
        return any(all(n < target for n in vec) for vec in vectors)

    @staticmethod
    def _score_vec(val: int, vec: tuple[int,...]) -> int:
        for i, n in enumerate(vec):
            if n >= val:
                return i+1
        else:
            return len(vec)

    def viewscore(self, x: int, y: int) -> int:
        w, h = (len(self.grid[0]), len(self.grid))
        if x in (0, w-1) or y in (0, h-1):
            return 0
        target = self[x, y]
        col = self[x, ...]
        row = self[..., y]
        vectors = [
            col[y-1::-1],
            col[y+1:],
            row[x-1::-1],
            row[x+1:],
        ]
        acc = 1
        for vec in vectors:
            acc *= self._score_vec(target, vec)
        return acc


    def gen_all_coords(self) -> Iterable[tuple[int, int]]:
        h = len(self.grid)
        w = len(self.grid[0])
        yield from product(range(w), range(h))

    def gen_inner_coords(self) -> Iterable[tuple[int, int]]:
        h = len(self.grid)
        w = len(self.grid[0])
        yield from product(range(1, w - 1), range(1, h - 1))


ex = Forest(EXAMPLE)
for y in range(len(ex.grid)):
    for x in range(len(ex.grid[0])):
        print(1 if ex.visible(x, y) else 0, end='')
    print()
    
print(sum(1 for coord in ex.gen_all_coords() if ex.visible(*coord)))
print(max((ex.viewscore(*coord), coord) for coord in ex.gen_inner_coords()))

real = Forest(DATA)
print(sum(1 for coord in real.gen_all_coords() if real.visible(*coord)))
print(max(real.viewscore(*coord) for coord in real.gen_inner_coords()))
