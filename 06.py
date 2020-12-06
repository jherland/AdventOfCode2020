def parse_groups(f):
    for lines in f.read().split('\n\n'):
        yield [set(line) for line in lines.split('\n')]


with open('06.input') as f:
    groups = list(parse_groups(f))

# part 1
print(sum(len(set.union(*persons)) for persons in groups))

# part 2
print(sum(len(set.intersection(*persons)) for persons in groups))
