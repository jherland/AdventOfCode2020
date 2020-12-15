from typing import Iterable, Iterator


def play(starting: Iterable[int]) -> Iterator[int]:
    starting = iter(starting)
    prev = next(starting)
    yield prev

    seen = {}  # map number -> sequence number
    for seq, cur in enumerate(starting):
        yield cur
        seen[prev] = seq
        prev = cur

    while True:
        seq += 1
        if prev not in seen:
            cur = 0
        else:
            cur = seq - seen[prev]
        yield cur
        seen[prev] = seq
        prev = cur


with open('15.input') as f:
    starting = [int(num) for num in f.read().strip().split(',')]

for i, number in enumerate(play(starting), start=1):
    # part 1
    if i == 2020:
        print(number)
    # part 2
    if i == 30000000:
        print(number)
        break
