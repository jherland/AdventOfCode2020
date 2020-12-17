from dataclasses import dataclass
from itertools import product
from typing import Tuple


@dataclass(frozen=True)
class NCoord:
    dim: Tuple[int, ...]

    def __str__(self):
        return f'<{",".join(map(str, self.dim))}>'

    def add_dimension(self, *args):
        return self.__class__(tuple(list(self.dim) + list(args)))

    def neighbors(self):
        def each_variation():
            for i in range(len(self.dim)):
                yield (self.dim[i] - 1, self.dim[i], self.dim[i] + 1)

        for coord in product(*[(val - 1, val, val + 1) for val in self.dim]):
            if coord != self.dim:
                yield self.__class__(coord)


def parse(f):
    legend = {'.': False, '#': True}
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            yield NCoord((x, y)), legend[c]


def count_active_neighbors(state, pos):
    return sum(coord in state for coord in pos.neighbors())


def step(state):
    candidates = set(state)
    for pos in state:
        candidates.update(pos.neighbors())
    for pos in candidates:
        if pos in state and count_active_neighbors(state, pos) in {2, 3}:
            yield pos
        elif pos not in state and count_active_neighbors(state, pos) == 3:
            yield pos


def run(state, cycles):
    for _ in range(cycles):
        state = set(step(state))
    return state


with open('17.input') as f:
    inital2d = {coord for coord, on in parse(f) if on}

# part 1
print(len(run({coord.add_dimension(0) for coord in inital2d}, 6)))

# part 2
print(len(run({coord.add_dimension(0, 0) for coord in inital2d}, 6)))
