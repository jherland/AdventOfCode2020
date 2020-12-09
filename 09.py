from itertools import combinations, filterfalse


def next_num_with_preamble(nums, preamble_len=25):
    assert len(nums) > preamble_len
    preamble = nums[:preamble_len]
    for n in nums[preamble_len:]:
        yield n, preamble
        preamble = preamble[1:] + [n]


def valid_xmas_num(num, preamble, sum_of_n=2):
    return any(
        sum(addends) == num for addends in combinations(preamble, sum_of_n))


def find_consecutive_nums_with_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            n = sum(nums[i:j])
            if n == target:
                yield i, j
            elif n > target:
                break  # next i


with open('09.input') as f:
    nums = [int(line.rstrip()) for line in f]

# part 1
first_invalid = next(filterfalse(
    lambda args: valid_xmas_num(*args), next_num_with_preamble(nums)))[0]
print(first_invalid)

# part 2
start, end = next(find_consecutive_nums_with_sum(nums, first_invalid))
addends = sorted(nums[start:end])
print(addends[0] + addends[-1])
