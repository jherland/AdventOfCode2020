from dataclasses import dataclass
from enum import Enum
from typing import Dict, Union

CardDir = Enum('CardDir', 'N S E W')
TurnDir = Enum('TurnDir', 'L R')
MoveDir = Enum('MoveDir', 'F')
AnyDir = Union[CardDir, TurnDir, MoveDir]


@dataclass(frozen=True)
class Instruction:
    dir: AnyDir
    amt: int

    @classmethod
    def parse(cls, s: str) -> 'Instruction':
        Dirs: Dict[str, AnyDir] = {
            'N': CardDir.N,
            'S': CardDir.S,
            'E': CardDir.E,
            'W': CardDir.W,
            'L': TurnDir.L,
            'R': TurnDir.R,
            'F': MoveDir.F,
        }
        dir = Dirs[s[0]]
        amt = int(s[1:])
        if isinstance(dir, TurnDir):
            assert amt % 90 == 0
        assert amt > 0
        return cls(dir, amt)


def parse(f):
    for line in f:
        yield Instruction.parse(line.rstrip())


@dataclass
class Coord:
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return self.__class__(self.y + other.y, self.x + other.x)

    def __mul__(self, other: int) -> 'Coord':
        return self.__class__(self.y * other, self.x * other)


def move(pos: Coord, dir: CardDir, amt: int) -> Coord:
    '''Move from pos in a cardinal direction by the given amount.'''
    dpos = {
        CardDir.N: Coord(+1, 0),
        CardDir.S: Coord(-1, 0),
        CardDir.E: Coord(0, +1),
        CardDir.W: Coord(0, -1),
    }[dir]
    return pos + (dpos * amt)


def turn(dir: CardDir, way: TurnDir, amt: int) -> CardDir:
    '''Turn left/right from a given start direction by the given amount.'''
    circle = [
        (CardDir.N, CardDir.W),
        (CardDir.W, CardDir.S),
        (CardDir.S, CardDir.E),
        (CardDir.E, CardDir.N),
    ]
    next_dir = {
        TurnDir.L: {a: b for a, b in circle},
        TurnDir.R: {b: a for a, b, in circle},
    }
    assert amt % 90 == 0 and amt >= 0
    while amt > 0:
        dir = next_dir[way][dir]
        amt -= 90
    return dir


@dataclass
class Ship:
    pos: Coord = Coord(0, 0)  # current position
    facing: CardDir = CardDir.E  # facing direction

    def move(self, instr: Instruction) -> None:
        if isinstance(instr.dir, CardDir):
            self.pos = move(self.pos, instr.dir, instr.amt)
        elif isinstance(instr.dir, TurnDir):
            self.facing = turn(self.facing, instr.dir, instr.amt)
        elif isinstance(instr.dir, MoveDir):
            self.move(Instruction(self.facing, instr.amt))
        else:
            raise NotImplementedError(instr)

    def move_by(self, vector: Coord, scale: int) -> None:
        self.pos += vector * scale


@dataclass
class Waypoint:
    pos: Coord  # current position, relative to ship

    def move(self, instr: Instruction) -> None:
        if isinstance(instr.dir, CardDir):
            self.pos = move(self.pos, instr.dir, instr.amt)
        elif isinstance(instr.dir, TurnDir):
            rotate = {
                TurnDir.L: lambda pos: Coord(pos.x, -pos.y),
                TurnDir.R: lambda pos: Coord(-pos.x, pos.y),
            }
            amt = instr.amt
            assert amt % 90 == 0 and amt >= 0
            while amt > 0:
                self.pos = rotate[instr.dir](self.pos)
                amt -= 90
        else:
            raise NotImplementedError(instr)


def mhdist(pos: Coord) -> int:
    return abs(pos.y) + abs(pos.x)


with open('12.input') as f:
    instructions = list(parse(f))


# part 1
ship = Ship()
for instr in instructions:
    ship.move(instr)
print(mhdist(ship.pos))

# part 2
ship = Ship()
waypoint = Waypoint(Coord(1, 10))
for instr in instructions:
    if isinstance(instr.dir, (CardDir, TurnDir)):
        waypoint.move(instr)
    elif isinstance(instr.dir, MoveDir):
        ship.move_by(waypoint.pos, instr.amt)
print(mhdist(ship.pos))
