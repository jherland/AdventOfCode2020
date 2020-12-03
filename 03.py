from math import prod


def parse_map(f):
    legend = {'.': 0, '#': 1}
    for line in f:
        yield [legend[c] for c in line.strip()]


def slope_score(slope_map, slope, y=0):
    if y >= len(slope_map):
        return 0  # reached bottom
    dx, dy = slope
    assert y % dy == 0
    x = ((y // dy) * dx) % len(slope_map[y])
    return slope_map[y][x] + slope_score(slope_map, slope, y + dy)


with open('03.input') as f:
    slope_map = list(parse_map(f))

# part 1
print(slope_score(slope_map, (3, 1)))

# part 2
check_slopes = {(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)}
print(prod(slope_score(slope_map, slope) for slope in check_slopes))
