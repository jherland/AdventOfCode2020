def pwdb(f):
    for line in f:
        policy, pwd = line.split(':', 1)
        limits, letter = policy.split(' ', 1)
        lower, upper = map(int, limits.split('-', 1))
        assert lower <= upper
        assert len(letter) == 1
        assert len(pwd)
        yield lower, upper, letter, pwd.strip()


def is_count_within_limits(lower, upper, letter, pwd):
    return lower <= pwd.count(letter) <= upper


def count_matching_positions(lower, upper, letter, pwd):
    assert 0 < lower <= len(pwd)
    assert 0 < upper <= len(pwd)
    a, b = pwd[lower - 1], pwd[upper - 1]
    return (a == letter) + (b == letter)


with open('02.input') as f:
    db = list(pwdb(f))

# part 1
print(len([entry for entry in db if is_count_within_limits(*entry)]))

# part 2
print(len([entry for entry in db if count_matching_positions(*entry) == 1]))
