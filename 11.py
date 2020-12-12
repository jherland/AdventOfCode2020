def parse(f):
    legend = {'L': True, '.': False}
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            yield (y, x), legend[c]


def render(state):
    width = max(x for y, x in state.keys()) + 1
    height = max(y for y, x in state.keys()) + 1
    pixel = {None: '.', False: 'L', True: '#'}
    for y in range(height):
        for x in range(width):
            print(pixel[state.get((y, x))], end='')
        print()
    print()


def bbox(coords):
    '''Return bounding box around given coords: (ymin, xmin), (ymax, xmax).'''
    y_min = min(y for y, x in coords)
    x_min = min(x for y, x in coords)
    y_max = max(y for y, x in coords)
    x_max = max(x for y, x in coords)
    return (y_min, x_min), (y_max, x_max)


def within(pos, box):
    '''Return True iff pos is within the given box.'''
    y, x = pos
    (y_min, x_min), (y_max, x_max) = box
    return y_min <= y <= y_max and x_min <= x <= x_max


Dirs = {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}


def move(pos, dir):
    y, x = pos
    dy, dx = dir
    return (y + dy, x + dx)


def directly_adjacent(pos, points):
    '''Return 8 adjacent coordinates to the given pos.'''
    return {move(pos, dir) for dir in Dirs} & points


def nearest_in_dir(pos, dir, points):
    '''Return nearest point in the given direction from pos.'''
    box = bbox(points)
    while within(pos, box):
        pos = move(pos, dir)
        if pos in points:
            return pos
    return None


def lines_of_sight(pov, points):
    '''Return coordinates for the nearest point in all 8 directions.'''
    return {nearest_in_dir(pov, dir, points) for dir in Dirs} & points


def occupy(state, pos, neighbors, rule):
    '''Return True iff this seat becomes occupied in the next instant.'''
    return rule(state[pos], sum(state[nbor] for nbor in neighbors[pos]))


def step(state, neighbors, rule):
    '''Step entire state into the next instant for each iteration.'''
    while True:
        yield state
        state = {
            pos: occupy(state, pos, neighbors, rule) for pos in state.keys()}


def settle(state, neighbors, rule):
    '''Keep stepping until the state is stable.

    Return number of steps until repeat and the final state.
    '''
    prev = None
    for gen, state in enumerate(step(state, neighbors, rule)):
        if state == prev:
            break
        prev = state
    return gen, state


def part1_rule(occupied, neighbors_occupied):
    if not occupied and neighbors_occupied == 0:
        return True
    elif occupied and neighbors_occupied >= 4:
        return False
    else:
        return occupied


def part2_rule(occupied, neighbors_occupied):
    if not occupied and neighbors_occupied == 0:
        return True
    elif occupied and neighbors_occupied >= 5:
        return False
    else:
        return occupied


with open('11.input') as f:
    seats = {pos for pos, seat in parse(f) if seat}

# part 1
neighbors = {pos: directly_adjacent(pos, seats) for pos in seats}
when, settled = settle(dict.fromkeys(seats, False), neighbors, part1_rule)
# render(settled)
# print(when)
print(sum(settled.values()))

# part 2
neighbors = {pos: lines_of_sight(pos, seats) for pos in seats}
when, settled = settle(dict.fromkeys(seats, False), neighbors, part2_rule)
# render(settled)
# print(when)
print(sum(settled.values()))
