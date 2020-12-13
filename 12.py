from dataclasses import dataclass


def parse(f):
    for line in f:
        assert line[0] in 'NSEWLRF'
        yield line[0], int(line[1:].rstrip())


@dataclass
class Coord:
    y: int
    x: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return self.__class__(self.y + other.y, self.x + other.x)

    def __mul__(self, other: int) -> 'Coord':
        return self.__class__(self.y * other, self.x * other)


def move(pos: Coord, dir: str, amt: int) -> Coord:
    '''Move from pos in a cardinal direction by the given amount.'''
    dpos = {
        'N': Coord(+1, 0),
        'S': Coord(-1, 0),
        'E': Coord(0, +1),
        'W': Coord(0, -1),
    }[dir]
    return pos + (dpos * amt)


def turn(dir: str, way: str, amt: int) -> str:
    '''Turn left/right from a given direction by the given amount.'''
    clockwise = [('N', 'E'), ('E', 'S'), ('S', 'W'), ('W', 'N')]
    turner = {
        'L': {b: a for a, b in clockwise},
        'R': {a: b for a, b in clockwise},
    }
    assert amt % 90 == 0 and amt >= 0
    for _ in range(amt // 90):
        dir = turner[way][dir]
    return dir


def rotate(vector: Coord, way: str, amt: int) -> Coord:
    '''Rotate vector left/right by the given amount.'''
    rotator = {
        'L': lambda vec: Coord(vec.x, -vec.y),
        'R': lambda vec: Coord(-vec.x, vec.y),
    }
    assert amt % 90 == 0 and amt >= 0
    for _ in range(amt // 90):
        vector = rotator[way](vector)
    return vector


def mhdist(pos: Coord) -> int:
    return abs(pos.y) + abs(pos.x)


with open('12.input') as f:
    instructions = list(parse(f))


# part 1
@dataclass
class Ship1:
    pos: Coord
    face: str

    def move(self, instr):
        dir, amt = instr
        if dir in 'NSEW':
            self.pos = move(self.pos, dir, amt)
        elif dir in 'LR':
            self.face = turn(self.face, dir, amt)
        elif dir == 'F':
            self.move((self.face, amt))
        else:
            raise NotImplementedError(instr)

    def accumulate(self, instructions):
        for instr in instructions:
            self.move(instr)


ship = Ship1(Coord(0, 0), 'E')
ship.accumulate(instructions)
print(mhdist(ship.pos))


# part 2
@dataclass
class Ship2(Ship1):
    waypoint: Coord

    def move(self, instr):
        dir, amt = instr
        if dir in 'NSEW':
            self.waypoint = move(self.waypoint, dir, amt)
        elif dir in 'LR':
            self.waypoint = rotate(self.waypoint, dir, amt)
        elif dir == 'F':
            self.pos += self.waypoint * amt
        else:
            raise NotImplementedError(instr)


ship = Ship2(Coord(0, 0), 'E', Coord(1, 10))
ship.accumulate(instructions)
print(mhdist(ship.pos))
