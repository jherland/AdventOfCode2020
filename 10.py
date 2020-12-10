from collections import Counter
from typing import Mapping


def diffs(adapters, start, end):
    prev = start
    for cur in adapters + [end]:
        assert cur - prev in {1, 2, 3}
        yield cur - prev
        prev = cur


def num_paths(adapters, start, end):
    available = {a for a in adapters if start < a < end}
    available.add(end)
    paths_to = {start: 1}

    for cur in sorted(available):
        prevs = {cur - 1, cur - 2, cur - 3} & paths_to.keys()
        paths_to[cur] = sum(paths_to[prev] for prev in prevs)

    return paths_to


with open('10.input') as f:
    adapters = sorted(int(line.rstrip()) for line in f)
start, end = 0, adapters[-1] + 3

# part 1
diff_counts: Mapping[int, int] = Counter(diffs(adapters, start, end))
print(diff_counts[1] * diff_counts[3])

# part 2
print(num_paths(adapters, start, end)[end])
