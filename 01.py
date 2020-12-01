from itertools import combinations
from math import prod

with open('01.input') as f:
    nums = [int(line) for line in f]


def find_addends(num_addends, target_sum):
    for addends in combinations(nums, num_addends):
        if sum(addends) == target_sum:
            yield addends


# part 1
print(prod(next(find_addends(2, 2020))))

# part 2
print(prod(next(find_addends(3, 2020))))
