from collections import Counter, defaultdict
import re
from typing import Dict, Iterable, Tuple

# Hex grid:
#  NW | NE
#  \./'\./
# W | 0 | E
#  /'\./'\
#  SW | SE

step_pattern = re.compile(r'(e|se|sw|w|nw|ne)')


def parse(f):
    for line in f:
        yield [m.group(1) for m in step_pattern.finditer(line.rstrip())]


def find_coord(steps: Iterable[str]) -> Tuple[int, int]:
    '''Turn a sequence of steps into a pair of (E, SE) coordinates.'''
    counts = Counter(steps)
    # Cancel W against E, NW against SE, NE against SW
    e = counts.get('e', 0) - counts.get('w', 0)
    se = counts.get('se', 0) - counts.get('nw', 0)
    sw = counts.get('sw', 0) - counts.get('ne', 0)
    # 1 SW == 1 SE - 1 E
    return e - sw, se + sw


def adjacent(coord):
    '''Return coordinates immediately E/SE/SW/W/NW/NE to the given.'''
    e, se = coord
    return {
        (e + 1, se + 0),  # E
        (e + 0, se + 1),  # SE
        (e - 1, se + 1),  # SW
        (e - 1, se + 0),  # W
        (e + 0, se - 1),  # NW
        (e + 1, se - 1),  # NE
    }


def nextday(tiles):
    ret = defaultdict(lambda: False)
    black_tiles = {t for t, black in tiles.items() if black}
    candidates = set(black_tiles)
    for b in black_tiles:
        candidates |= adjacent(b)
    for c in candidates:
        black_neighbors = sum(tiles[nb] for nb in adjacent(c))
        if tiles[c] and black_neighbors in {1, 2}:  # remain black
            ret[c] = True
        elif not tiles[c] and black_neighbors == 2:  # flip to black
            ret[c] = True
    return ret


with open('24.input') as f:
    flips = list(parse(f))

# Map (E, SE) coordinates -> False/white or True/black tile
tiles: Dict[Tuple[int, int], bool] = defaultdict(lambda: False)
for steps_to_flip in flips:
    coord = find_coord(steps_to_flip)
    tiles[coord] = not tiles[coord]

# part 1
print(sum(tiles.values()))

# part 2
for _ in range(100):
    tiles = nextday(tiles)
print(sum(tiles.values()))
