from ._input import CALORIE_DATA


class Elf(list[int]):
    @property
    def total(self) -> int:
        return sum(self)


elves: list[Elf] = [Elf(map(int, data.strip().split("\n"))) for data in CALORIE_DATA]
elves.sort(key=lambda x: x.total)

print(elves[-1].total)
print(sum(e.total for e in elves[-3:]))