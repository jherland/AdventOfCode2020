from typing import Dict, NamedTuple


cups: Dict[int, 'Cup'] = {}  # doubly linked list: cup -> (prev, next)


class Cup(NamedTuple):
    prev: int
    next: int

    def __repr__(self) -> str:
        return f'<{self.prev} {self.next}>'


def move(i0):
    i1 = cups[i0].next   # pickup #1
    i2 = cups[i1].next   # pickup #2
    i3 = cups[i2].next   # pickup #3
    i4 = cups[i3].next   # after pickup #3

    iX = current - 1  # destination
    while iX in {i1, i2, i3} or iX not in cups:
        iX -= 1
        if iX <= 0:
            iX = len(cups)
    iY = cups[iX].next

    # remove pickup from after cur
    cups[i0], cups[i4] = Cup(cups[i0].prev, i4), Cup(i0, cups[i4].next)

    # insert pickup to after dest
    cups[iX], cups[i1] = Cup(cups[iX].prev, i1), Cup(iX, cups[i1].next)
    cups[i3], cups[iY] = Cup(cups[i3].prev, iY), Cup(i3, cups[iY].next)

    return i4


with open('23.input') as f:
    start = [int(c) for c in f.read().rstrip()]

# part 1
cups.clear()
for p, cur, n in zip([start[-1]] + start, start, start[1:] + [start[0]]):
    cups[cur] = Cup(p, n)
current = start[0]
for i in range(100):
    current = move(current)

i = cups[1].next
result = []
while i != 1:
    assert isinstance(i, int)
    result.append(i)
    i = cups[i].next
print(''.join(map(str, result)))

# part 2
cups.clear()
for p, cur, n in zip([1_000_000] + start, start + [10], start[1:] + [10, 11]):
    cups[cur] = Cup(p, n)
assert len(cups) == 10
for cur in range(11, 1_000_000):
    cups[cur] = Cup(cur - 1, cur + 1)
cups[1_000_000] = Cup(999_999, start[0])
assert len(cups) == 1_000_000
assert list(sorted(cups.keys())) == list(range(1, 1_000_001))
assert list(sorted(c.prev for c in cups.values())) == list(range(1, 1_000_001))
assert list(sorted(c.next for c in cups.values())) == list(range(1, 1_000_001))

current = start[0]
for i in range(10_000_000):
    current = move(current)

print(cups[1].next * cups[cups[1].next].next)
