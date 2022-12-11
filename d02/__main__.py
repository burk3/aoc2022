from enum import IntEnum
from typing import cast, Literal, Self
from ._input import STRATS

class Res(IntEnum):
    loss = -1
    tie = 0
    win = 1

class T(IntEnum):
    R = 1
    P = 2
    S = 3

    def for_res_throw(self, res: Res) -> 'T':
        """
        """
        me = self - 1
        th = (me + res) % 3
        return T(th + 1)

R = T.R
P = T.P
S = T.S

OppThrow = Literal["A", "B", "C"]
MyRes = Literal["X", "Y", "Z"]

class Round(str):
    @staticmethod
    def _throw(x: MyRes | OppThrow) -> T:
        match x:
            case "A" | "X":
                return R
            case "B" | "Y":
                return P
            case "C" | "Z":
                return S
    
    @property
    def res(self) -> Res:
        match cast(MyRes, self[-1]):
            case "X":
                return Res.loss
            case "Y":
                return Res.tie
            case "Z":
                return Res.win
        raise RuntimeError("Nope")

    @property
    def me(self) -> T:
        return self._throw(cast(MyRes, self[-1]))

    @property
    def opp(self) -> T:
        match cast(OppThrow, self[0]):
            case "A":
                return R
            case "B":
                return P
            case "C":
                return S
        return self._throw(cast(OppThrow, self[0]))


    def score(self) -> int:
        match (self.me, self.opp):
            case (T.R, T.S) | (T.S, T.P) | (T.P, T.R):
                return 6 + self.me
            case (me, opp) if me == opp:
                return 3 + self.me
        return int(self.me)


    def new_score(self) -> int:
        my_throw = self.opp.for_res_throw(self.res)
        return my_throw + ((self.res + 1) * 3)

print(sum(Round(r).score() for r in STRATS))
print(sum(Round(r).new_score() for r in STRATS))