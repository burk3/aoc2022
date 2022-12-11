from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from itertools import islice
from pathlib import Path
from typing import cast, NamedTuple, Generator, Iterable, TypeAlias, TypeVar, Literal as Lit

from parsec import *

from ._input import EXAMPLE, DATA

class Item(NamedTuple):
    name: str
    size: int
    parent: "Dir"

    def walk(self, cwd: Path) -> Iterable[tuple[Path, Item]]:
        yield (cwd / self.name, self)

@dataclass
class Dir:
    name: str
    items: "list[Item | Dir]"
    parent: "Dir | None"

    @cached_property
    def size(self) -> int:
        return sum(x.size for x in self.items)
    
    def walk(self, cwd: Path) -> Iterable[tuple[Path, Item | Dir]]:
        cwd = cwd / self.name
        yield (cwd, self)
        for ent in self.items:
            yield from ent.walk(cwd)

            

nl = string("\n")

name = regex(r"[a-zA-Z0-9_.-]+")
dir_str = string("/") | string("..") | name

T = TypeVar("T")
PGenT: TypeAlias = Generator[Parser, None, T]
DirLn: TypeAlias = tuple[Lit["dir"], str]
FileLn: TypeAlias = tuple[int, str]
CdComm: TypeAlias = tuple[Lit["cd"], str]
LsComm: TypeAlias = tuple[Lit["ls"], list[DirLn | FileLn]]
@generate
def ls_out_dir() -> PGenT[DirLn]:
    n = yield string("dir") >> space() >> name
    return ("dir", cast(str, n))

@generate
def ls_out_file() -> PGenT[FileLn]:
    sz = yield regex(r"\d+")
    n = yield space() >> name
    return (int(cast(str, sz)), cast(str, n))

@generate
def cd_command() -> PGenT[CdComm]:
    s = yield string("cd") >> space() >> dir_str << nl
    return ("cd", cast(str, s))

@generate
def ls_command() -> PGenT[LsComm]:
    yield string("ls") << nl
    output = yield sepEndBy1(ls_out_dir | ls_out_file, nl)
    return ("ls", cast(list[DirLn | FileLn], output))

@generate
def command() -> PGenT[LsComm | CdComm]:
    cmd = yield string("$ ") >> (ls_command | cd_command)
    return cast(LsComm | CdComm, cmd)



class ShellParser:
    _fs: Dir

    def __init__(self, s: str) -> None:
        self._fs = Dir("", [], None)
        self._parse_shell(s, self._fs)

    @property
    def fs(self) -> Dir:
        return self._fs
    
    @staticmethod
    def _parse_shell(s: str, fs: Dir) -> None:
        cwd: Dir = fs

        def pwd() -> str:
            parts: list[str] = []
            ent = cwd
            while ent.parent is not None:
                parts.append(ent.name)
                ent = ent.parent
            return "/" + "/".join(reversed(parts))

        for cmd in many(command).parse(s):
            match cmd:
                case ("cd", "/"):
                    cwd = fs
                case ("cd", ".."):
                    assert cwd.parent is not None
                    cwd = cwd.parent
                case ("cd", str(d)):
                    for ent in cwd.items:
                        if ent.name == d:
                            assert type(ent) is Dir
                            cwd = ent
                            break
                    else:
                        raise RuntimeError(f"no dir {d} in {pwd()} exists")
                case ("ls", outs):
                    for out in outs:
                        match out:
                            case ("dir", str(n)):
                                cwd.items.append(Dir(n, [], cwd))
                            case (int(sz), str(n)):
                                cwd.items.append(Item(n, sz, cwd))
    
    def walk(self) -> Iterable[tuple[Path, Dir | Item]]:
        yield from self._fs.walk(Path("/"))


ex = ShellParser(EXAMPLE)

print(sum(ent.size for _p, ent in ex.walk() if type(ent) is Dir and ent.size <= 100_000))


real = ShellParser(DATA)

print(sum(ent.size for _p, ent in real.walk() if type(ent) is Dir and ent.size <= 100_000))

FS_SIZE = 70_000_000
REQ_FREE = 30_000_000
CURRENT_FREE = FS_SIZE - real.fs.size

print(sorted(ent.size for _p, ent in real.walk() if type(ent) is Dir and CURRENT_FREE + ent.size >= REQ_FREE)[0])