from itertools import tee
from typing import Iterable

from ._input import DATA, EXAMPLES, EXAMPLES2

def window(iterator: str, n: int) -> Iterable[tuple[str,...]]:
    its = tee(iterator, n)
    for i, it in enumerate(its):
        for _ in range(i):
            next(it, None)
    
    return zip(*its)

N = 4

for ex, expected in EXAMPLES.items():
    print(f"{ex} should be {expected}")
    for i, w in enumerate(window(ex, N)):
        if len(set(w)) == N:
            print(f"got {i+N}")
            assert i+N == expected
            break

for i, w in enumerate(window(DATA, N)):
    if len(set(w)) == N:
        print(f"found packet marker for DATA at {i+N}")
        break

N = 14
for ex, expected in EXAMPLES2.items():
    print(f"{ex} should be {expected}")
    for i, w in enumerate(window(ex, N)):
        if len(set(w)) == N:
            print(f"got {i+N}")
            assert i+N == expected
            break

for i, w in enumerate(window(DATA, N)):
    if len(set(w)) == N:
        print(f"found message marker for DATA at {i+N}")
        break