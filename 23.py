import pyximport; pyximport.install(language_level=3)  # noqa: E702
from helpers import day23_part2


def move(cups, cur):
    while len(cups) - cur <= 3:
        cups.append(cups.pop(0))
        cur -= 1
    triple = cups[cur + 1:cur + 4]
    assert len(triple) == 3
    needle = cups[cur] - 1
    while True:
        try:  # search left side
            dest = cups.index(needle, 0, cur)
            cups[dest + 1:cur + 4] = triple + cups[dest + 1:cur + 1]
            return (cur + 4) % len(cups)
        except ValueError:
            try:  # search right side
                dest = cups.index(needle, cur + 4)
                cups[cur + 1:dest + 1] = cups[cur + 4:dest + 1] + triple
                return cur + 1
            except ValueError:
                needle -= 1
                if needle <= 0:
                    needle = max(cups)


with open('23.input') as f:
    start = [int(c) for c in f.read().rstrip()]

# part 1
cups = list(start)
current = 0
for i in range(100):
    current = move(cups, current)
i1 = cups.index(1)
print(''.join(map(str, cups[i1 + 1:] + cups[:i1])))

# part 2
print(day23_part2(start))
