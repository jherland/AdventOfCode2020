from collections import Counter
from math import prod
import re
import typing

rule_pattern = re.compile(r'(\d+)-(\d+) or (\d+)-(\d+)')


def create_predicate(rule):
    match = rule_pattern.fullmatch(rule.strip())
    assert match is not None
    a, b, c, d = map(int, match.groups())
    return lambda num: a <= num <= b or c <= num <= d


def parse_rules(f):
    for line in f:
        if not line.rstrip():
            return
        field, rule = line.split(':', 1)
        yield field, create_predicate(rule)


def parse_tickets(f):
    for line in f:
        if not line.rstrip():
            return
        yield [int(num) for num in line.rstrip().split(',')]


def ticket_error_rate(ticket, rules):
    for num in ticket:
        if all(predicate(num) is False for predicate in rules.values()):
            return num, True
    return 0, False


with open('16.input') as f:
    rules = dict(parse_rules(f))
    assert next(f) == 'your ticket:\n'
    tickets = list(parse_tickets(f))
    assert len(tickets) == 1
    my_ticket = tickets[0]
    assert next(f) == 'nearby tickets:\n'
    nearby_tickets = list(parse_tickets(f))

# part 1
print(sum(ticket_error_rate(t, rules)[0] for t in nearby_tickets))

# part 2
tickets = [t for t in nearby_tickets if not ticket_error_rate(t, rules)[1]]
possibles: typing.List[typing.Set[str]] = [set() for _ in range(len(rules))]
assignments = {}  # map determined field name to ticket index

# check ticket values against rules to determine possible field assignments
for i, ps in enumerate(possibles):
    for field, predicate in rules.items():
        if all(predicate(t[i]) for t in tickets):
            ps.add(field)
    assert len(ps) >= 1, i
    if len(ps) == 1:
        assignments[ps.pop()] = i

# narrow down to fully determine all field assignments
while len(assignments) < len(rules):
    counter: typing.Counter[str] = Counter()
    for i, ps in enumerate(possibles):
        ps -= set(assignments.keys())
        if len(ps) == 0:
            assert i in assignments.values()  # sanity check
        elif len(ps) == 1:  # only one possible assignment for this index
            field = ps.pop()
            assert field not in assignments
            assert i not in assignments.values()
            assignments[field] = i
        else:  # keep track of how many times a given field is a candidate
            counter.update(ps)
    for field, count in counter.items():
        if count == 1 and field not in assignments:  # field fits only 1 index
            indices = [i for i, ps in enumerate(possibles) if field in ps]
            assert len(indices) == 1
            i = indices.pop()
            assert i not in assignments.values()
            assignments[field] = i
            possibles[i] = set()

print(prod(
    my_ticket[i]
    for field, i in assignments.items()
    if field.startswith('departure ')
))
