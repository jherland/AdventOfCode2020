from itertools import combinations
from math import prod


def find_addends(nums, length, target):
    return (ns for ns in combinations(nums, length) if sum(ns) == target)


with open('01.input') as f:
    nums = [int(line) for line in f]

# part 1
print(prod(next(find_addends(nums, 2, 2020))))

# part 2
print(prod(next(find_addends(nums, 3, 2020))))
