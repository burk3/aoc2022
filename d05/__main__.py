from typing import NamedTuple

from ._input import EXAMPLE, DATA

class Move(NamedTuple):
    num: int
    a: int
    b: int

class Stacks:
    _stacks: list[list[str]]
    def __init__(self, num_stacks: int) -> None:
        self._stacks = [[] for _ in range(num_stacks)]
    
    def do_move(self, move: Move) -> None:
        for _ in range(move.num):
            self[move.b].append(self[move.a].pop())
    
    def do_move2(self, move: Move) -> None:
        acc = [self[move.a].pop() for _ in range(move.num)]
        self[move.b].extend(reversed(acc))
    
    def tops(self) -> str:
        return "".join(stack[-1] for stack in self._stacks)


    def __getitem__(self, idx: int | tuple[int]) -> list[str]:
        match idx:
            case int(i):
                return self._stacks[i-1]
            case (i,):
                return self._stacks[i]
        raise RuntimeError()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._stacks!r}"


def parse(inp: list[str]) -> tuple[Stacks, list[Move]]:
    moves: list[Move] = []

    # first find the start of the moves/end of stack index
    div = next(i for i, l in enumerate(inp) if l == "")

    # find number of stacks
    num_stacks = max(map(int, inp[div-1].split()))

    # populate stacks
    stacks = Stacks(num_stacks)

    for line in inp[div-2::-1]:
        for i, c in enumerate(line[1::4]):
            if c != ' ':
                stacks[i,].append(c)

    # parse moves
    for move in inp[div+1:]:
        moves.append(Move(*map(int, move.split()[1::2])))
    
    return (stacks, moves)
    

stacks, moves = parse(EXAMPLE)

for move in moves:
    stacks.do_move2(move)
    print(stacks)

stacks, moves = parse(DATA)
for move in moves:
    stacks.do_move2(move)

print(stacks.tops())