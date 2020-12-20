from functools import cached_property
import math
import re
from typing import Callable, Dict, Iterable, Iterator, List, Set, Tuple, cast

North, South, West, East = 0, 1, 2, 3
Block = List[str]
Edges = Tuple[str, str, str, str]  # edges in N S W E order
Orientation = Tuple[int, int, int, int]  # N S W E indices from edge_symmetries
Transformer = Callable[[Block], Block]

Opposite = {North: South, South: North, West: East, East: West}

Seamonster = [
    '..................#.',
    '#....##....##....###',
    '.#..#..#..#..#..#...',
]


def block_edges(block: Block) -> Edges:
    '''Return (N, S, W, E) edges from a block.'''
    return (
        block[0],
        block[-1],
        ''.join(line[0] for line in block),
        ''.join(line[-1] for line in block),
    )


def rotateCCW(block: Block) -> Block:
    lines = ['' for _ in block[0]]
    for line in block:
        for i, c in enumerate(line):
            lines[i] += c
    return lines[::-1]


def flipH(block: Block) -> Block:
    return [line[::-1] for line in block]


def flipV(block: Block) -> Block:
    return block[::-1]


# Associate numbers with sequences of indices from edge_symmetries
# corresponding to N S W E edges after applying transformation
Orientations: Dict[Orientation, Transformer] = {
    # N S W E: no transformation
    (0, 1, 2, 3): lambda b: b,
    # E W -N -S: rotate CCW 90 degrees
    (3, 2, 4, 5): lambda b: rotateCCW(b),
    # -S -N -E -W: rotate 180 degrees
    (5, 4, 7, 6): lambda b: rotateCCW(rotateCCW(b)),
    # -W -E S N: rotate CW 90 degrees
    (6, 7, 1, 0): lambda b: rotateCCW(rotateCCW(rotateCCW(b))),
    # -N -S E W: flip horizontally
    (4, 5, 3, 2): lambda b: flipH(b),
    # S N -W -E: flip vertically
    (1, 0, 6, 7): lambda b: flipV(b),
    # W E N S: flip about main diagonal
    (2, 3, 0, 1): lambda b: flipV(rotateCCW(b)),
    # -E -W -S -N: flip about other diagonal
    (7, 6, 5, 4): lambda b: flipH(rotateCCW(b)),
}


class Tile:
    @classmethod
    def parse(cls, lines: List[str]) -> 'Tile':
        header = lines.pop(0)
        assert header.startswith('Tile ') and header.endswith(':')
        return cls(int(header[5:-1]), lines)

    def __init__(self, num, block):
        self.num: int = num
        self.block: Block = block

        # Start in default orientation. Mutated later with .orient():
        self.orientation: Orientation = list(Orientations.keys())[0]

    def __hash__(self):
        return hash(self.num)

    def __eq__(self, other):
        return self.num == other.num

    @cached_property
    def edge_symmetries(self) -> List[str]:
        '''Return possible edges in any orientation (flip + rotate).

        Figuring out how rotating + flipping a tile affect the N S W E edges:
            Rotating CW: N -> E -> -S -> -W -> N
            Rotating CCW: N -> -W -> -S -> E -> N
            Flip horizontally: N -> -N, S -> -S, E -> W, W -> E
            Flip vertically: N -> S, S -> N, E -> -E, W -> -W
        Hence all symmetries are found by returning edges and their reversals.
        return [N, S, W, E, -N, -S, -W, -E]
        '''
        orig_edges = block_edges(self.block)
        return list(orig_edges) + [edge[::-1] for edge in orig_edges]

    def edges(self) -> Edges:
        '''Return N S W E edges according to current orientation.'''
        return cast(
            Edges, tuple(self.edge_symmetries[i] for i in self.orientation))

    def facing(self, direction: int) -> str:
        return self.edges()[direction]

    def common_edges(self, other: 'Tile') -> Set[str]:
        '''Yield possible common edges between this tile and another.'''
        return set(self.edge_symmetries) & set(other.edge_symmetries)

    def adjacents(self, tiles: Iterable['Tile']) -> Iterator['Tile']:
        '''Yield possibly adjacent tiles.'''
        for tile in tiles:
            if self.num != tile.num and self.common_edges(tile):
                yield tile

    def orient(self, edge: str, direction: int) -> None:
        '''Orient this tile to show the given edge in the given direction.

        The 'direction' is an int that specifies north (0), south (1),
        west (2), or east (3).
        '''
        assert 0 <= direction <= 3
        orient_by_dir = {o[direction]: o for o in Orientations.keys()}
        self.orientation = orient_by_dir[self.edge_symmetries.index(edge)]

    def orient_next_to(self, other: 'Tile', direction: int) -> None:
        '''Determine orientation of this tile in relation to the given tile.

        The 'direction' is an int that tells use whether the given 'other' tile
        is to the north (0), south (1), west (2), or east (3) of this tile.
        '''
        assert self != other
        assert 0 <= direction <= 3
        facing = other.facing(Opposite[direction])
        assert facing in self.common_edges(other)
        self.orient(facing, direction)

    def size(self, with_edge):
        if with_edge:
            return len(self.block) + 1
        else:
            return len(self.block) - 2

    def render(self, with_edge):
        lines = Orientations[self.orientation](self.block)
        if with_edge:
            for line in lines:
                yield line + '|'
            yield '-' * len(line) + '+'
        else:
            for line in lines[1:-1]:
                yield line[1:-1]


def render(picture, with_edge=False):
    '''picture is a 2D list of tiles from top left to bottom right.'''
    tile_size = picture[0][0].size(with_edge)
    for row in picture:
        rowlines = ['' for _ in range(tile_size)]
        for tile in row:
            if tile is None:
                lines = ['?' * tile_size] * tile_size
            else:
                lines = tile.render(with_edge)
            for i, line in enumerate(lines):
                rowlines[i] += line
        yield from rowlines


def display(picture, with_edge=False):
    print('\n'.join(render(picture, with_edge)))


def find_neighbor(tile, direction, neighbors):
    for neighbor in neighbors[tile]:
        if tile.facing(direction) in tile.common_edges(neighbor):
            return neighbor


def find_seamonsters(image: List[str]) -> Iterator[Tuple[int, int]]:
    # Look for the middle line by regex, and cofirm the remainder manually
    patterns = [re.compile(pattern) for pattern in Seamonster]
    assert len(patterns) == 3
    for i, line in enumerate(image[1:-1]):
        for match in patterns[1].finditer(line):
            start, stop = match.span()
            sea1 = patterns[0].fullmatch(image[i + 0], start, stop)
            assert patterns[1].fullmatch(image[i + 1], start, stop)
            sea3 = patterns[2].fullmatch(image[i + 2], start, stop)
            if sea1 and sea3:
                yield i, start


def count_active_pixels(lines):
    return sum(line.count('#') for line in lines)


with open('20.input') as f:
    tiles = {
        Tile.parse(chunk.rstrip().split('\n'))
        for chunk in f.read().split('\n\n')
    }

neighbors = {tile: set(tile.adjacents(tiles)) for tile in tiles}
corners = {a for a, bs in neighbors.items() if len(bs) == 2}
assert(len(corners) == 4)

# part 1
print(math.prod(tile.num for tile in corners))

# part 2
# Start in a corner, and orient all tiles accordingly
size = int(math.sqrt(len(tiles)))
edges = {a for a, bs in neighbors.items() if len(bs) == 3}
assert(len(edges) == (size - 2) * 4)
topleft = corners.pop()
assert(all(neighbor in edges for neighbor in neighbors[topleft]))
top, left = neighbors[topleft]

# Figure out orientation of topleft corner
for east in topleft.common_edges(top):
    topleft.orient(east, East)
    if topleft.facing(South) not in topleft.common_edges(left):
        continue
assert topleft.facing(East) in topleft.common_edges(top)
assert topleft.facing(South) in topleft.common_edges(left)

# Orient neighbors
top.orient_next_to(topleft, 2)  # top has topleft to its West
left.orient_next_to(topleft, 0)  # left has topleft to its North

# Connect the rest of the picture
picture: List[List[Tile]] = [[topleft, top], [left]]

for y in range(size):
    if y >= len(picture):
        picture.append([])
    for x in range(size):
        if x >= len(picture[y]):  # Find correct tile and orient it.
            if x == 0:  # First tile on this row, use tile above
                prev, direction = picture[y - 1][x], North
            else:  # Use tile to our left
                prev, direction = picture[y][x - 1], West
            cur = find_neighbor(prev, Opposite[direction], neighbors)
            cur.orient_next_to(prev, direction)
            picture[y].append(cur)

# display(picture, with_edge=True)

# Find the image orientation with at least one sea monster
for xform in Orientations.values():
    image = xform(list(render(picture)))
    seamonsters = len(list(find_seamonsters(image)))
    if seamonsters:
        break

# How many active pixels are NOT part of a sea monster?
seamonsters_pixels = count_active_pixels(Seamonster) * seamonsters
print(count_active_pixels(image) - seamonsters_pixels)
