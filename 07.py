import re

rule_regex = re.compile(r'(\w+ \w+) bags contain(.*)\.')
content_regex = re.compile(r' (\d+) (\w+ \w+) bags?')


def parse_rules(f):
    for line in f:
        match = rule_regex.fullmatch(line.rstrip())
        assert match is not None
        bag, rhs = match.groups()
        matches = [content_regex.fullmatch(s) for s in rhs.split(',')]
        contents = {b: int(n) for n, b in (m.groups() for m in matches if m)}
        yield bag, contents


def bags_within(rules, outer):
    return sum(
        n + n * bags_within(rules, bag) for bag, n in rules[outer].items())


with open('07.input') as f:
    rules = dict(parse_rules(f))

# part 1
q = ['shiny gold']
containers = set()
while q:
    bag = q.pop()
    for holder, helds in rules.items():
        if bag in helds:
            q.append(holder)
            containers.add(holder)
print(len(containers))

# part 2
print(bags_within(rules, 'shiny gold'))
